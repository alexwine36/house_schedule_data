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

# zip_codes["CITY"] = search.by_zipcode(zip_codes["ZIP"]).major_city

# print(zip_codes)

zipcode_df = pd.DataFrame(columns=["ZIP", "CITY", "COUNTY", "POPULATION", "POPULATION_DENSITY",
                                   "HOUSING_UNITS", "OCCUPIED_HOUSING_UNITS", "MEDIAN_HOME_VALUE", "MEDIAN_HOUSEHOLD_INCOME"])

zipcode_data = zip_codes["ZIP"].unique()

for zipcode in zipcode_data:
         # print(zipcode["ZIP"])
    zi = search.by_zipcode(zipcode)
    # print(str(zipcode))
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

# new_columns = pd.DataFrame(columns=['ACTUAL_DURATION', 'ACTIVITYNAME'])

# print(house_schedules)
# print(vendor_master)
# print(activity_codes)


house_schedules = h_schedules.dropna(
    subset=[
        # "VENDORNUMBER",
        "ACTUALSTARTDATE", "ACTUALFINISHDATE"])
# print(house_schedules)
house_schedules = house_schedules.reset_index(drop=True)

homes = house_schedules["HOUSENUMBER"].unique()
# print(house_schedules[house_schedules["ACTIVITYCODE"] == "P57"])


houses_df = pd.DataFrame(
    columns=["HOUSENUMBER", "CONSTRUCTIONTIME", "LOANTIME"])

# print(house_schedules)

for house in homes:
    is_house = house_schedules["HOUSENUMBER"] == house
    current_house = house_schedules[is_house]
    start = current_house[current_house["ACTIVITYCODE"] == "A00"]
    end = current_house[current_house["ACTIVITYCODE"] == "P57"]
    co = current_house[current_house["ACTIVITYCODE"] == "P30"]

    if start.empty:
        # print("A00 Missing")
        start = current_house[current_house["ACTIVITYCODE"] == "C05"]
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
# print(houses_df)
houses_df = houses_df.join(
    start_matrix.set_index('Job #'), on="HOUSENUMBER")
houses_df = houses_df.join(zip_codes.set_index('DEVELOPMENT'), on="DEV")
houses_df.to_csv('./files/compiled_houses.csv', index=False)


# VENDOR ACTIVE JOB COUNT
# house_schedules["YEAR"] = pd.DatetimeIndex(
#     house_schedules["ACTUALSTARTDATE"]).year
# house_schedules["MONTH"] = pd.DatetimeIndex(
#     house_schedules["ACTUALSTARTDATE"]).month
# house_schedules["WEEK"] = pd.DatetimeIndex(
#     house_schedules["ACTUALSTARTDATE"]).week
# years = house_schedules["YEAR"].unique()
# for year in years:
#     h_yr = house_schedules[house_schedules["YEAR"] == year]
#     weeks = h_yr["WEEK"].unique()

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
# if idx < 25:
#     print(plus, minus)
#     print(count["VENDORNUMBER"].value_counts())
#   count = schedule_df[]

developments = house_schedules["DEVELOPMENTCODE"].unique()
houses = house_schedules["HOUSENUMBER"].unique()
activities = house_schedules["ACTIVITYCODE"].unique()
vendors = house_schedules["VENDORNUMBER"].unique()
total_rows = house_schedules.count()[0]


# print(house_schedules)
# print(developments)


hs = house_schedules.join(vendor_master.set_index('NUMBER'), on="VENDORNUMBER")

hs = hs.join(activity_codes.set_index('ACTIVITYCODE'), on="ACTIVITYCODE")
hs = hs.join(zip_codes.set_index('DEVELOPMENT'), on="DEVELOPMENTCODE")

# hs = hs.join(houses_df.set_index('HOUSENUMBER'), on="HOUSENUMBER")
# print(hs)

# hs["ACTUALSTARTDATE"] = hs["ACTUALSTARTDATE"].values.astype('datetime64[D]')
# hs["ACTUALFINISHDATE"] = hs["ACTUALFINISHDATE"].values.astype('datetime64[D]')
hs["BUSINESS_DURATION"] = np.busday_count(
    hs["ACTUALSTARTDATE"].values.astype('datetime64[D]'), hs["ACTUALFINISHDATE"].values.astype('datetime64[D]'))
hs["BUSINESS_DURATION"] = hs["BUSINESS_DURATION"] + 1
hs["ACTUAL_DURATION"] = hs["ACTUALFINISHDATE"] - hs["ACTUALSTARTDATE"]
hs["ACTUAL_DURATION"] = hs["ACTUAL_DURATION"] / np.timedelta64(1, 'D')
hs["ACTUAL_DURATION"] = hs["ACTUAL_DURATION"] + 1
# print(hs)


# print(row["VENDORNUMBER"])
# vendor = vendor_master.loc[vendor_master['NUMBER']
#    == row["VENDORNUMBER"]]
# print(vendor["NAME"])
# house_schedules.loc[idx, 'VENDORNAME'] = vendor["NAME"]
# print(house_schedules)
# print(developments)
# print(len(houses))
# print(activities)
# print(vendors)


# print(total_rows)


hs = hs.drop([
    'Unnamed: 33',
    'Unnamed: 4',
], axis=1)
print(list(hs.columns.values))

hs.to_csv('./files/compiled_schedules.csv', index=False)
