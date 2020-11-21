import pandas as pd

dli_url = "https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada/study-permit/prepare/designated-learning-institutions-list.html"

dli_df = pd.read_html(dli_url)


def dli_df_single(df):
    return pd.concat(df, ignore_index=True)


def get_province(province):
    provinces = [
        (0, "british columbia", "bc"),
        (1, "alberta", "ab"),
        (2, "saskatchewan", "sk"),
        (3, "manitoba", "mb"),
        (4, "ontario", "on"),
        (5, "quebec", "qc"),
        (6, "prince edward island", "pei"),
        (7, "new brunswick", "nb"),
        (8, "nova scotia", "ns"),
        (9, "newfoundland and labrador", "nl"),
        (10, "yukon", "yt"),
        (11, "northwest territories", "nt"),
    ]
    for i in provinces:
        if province in i:
            return dli_df[i[0]]


def get_city(city):
    return dli_df_single(dli_df).query("City == '@city'")


def get_pgwp_eligible(option, city=None, province=None):
    if option.lower() in ["yes", "y", True]:
        option = "Yes"
    elif option.lower() in ["no", "n", False]:
        option = "No"

    if city:
        city = city.title()
        return get_city(city).query("`Offers PGWP-eligible programs` == '@option'")

    if province:
        province = province.lower()
        return get_province(province).query(
            "`Offers PGWP-eligible programs` == '@option'"
        )

    return dli_df_single(dli_df).query("`Offers PGWP-eligible programs` == '@option'")


# def is_dli_pgwp_eligible(dli):
# //TODO: Create function to check if given DLI is pgwp eligible
# //TODO: Create class to export to different formats
# //TODO: Create function to filter out DLIs with certain keywords

df_canada = pd.concat(dli_df, sort=False)  # concats into one dataframe
filter_ = [
    "Helicopters",
    "Flying",
    "Aviation",
    "Flight",
    "Air",
]  # list of strings to filter
df_canada = df_canada[
    ~df_canada["Name of institution"].str.contains("|".join(filter_))
]  # filters flying schools out

_filter = np.in1d(
    df_canada["Offers PGWP-eligible programs"].values, ["No"], invert=True
)  # removes those that don't have a pgwp eligible program
df_canada = df_canada[_filter]

with pd.ExcelWriter("Canada_List.xlsx") as writer:
    df_canada.to_excel(writer, "Sheet 1")
    writer.save()
