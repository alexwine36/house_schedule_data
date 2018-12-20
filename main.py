import pandas as pd
import numpy as np
from uszipcode import SearchEngine
import datetime

search = SearchEngine(simple_zipcode=True)

activity_codes = pd.read_csv("./files/ACTIVITY_CODE Description - Sheet1.csv")
h_schedules = pd.read_csv("./files/house_schedules.csv",
                          na_values="      ", dtype={'VENDORNUMBER': np.str, }, parse_dates=["ACTUALSTARTDATE", "ACTUALFINISHDATE", "EARLYFINISHDATE", "EARLYSTARTDATE"], infer_datetime_format=True)
vendor_master = pd.read_csv(
    "./files/vendor_master.csv", dtype={'NUMBER': np.str})
zip_codes = pd.read_csv("./files/development_zips.csv")
start_matrix = pd.read_csv(
    "./files/StartScheduleMatrix - Matrix.csv", na_values="X", parse_dates=["O.L. Date", "Mgmt Release", "Colors", "Water Req", "PP Req.", "PP Back", "PP Approved", "CL Closing", "POs Released", "Plan Check Submitted",	"Permit Back",	"As Built",	"Plumb Set",	"Framer Set",	"Elec Set",	"City Set",	"IHMS Docs",	"IHMS Sched",	"Start Pack",	"CO"], infer_datetime_format=True)


zipcode_df = pd.DataFrame(columns=["ZIP", "CITY", "COUNTY", "POPULATION", "POPULATION_DENSITY",
                                   "HOUSING_UNITS", "OCCUPIED_HOUSING_UNITS", "MEDIAN_HOME_VALUE", "MEDIAN_HOUSEHOLD_INCOME"])


def generate_zip_data():
    global zip_codes
    global zipcode_df
    print("Running ZIP CODE DATA")

    zipcode_data = zip_codes["ZIP"].unique()

    for zipcode in zipcode_data:
        zi = search.by_zipcode(zipcode)
        zip_data = {
            "ZIP": zipcode, "CITY": zi.major_city,
            "COUNTY": zi.county, "POPULATION": zi.population,
            "POPULATION_DENSITY": zi.population_density,
            "HOUSING_UNITS": zi.housing_units, "OCCUPIED_HOUSING_UNITS": zi.occupied_housing_units,
            "MEDIAN_HOME_VALUE": zi.median_home_value, "MEDIAN_HOUSEHOLD_INCOME": zi.median_household_income
        }
        # print(zip_data)
        zipcode_df = zipcode_df.append(zip_data, ignore_index=True)

    # print(zipcode_df)

    zip_codes = zip_codes.join(zipcode_df.set_index('ZIP'), on="ZIP")
    print("Finished ZIP CODE DATA")


house_schedules = h_schedules.dropna(
    subset=[
        # "VENDORNUMBER",
        "ACTUALSTARTDATE", "ACTUALFINISHDATE"])
# print(house_schedules)
house_schedules = house_schedules.reset_index(drop=True)


# print(house_schedules)
def generate_houses_df():
    print("Running Generate House Schedules")
    homes = house_schedules["HOUSENUMBER"].unique()

    houses_df = pd.DataFrame(
        columns=["HOUSENUMBER", "CONSTRUCTIONTIME", "LOANTIME"])
    for house in homes:
        is_house = house_schedules["HOUSENUMBER"] == house
        current_house = house_schedules[is_house]
        start = current_house[current_house["ACTIVITYCODE"] == "C05"]
        end = current_house[current_house["ACTIVITYCODE"] == "P57"]
        co = current_house[current_house["ACTIVITYCODE"] == "P30"]

        if start.empty:
            print("C05 Missing")
            start = current_house[current_house["ACTIVITYCODE"] == "A00"]
            # pass

        if co.empty:
            # print("END SKIP")
            pass
        else:
            end_date = None
            loan_time = None
            start_date = start["EARLYSTARTDATE"].values.astype('datetime64[D]')[
                0]
            if not end.empty:
                end_date = end["ACTUALFINISHDATE"].values.astype('datetime64[D]')[
                    0]
                loan_time = end_date - start_date
                loan_time = loan_time / np.timedelta64(1, 'D')
            const_end_date = co["ACTUALFINISHDATE"].values.astype('datetime64[D]')[
                0]
            # print(start_date, end_date)

            build_time = const_end_date - start_date
            build_time = build_time / np.timedelta64(1, 'D')

            # print(build_time, loan_time)

            house_data = {
                "HOUSENUMBER": house,
                "CONSTRUCTIONTIME": build_time,
                "LOANTIME": loan_time,
                "YEAR": pd.to_datetime(start_date).year
            }
            # print(house_data)

            houses_df = houses_df.append(house_data, ignore_index=True)

    houses_df = houses_df.dropna(
        subset=[
            # "VENDORNUMBER",
            "CONSTRUCTIONTIME", "YEAR"])

    houses_df = houses_df.join(
        start_matrix.set_index('Job #'), on="HOUSENUMBER")
    houses_df = houses_df.join(zip_codes.set_index('DEVELOPMENT'), on="DEV")
    houses_df.to_csv('./files/compiled_houses.csv', index=False)
    print("Finished Generate House Schedules")


def calc_vendor_load():
    global house_schedules
    vendor_load = pd.DataFrame()

    for idx, row in house_schedules.iterrows():
        vendor = row["VENDORNUMBER"]
        start = row["ACTUALSTARTDATE"]
        plus = start + datetime.timedelta(days=7)
        minus = start - datetime.timedelta(days=7)
        count = 0 | house_schedules[(house_schedules["VENDORNUMBER"] == vendor) & (
            house_schedules["ACTUALSTARTDATE"] >= minus) & (house_schedules["ACTUALSTARTDATE"] <= plus)]["VENDORNUMBER"].count()

        vendor_load = vendor_load.append({
            "TWO_WEEK_LOAD": count
        }, ignore_index=True)

    print(vendor_load)
    house_schedules = house_schedules.join(vendor_load)

# developments = house_schedules["DEVELOPMENTCODE"].unique()
# houses = house_schedules["HOUSENUMBER"].unique()
# activities = house_schedules["ACTIVITYCODE"].unique()
# vendors = house_schedules["VENDORNUMBER"].unique()
# total_rows = house_schedules.count()[0]


def generate_house_schedules():
    hs = house_schedules.join(
        vendor_master.set_index('NUMBER'), on="VENDORNUMBER")

    hs = hs.join(activity_codes.set_index('ACTIVITYCODE'), on="ACTIVITYCODE")
    hs = hs.join(zip_codes.set_index('DEVELOPMENT'), on="DEVELOPMENTCODE")

    hs["BUSINESS_DURATION"] = np.busday_count(
        hs["ACTUALSTARTDATE"].values.astype('datetime64[D]'), hs["ACTUALFINISHDATE"].values.astype('datetime64[D]'))
    hs["BUSINESS_DURATION"] = hs["BUSINESS_DURATION"] + 1
    hs["ACTUAL_DURATION"] = hs["ACTUALFINISHDATE"] - hs["ACTUALSTARTDATE"]
    hs["ACTUAL_DURATION"] = hs["ACTUAL_DURATION"] / np.timedelta64(1, 'D')
    hs["ACTUAL_DURATION"] = hs["ACTUAL_DURATION"] + 1
    hs = hs.drop([
        'Unnamed: 33',
        'Unnamed: 4',
    ], axis=1)
    print(list(hs.columns.values))

    hs.to_csv('./files/compiled_schedules.csv', index=False)


if __name__ == "__main__":
    generate_zip_data()
    generate_houses_df()
    # calc_vendor_load()
    # generate_house_schedules()
