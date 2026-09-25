"""
Builds the raw Sydney housing sold-property dataset.

Source: Domain.com.au sold-listings search pages for three Sydney suburbs
(Castle Hill NSW 2154, Parramatta NSW 2150, Liverpool NSW 2170), collected
by hand on 25 Sep 2026 by reading the first 2-3 pages of "Sold" results for
each suburb (https://www.domain.com.au/sold-listings/<suburb>-nsw-<postcode>/).
Only listings with a disclosed sale price were kept ("Price Withheld"
listings were skipped, since they have no usable target value).

Each row below was transcribed directly from a listing card: address,
sale price, bed/bath/parking counts, floor/land area (m^2, where shown),
property type, sale date, and sale method (private treaty / auction /
sold prior to auction).
"""
import pandas as pd

# columns: suburb, address, price, beds, baths, parking, area_sqm, property_type, sale_date, sale_method
records = [
    # ---------------- LIVERPOOL (page 1) ----------------
    ("Liverpool", "G01/19 Bigge Street, Liverpool", 560000, 2, 2, 1, None, "Apartment", "2026-09-24", "private treaty"),
    ("Liverpool", "12/53 Bathurst Street, Liverpool", 510000, 2, 1, 1, None, "Apartment", "2026-09-23", "private treaty"),
    ("Liverpool", "1/10-12 Lewis Road, Liverpool", 825000, 3, 2, 2, None, "Townhouse", "2026-09-23", "private treaty"),
    ("Liverpool", "18 Rose Street, Liverpool", 1582000, 7, 3, 4, 809, "House", "2026-09-19", "auction"),
    ("Liverpool", "69 Orange Grove Road, Liverpool", 910000, 3, 2, 1, 613, "House", "2026-09-17", "private treaty"),
    ("Liverpool", "2/28 Nagle Street, Liverpool", 410000, 2, 1, 1, None, "Apartment", "2026-09-17", "private treaty"),
    ("Liverpool", "18/26 Goulburn Street, Liverpool", 399000, 2, 1, 1, 1460, "Apartment", "2026-09-15", "private treaty"),
    ("Liverpool", "8/8-10 Lachlan Street, Liverpool", 550000, 2, 2, 1, None, "Apartment", "2026-09-15", "private treaty"),
    ("Liverpool", "40 Maryvale Avenue, Liverpool", 1200000, 3, 1, 1, 701, "House", "2026-09-15", "private treaty"),
    ("Liverpool", "3 Secant Street, Liverpool", 2000000, 4, 2, 2, 676, "House", "2026-09-15", "private treaty"),
    ("Liverpool", "22B Mary Crescent, Liverpool", 1200000, 5, 3, 2, 302, "Semi-detached", "2026-09-12", "private treaty"),
    ("Liverpool", "202/21 Atkinson Street, Liverpool", 530000, 2, 2, 1, None, "Apartment", "2026-09-11", "private treaty"),
    ("Liverpool", "501/311 Hume Highway, Liverpool", 600000, 2, 2, 1, None, "Apartment", "2026-09-11", "private treaty"),
    ("Liverpool", "41 Tully Avenue, Liverpool", 1150000, 6, 2, 2, None, "House", "2026-09-11", "private treaty"),
    ("Liverpool", "505/17 Shepherd Street, Liverpool", 570000, 2, 2, 1, 131, "Apartment", "2026-09-11", "private treaty"),
    ("Liverpool", "803/2 Lachlan Street, Liverpool", 650000, 2, 2, 1, None, "Apartment", "2026-09-11", "private treaty"),
    ("Liverpool", "35/4 Riverpark Drive, Liverpool", 500000, 2, 1, 1, None, "Apartment", "2026-09-08", "private treaty"),
    ("Liverpool", "3 Edwin Place, Liverpool", 1235000, 4, 2, 5, 613, "House", "2026-09-07", "private treaty"),
    ("Liverpool", "3/1 Stanton Street, Liverpool", 770000, 3, 1, 1, None, "Townhouse", "2026-09-03", "private treaty"),
    # ---------------- LIVERPOOL (page 2) ----------------
    ("Liverpool", "6/16-18 Mainsbridge Avenue, Liverpool", 720000, 2, 2, 1, None, "Townhouse", "2026-08-29", "private treaty"),
    ("Liverpool", "35/12-20 Lachlan Street, Liverpool", 730000, 3, 2, 2, 157, "Apartment", "2026-08-28", "private treaty"),
    ("Liverpool", "12/119-121 Castlereagh Street, Liverpool", 460000, 2, 1, 1, 93, "Apartment", "2026-08-27", "private treaty"),
    ("Liverpool", "9/53 Goulburn Street, Liverpool", 423000, 2, 1, 1, None, "Apartment", "2026-08-27", "private treaty"),
    ("Liverpool", "503/311 Hume Highway, Liverpool", 570000, 2, 2, 1, None, "Apartment", "2026-08-25", "private treaty"),
    ("Liverpool", "2/30 Speed Street, Liverpool", 385000, 2, 1, 1, None, "Apartment", "2026-08-24", "private treaty"),
    ("Liverpool", "4/44-46 Passefield Street, Liverpool", 875000, 3, 2, 1, None, "Townhouse", "2026-08-24", "private treaty"),
    ("Liverpool", "1303/30 Shepherd Street, Liverpool", 539000, 2, 2, 1, 106, "Apartment", "2026-08-24", "private treaty"),
    ("Liverpool", "19/32 Pirie Street, Liverpool", 400000, 2, 1, 1, None, "Apartment", "2026-08-22", "private treaty"),
    ("Liverpool", "8 Angelo Avenue, Liverpool", 935000, 3, 1, 1, None, "House", "2026-08-22", "auction"),
    ("Liverpool", "5/10 Christie Street, Liverpool", 870000, 3, 2, 1, None, "House", "2026-08-22", "private treaty"),
    ("Liverpool", "10/50 Castlereagh Street, Liverpool", 433000, 2, 1, 1, None, "Apartment", "2026-08-21", "private treaty"),
    ("Liverpool", "1/34 Goulburn Street, Liverpool", 390000, 2, 1, 1, 1055, "Apartment", "2026-08-20", "private treaty"),
    ("Liverpool", "66/387 Macquarie Street, Liverpool", 570000, 2, 2, 1, None, "Apartment", "2026-08-19", "private treaty"),
    ("Liverpool", "40/387 Macquarie Street, Liverpool", 431000, 1, 1, 1, None, "Apartment", "2026-08-19", "private treaty"),
    ("Liverpool", "401/21 Charles Street, Liverpool", 550000, 2, 2, 1, None, "Apartment", "2026-08-13", "private treaty"),

    # ---------------- PARRAMATTA (page 1) ----------------
    ("Parramatta", "33/18 Thomas Street, Parramatta", 605000, 2, 1, 1, None, "Apartment", "2026-09-25", "private treaty"),
    ("Parramatta", "22/4 Peace Lane, Parramatta", 500000, 2, 2, 1, 101, "Apartment", "2026-09-19", "auction"),
    ("Parramatta", "4/44-50 Thomas Street, Parramatta", 720000, 2, 1, 1, 128, "Townhouse", "2026-09-16", "private treaty"),
    ("Parramatta", "2315/45 Macquarie Street, Parramatta", 640000, 2, 2, 1, None, "Apartment", "2026-09-16", "private treaty"),
    ("Parramatta", "1/3 Stewart Street, Parramatta", 570000, 2, 1, 1, None, "Apartment", "2026-09-16", "private treaty"),
    ("Parramatta", "641/180 George Street, Parramatta", 600000, 2, 1, None, None, "Apartment", "2026-09-16", "private treaty"),
    ("Parramatta", "610/36-46 Cowper Street, Parramatta", 575000, 2, 2, 1, None, "Apartment", "2026-09-14", "private treaty"),
    ("Parramatta", "2/16 Betts Street, Parramatta", 660000, 2, 1, 1, None, "Apartment", "2026-09-12", "private treaty"),
    ("Parramatta", "1404/1-3 Valentine Avenue, Parramatta", 320000, 1, 1, None, None, "Apartment", "2026-09-11", "private treaty"),
    ("Parramatta", "820K/2 Morton Street, Parramatta", 650000, 2, 2, 1, 12280, "Apartment", "2026-09-11", "private treaty"),
    # ---------------- PARRAMATTA (page 2) ----------------
    ("Parramatta", "15/12 Early Street, Parramatta", 493000, 2, 1, 1, None, "Apartment", "2026-09-11", "private treaty"),
    ("Parramatta", "1010 H/2 Morton Street, Parramatta", 687000, 2, 2, 1, None, "Apartment", "2026-09-11", "private treaty"),
    ("Parramatta", "1601/11 Hassall Street, Parramatta", 700000, 2, 2, 1, None, "Apartment", "2026-09-11", "private treaty"),
    ("Parramatta", "33/68 Great Western Highway, Parramatta", 520000, 2, 1, 1, None, "Apartment", "2026-09-11", "private treaty"),
    ("Parramatta", "1607/45 Macquarie Street, Parramatta", 547000, 1, 1, 1, None, "Apartment", "2026-09-10", "private treaty"),
    ("Parramatta", "505/23 Hassall Street, Parramatta", 660000, 2, 2, 1, None, "Apartment", "2026-09-09", "private treaty"),
    ("Parramatta", "89/459-463 Church Street, Parramatta", 580000, 2, 2, 1, None, "Apartment", "2026-09-04", "private treaty"),
    ("Parramatta", "8/64-66 Great Western Highway, Parramatta", 425000, 1, 1, 1, None, "Apartment", "2026-09-04", "private treaty"),
    ("Parramatta", "1702/45 Macquarie Street, Parramatta", 705000, 2, 2, 1, None, "Apartment", "2026-09-04", "private treaty"),
    ("Parramatta", "10/4 Peace Lane, Parramatta", 570000, 2, 2, 1, 108, "Apartment", "2026-09-03", "private treaty"),
    ("Parramatta", "505/330 Church Street, Parramatta", 700000, 2, 2, 1, None, "Apartment", "2026-09-03", "private treaty"),
    # ---------------- PARRAMATTA (page 3) ----------------
    ("Parramatta", "9/178 George Street, Parramatta", 490000, 1, 1, None, None, "Apartment", "2026-09-01", "private treaty"),
    ("Parramatta", "3/23 Good Street, Parramatta", 569000, 2, 1, 1, None, "Apartment", "2026-08-31", "private treaty"),
    ("Parramatta", "17/10-12 Thomas Street, Parramatta", 650000, 2, 1, 1, None, "Apartment", "2026-08-31", "private treaty"),
    ("Parramatta", "401/6 River Road West, Parramatta", 540000, 2, 2, 1, 108, "Apartment", "2026-08-30", "private treaty"),
    ("Parramatta", "1403/1-3 Valentine Avenue, Parramatta", 355000, 1, 1, 1, None, "Apartment", "2026-08-28", "private treaty"),
    ("Parramatta", "1201/45 Macquarie Street, Parramatta", 566000, 1, 1, 1, None, "Apartment", "2026-08-28", "private treaty"),
    ("Parramatta", "5/30-32 Queens Avenue, Parramatta", 680000, 2, 1, 1, None, "Apartment", "2026-08-28", "private treaty"),
    ("Parramatta", "11/32 Hassall Street, Parramatta", 590000, 2, 2, 1, None, "Apartment", "2026-08-28", "private treaty"),
    ("Parramatta", "C26/88-98 Marsden Street, Parramatta", 552000, 2, 2, 1, None, "Apartment", "2026-08-27", "private treaty"),
    ("Parramatta", "15/1 Good Street, Parramatta", 480000, 2, 1, 1, None, "Apartment", "2026-08-27", "private treaty"),
    ("Parramatta", "1417/32 Hunter Street, Parramatta", 560000, 1, 1, 1, None, "Apartment", "2026-08-25", "private treaty"),
    ("Parramatta", "907/6-10 Charles Street, Parramatta", 720000, 3, 2, 1, None, "Apartment", "2026-08-25", "private treaty"),
    ("Parramatta", "16L/15 Campbell Street, Parramatta", 405000, 1, 1, 1, None, "Apartment", "2026-08-25", "auction"),
    ("Parramatta", "D603/1 Broughton Street, Parramatta", 680000, 2, 2, 1, None, "Apartment", "2026-08-25", "private treaty"),
    ("Parramatta", "805/21 Hassall Street, Parramatta", 410000, 1, 1, None, None, "Apartment", "2026-08-24", "private treaty"),

    # ---------------- CASTLE HILL (page 1) ----------------
    ("Castle Hill", "89 Darcey Road, Castle Hill", 2150000, 6, 3, 3, None, "House", "2026-09-25", "private treaty"),
    ("Castle Hill", "22 Orleans Way, Castle Hill", 2065000, 4, 3, 2, 511, "House", "2026-09-25", "prior to auction"),
    ("Castle Hill", "14 Coolong Street, Castle Hill", 2180000, 4, 2, 2, 695, "House", "2026-09-23", "private treaty"),
    ("Castle Hill", "55/73 Crane Road, Castle Hill", 1350000, 3, 2, 2, None, "Townhouse", "2026-09-23", "private treaty"),
    ("Castle Hill", "1/240-242 Old Northern Road, Castle Hill", 895000, 2, 2, 2, None, "Apartment", "2026-09-21", "private treaty"),
    ("Castle Hill", "46/73 Crane Road, Castle Hill", 1390000, 3, 2, 2, 245, "Villa", "2026-09-18", "private treaty"),
    ("Castle Hill", "11 Brunette Drive, Castle Hill", 1955000, 4, 2, 2, 695, "House", "2026-09-17", "private treaty"),
    ("Castle Hill", "28 Ferguson Avenue, Castle Hill", 2300000, 4, 3, 3, 923, "House", "2026-09-14", "private treaty"),
    ("Castle Hill", "25/1-11 Rosa Crescent, Castle Hill", 825000, 2, 2, 2, None, "Apartment", "2026-09-11", "private treaty"),
    ("Castle Hill", "6 Woodvale Place, Castle Hill", 2900000, 5, 3, 3, 900, "House", "2026-09-11", "private treaty"),
    ("Castle Hill", "60 Womurrung Avenue, Castle Hill", 5200000, 5, 5, 6, 1284, "House", "2026-09-11", "private treaty"),
    # ---------------- CASTLE HILL (page 2) ----------------
    ("Castle Hill", "Address withheld, Castle Hill", 2900000, 4, 2, 2, 901, "House", "2026-09-10", "private treaty"),
    ("Castle Hill", "135 Ridgecrop Drive, Castle Hill", 2315000, 5, 3, 2, 802, "House", "2026-09-10", "private treaty"),
    ("Castle Hill", "75/59a Castle Street, Castle Hill", 1180000, 3, 2, 2, 231, "Townhouse", "2026-09-09", "private treaty"),
    ("Castle Hill", "22/49-55 Cecil Avenue, Castle Hill", 1140000, 3, 2, 2, None, "Apartment", "2026-09-04", "private treaty"),
    ("Castle Hill", "9/2-4 Purser Avenue, Castle Hill", 935000, 2, 2, 1, None, "Apartment", "2026-09-04", "private treaty"),
    ("Castle Hill", "307/11 Fishburn Crescent, Castle Hill", 855000, 2, 2, 1, None, "Apartment", "2026-08-31", "private treaty"),
    ("Castle Hill", "19 Galahad Crescent, Castle Hill", 2560000, 5, 3, 2, 950, "House", "2026-08-29", "auction"),
    ("Castle Hill", "12 Barcote Place, Castle Hill", 2450000, 5, 3, 2, 741, "House", "2026-08-26", "private treaty"),
    ("Castle Hill", "10/2-4 Purser Avenue, Castle Hill", 1150000, 3, 2, 2, None, "Apartment", "2026-08-25", "private treaty"),
    ("Castle Hill", "61 Cambewarra Avenue, Castle Hill", 3550000, 5, 5, 4, 923, "House", "2026-08-25", "private treaty"),
    # ---------------- CASTLE HILL (page 3) ----------------
    ("Castle Hill", "19 Clarke Place, Castle Hill", 2700000, 4, 3, 2, 902, "House", "2026-08-24", "private treaty"),
    ("Castle Hill", "11 Tristan Court, Castle Hill", 2325000, 5, 3, 3, None, "House", "2026-08-24", "auction"),
    ("Castle Hill", "66 David Road, Castle Hill", 2312000, 5, 3, 4, 741, "House", "2026-08-22", "auction"),
    ("Castle Hill", "6 Bordeaux Crescent, Castle Hill", 2320000, 5, 4, 2, 450, "House", "2026-08-21", "private treaty"),
    ("Castle Hill", "62 Excelsior Avenue, Castle Hill", 1950000, 3, 1, 1, 1037, "House", "2026-08-21", "prior to auction"),
    ("Castle Hill", "57 Church Street, Castle Hill", 2776000, 4, 2, 3, 916, "House", "2026-08-20", "private treaty"),
    ("Castle Hill", "111 Chepstow Drive, Castle Hill", 2655000, 6, 4, 3, 700, "House", "2026-08-19", "private treaty"),
    ("Castle Hill", "96 Harrington Avenue, Castle Hill", 1300000, 3, 2, 2, 229, "Duplex", "2026-08-18", "prior to auction"),
    ("Castle Hill", "405/27 Ashford Avenue, Castle Hill", 632000, 1, 1, 1, 87, "Apartment", "2026-08-13", "private treaty"),
    ("Castle Hill", "55B First Farm Drive, Castle Hill", 1800000, 4, 3, 2, 403, "Semi-detached", "2026-08-11", "private treaty"),
    ("Castle Hill", "2 Cumberland Avenue, Castle Hill", 2305000, 5, 2, 2, 929, "House", "2026-08-08", "auction"),
    ("Castle Hill", "5 Kincraig Court, Castle Hill", 2720000, 6, 3, 4, 905, "House", "2026-08-08", "auction"),
    ("Castle Hill", "15 Anthony Road, Castle Hill", 2690000, 3, 2, 1, 776, "House", "2026-08-07", "private treaty"),
]

cols = ["suburb", "address", "price", "beds", "baths", "parking", "area_sqm",
        "property_type", "sale_date", "sale_method"]
df = pd.DataFrame(records, columns=cols)
df["sale_date"] = pd.to_datetime(df["sale_date"])

print("Total rows:", len(df))
print(df["suburb"].value_counts())
print("Any duplicate addresses (same address+price)?", df.duplicated(subset=["address", "price"]).sum())

df.to_csv("sydney_housing_raw.csv", index=False)
print("Saved sydney_housing_raw.csv")
