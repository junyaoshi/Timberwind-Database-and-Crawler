'''Run this to crawl urls'''
import google_url_crawler as gc


# change the variable query to change the search keyword
# toggle between True and False to turn on and off auto_add
query = 'Visitor Management Software in the United States'
auto_add = False
gc.crawl(query, auto_add)