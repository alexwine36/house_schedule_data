import json
import pandas as pd
import re

schedule_df = pd.read_csv("./files/compiled_schedules.csv")


def slugify(s):
    """
    Simplifies ugly strings into something URL-friendly.
    >>> print slugify("[Some] _ Article's Title--")
    some-articles-title
    """

    # "[Some] _ Article's Title--"
    # "[some] _ article's title--"
    s = s.lower()

    # "[some] _ article's_title--"
    # "[some]___article's_title__"
    for c in [' ', '-', '.', '/']:
        s = s.replace(c, '_')

    # "[some]___article's_title__"
    # "some___articles_title__"
    s = re.sub('\W', '', s)

    # "some___articles_title__"
    # "some   articles title  "
    s = s.replace('_', ' ')

    # "some   articles title  "
    # "some articles title "
    s = re.sub('\s+', ' ', s)

    # "some articles title "
    # "some articles title"
    s = s.strip()

    # "some articles title"
    # "some-articles-title"
    s = s.replace(' ', '_')

    return s


j_dat = {
    "metadata": {
        "colab": {
            "collapsed_sections": [],
            "name": "Abrazo Schedules_v3.ipynb",
            "provenance": [],
            "version": "0.0.1"
        },
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.7.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 1,
    "cells": []
}


setup_cell = {
    "cell_type": "code",
    "metadata": {},
    "source": [
        "import pandas as pd\n",
        "import numpy as np\n",
        "import datetime\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "from dateutil.relativedelta import relativedelta\n",
        "## Bokeh Setup\n",
        "\n",
        "from bokeh.io import output_notebook, show\n",
        "from bokeh.models import ColumnDataSource, HoverTool, FactorRange\n",
        "from bokeh.plotting import figure\n",
        "from bokeh.transform import factor_cmap\n",
        "from bokeh.palettes import Spectral, Category20, Paired\n",
        "from math import pi\n",
        "\n",
        "colors = []\n",
        "colors.append(Spectral[11]) \n",
        "colors.append(Category20[20])\n",
        "colors.append(Paired[12])\n",
        "\n",
        "\n",
        "def add_colors(color_list, flat_list):\n",
        "  for sublist in color_list:\n",
        "    for item in sublist:\n",
        "      flat_list.append(item)\n",
        "\n",
        "new_colors = []\n",
        "add_colors(colors, new_colors)\n",
        "colors = new_colors\n",
        "\n"
        # "pd.set_option('display.max_rows', None)\n"
        "pd.set_option('max_columns', None)\n",
        "sns.set(rc={'figure.figsize':(20,10)})\n",
        "\n",
        "house_df = pd.read_csv(\"https://raw.githubusercontent.com/alexwine36/house_schedule_data/master/files/compiled_houses.csv\")\n",
        "schedule_df = pd.read_csv(\"https://raw.githubusercontent.com/alexwine36/house_schedule_data/master/files/compiled_schedules.csv\")\n",
        "\n",
        "schedule_df[\"YEAR\"] = pd.DatetimeIndex(schedule_df[\"ACTUALSTARTDATE\"]).year\n",
        "schedule_df[\"MONTH\"] = pd.DatetimeIndex(schedule_df[\"ACTUALSTARTDATE\"]).month\n",
        "schedule_df[\"WEEK\"] = pd.DatetimeIndex(schedule_df[\"ACTUALSTARTDATE\"]).week\n",
        "\n",
        "schedule_df[\"DURATION_VAR\"] = schedule_df[\"ACTUAL_DURATION\"] - schedule_df[\"DAYS\"]\n",
        "schedule_df[\"DURATION_VAR_BUS\"] = schedule_df[\"BUSINESS_DURATION\"] - schedule_df[\"DAYS\"]\n",
        "months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']\n",
        "years = sorted(schedule_df[\"YEAR\"].unique(), reverse=True)\n",
        "\n",
        "def get_month_name(month):\n",
        "  return months[(month - 1)]\n",
        "\n",
        "schedule_df[\"MONTH_NAME\"] = schedule_df[\"MONTH\"].apply(get_month_name)\n",
        "from IPython.display import display_html\n",
        "def display_side_by_side(*args):\n",
        "    html_str=''\n",
        "    for df in args:\n",
        "        html_str+=df.to_html()\n",
        "    display_html(html_str.replace('table','table style=\"display:inline\"'),raw=True)\n",
        "\n"
        "## DATA CLEANING\n",
        "\n",
        "schedule_df = schedule_df[schedule_df[\"BUSINESS_DURATION\"] > 0]\n",
        "schedule_df = schedule_df[schedule_df[\"DEVELOPMENTCODE\"] != \"OS\"]\n",
        "schedule_df = schedule_df.reset_index(drop=True)\n"
        "\n",
        "## PAST 18 & 12 MONTHS SCHEDULE\n",
        "\n",
        "max_date = schedule_df[\"ACTUALFINISHDATE\"].max()\n",
        "start_18 = np.datetime64(max_date) - np.timedelta64((30 * 18), 'D')\n",
        "start_18 = np.datetime64(start_18, 'M')\n",
        "start_12 = np.datetime64(max_date) - np.timedelta64((30 * 12), 'D')\n",
        "start_12 = np.datetime64(start_12, 'M')\n",
        "schd_df = schedule_df[schedule_df[\"ACTUALFINISHDATE\"].values.astype('datetime64[D]') > start_18]\n",
        "schd_df = schd_df.reset_index(drop=True)\n",
        "schd_12 = schedule_df[schedule_df[\"ACTUALFINISHDATE\"].values.astype('datetime64[D]') > start_12]\n",
        "schd_12 = schd_12.reset_index(drop=True)\n"
        "\n",

    ],
    "execution_count": 0,
    "outputs": []
}

categories = schedule_df["CATEGORY"].unique()


j_dat["cells"].append(setup_cell)
j_dat["cells"].append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "## BUSINESS DURATION FROM MEAN\n",
        "\n",
        "def duration_diff(row):\n",
        "  return row[\"BUSINESS_DURATION\"] - schd_df[schd_df[\"DESCRIPTION\"] == row[\"DESCRIPTION\"]][\"BUSINESS_DURATION\"].mean()\n",
        "def duration_diff_12(row):\n",
        "  return row[\"BUSINESS_DURATION\"] - schd_12[schd_12[\"DESCRIPTION\"] == row[\"DESCRIPTION\"]][\"BUSINESS_DURATION\"].mean()\n",
        "\n",
        "\n",
        "schd_df[\"AVG_DURATION_DIFFERENCE\"] = schd_df.apply(duration_diff, axis=1)\n",
        "schd_12[\"AVG_DURATION_DIFFERENCE\"] = schd_12.apply(duration_diff_12, axis=1)\n"
    ],
    "execution_count": 0,
    "outputs": []
})

# PROJECTED DURATIONS


j_dat["cells"].append({
    "metadata": {},
    "cell_type": "markdown",
    "source": [
        "# Scheduled vs. Actual Duration"
    ]
})

j_dat["cells"].append({
    "metadata": {},
    "cell_type": "markdown",
    "source": [
        "## All"
    ]
})
j_dat["cells"].append({
    "metadata": {},
    "cell_type": "code",
    "source": [
        "schd_diff = schd_df.groupby([\"DESCRIPTION\"]).quantile(.5)[['DAYS', 'BUSINESS_DURATION' ]].rename(columns={\"DAYS\": \"PROJECTED_DURATION\"})\n",
        "schd_12_diff = schd_12.groupby([\"DESCRIPTION\"]).quantile(.5)[['DAYS', 'BUSINESS_DURATION' ]].rename(columns={\"DAYS\": \"PROJECTED_DURATION\"})\n",
        "schd_diff"
    ],
    "execution_count": 0,
    "outputs": []
})
j_dat["cells"].append({
    "metadata": {},
    "cell_type": "markdown",
    "source": [
        "## Actual Duration Greater than Scheduled Duration\n*18 Months vs. 12 Months*"
    ]
})
j_dat["cells"].append({
    "metadata": {},
    "cell_type": "code",
    "source": [
        "schd_diff_more = schd_diff[schd_diff[\"PROJECTED_DURATION\"] < schd_diff[\"BUSINESS_DURATION\"]]\n",
        "schd_12_diff_more = schd_12_diff[schd_12_diff[\"PROJECTED_DURATION\"] < schd_12_diff[\"BUSINESS_DURATION\"]]\n",
        "display_side_by_side(schd_diff_more, schd_12_diff_more)"
    ],
    "execution_count": 0,
    "outputs": []
})
j_dat["cells"].append({
    "metadata": {},
    "cell_type": "markdown",
    "source": [
        "## Actual Duration Less than Scheduled Duration"
    ]
})
j_dat["cells"].append({
    "metadata": {},
    "cell_type": "code",
    "source": [
        "schd_diff_more = schd_diff[schd_diff[\"PROJECTED_DURATION\"] > schd_diff[\"BUSINESS_DURATION\"]]\n",
        "schd_diff_more"
    ],
    "execution_count": 0,
    "outputs": []
})


categories = [x for x in categories if str(x) != 'nan']
schedule_df = schedule_df.dropna(subset=["NAME"])
print(categories)
for category in categories:
    group = schedule_df[schedule_df["CATEGORY"] == category]
    vendors = group["NAME"].unique()
    category_all = slugify(category)
    category_12 = "%s_12" % (category_all)
    category_18 = "%s_18" % (category_all)
    print(len(vendors), vendors)

    j_dat["cells"].append({
        "metadata": {},
        "cell_type": "markdown",
        "source": [
            "## %s" % (category)
        ]
    })
    j_dat["cells"].append({
        "metadata": {},
        "cell_type": "markdown",
        "source": [
            "### Duration by Year"
        ]
    })

    vendors_array = "vendors_%s" % (category_all)
    j_dat["cells"].append({
        "metadata": {},
        "cell_type": "code",
        "source": [
            "%s = schedule_df[schedule_df['CATEGORY'] == '%s']\n" % (
                category_all, category),
            "%s = schd_df[schd_df['CATEGORY'] == '%s']\n" % (
                category_18, category),
            "%s = schd_12[schd_12['CATEGORY'] == '%s']\n" % (
                category_12, category),
            "%s = %s['NAME'].unique()\n" % (vendors_array, category_all),
            "%s = [x for x in vendors_%s if str(x) != 'nan']" % (
                vendors_array, category_all),
        ],
        "execution_count": 0,
        "outputs": []
    })
    j_dat["cells"].append({
        "metadata": {},
        "cell_type": "code",
        "source": [
            "group = %s.groupby([\"DESCRIPTION\", \"YEAR\"], as_index=False).mean()[[\"DESCRIPTION\", \"YEAR\", 'BUSINESS_DURATION']].sort_index()\n" % (
                category_all),
            "group.YEAR = group.YEAR.astype(str)\n",
            "\n",
            "group[\"V_ACT\"] = list(zip(group[\"DESCRIPTION\"], group[\"YEAR\"]))\n",
            "\n",
            "source = ColumnDataSource(group)\n",
            "\n",
            "p = figure(plot_width=1000, x_range=FactorRange(*group[\"V_ACT\"]), title=\"Duration by Year\",\n",
            "          tools=\"hover,pan,wheel_zoom,box_zoom,reset\", tooltips=\"@DESCRIPTION - @YEAR: @BUSINESS_DURATION\"\n",
            "          )\n",
            "\n",
            "p.vbar(x=\"V_ACT\", top=\"BUSINESS_DURATION\", width=0.9, source=source,\n",
            "      color=factor_cmap('YEAR', palette=colors, factors=group[\"YEAR\"].unique())\n",
            "      )\n",
            "\n",
            "\n",
            "p.xaxis.major_label_orientation = pi/2\n",
            "p.x_range.range_padding = 0.05\n",
            "\n",
            "output_notebook()\n",
            "show(p)"
        ],
        "execution_count": 0,
        "outputs": []
    })
    if len(vendors) > 1:
        j_dat["cells"].append({
            "metadata": {},
            "cell_type": "markdown",
            "source": [
                "### Average Task Duration by Vendor\n",
                "*18 Months*"
            ]
        })
        j_dat["cells"].append({
            "metadata": {},
            "cell_type": "code",
            "source": [
                # "plmb_schd = plmb_schd.dropna(subset=[\"VENDORNUMBER\"])\n",
                # "\n",
                "group = %s.groupby([\"DESCRIPTION\", \"NAME\"], as_index=False).mean()[[\"NAME\", \"DESCRIPTION\", \"AVG_DURATION_DIFFERENCE\"]]\n" % (
                    category_18),
                "\n",
                "group[\"V_ACT\"] = list(zip(group[\"DESCRIPTION\"], group[\"NAME\"]))\n",
                "\n",
                "source = ColumnDataSource(group)\n",
                "\n",
                "p = figure(plot_width=1000, x_range=FactorRange(*group[\"V_ACT\"]), title=\"Duration Difference by Vendor\",\n",
                "          tools=\"hover,pan,wheel_zoom,box_zoom,reset\", tooltips=\"@DESCRIPTION - @NAME: @AVG_DURATION_DIFFERENCE\"\n",
                "          )\n",
                "\n",
                "p.vbar(x=\"V_ACT\", top=\"AVG_DURATION_DIFFERENCE\", width=0.9, source=source,\n",
                "      color=factor_cmap('NAME', nan_color='gray', palette=colors, factors=%s)\n" % (
                    vendors_array),
                "      )\n",
                "\n",
                "\n",
                "p.xaxis.major_label_orientation = pi/2\n",
                "p.x_range.range_padding = 0.05\n",
                "\n",
                "\n",
                "output_notebook()\n",
                "show(p)"
            ],
            "execution_count": 0,
            "outputs": []
        })


# print(json.dumps(j_dat))

generated_file = open("./trial/House_Schedules_Generated.ipynb", 'w')

json.dump(j_dat, generated_file, indent=4)
