import csv_database as db


# change the variable list_name to check a list
# toggle the is_netadvantage variable between True and False to select input file type (NetAdvantage/Crawler)

list_name = 'NA_Medical Waste Disposal.csv'
is_netadvantage = True

db.process_companies(list_name, 'file', is_netadvantage)
