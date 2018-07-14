import csv_database as db


'''change the variable list_name to add companies'''


list_name = "Crawler_Visitor Management Software in the United States.csv"

# change the variable below to 'crawler_manual' or 'NetAdvantage'
the_type = 'crawler_manual'
db.add_companies(list_name, the_type)