'''This is the internal code for crawl.py, run crawl.py instead of this'''
from googlesearch import search
import csv
import csv_database as db

global url_list
url_list = []
global bad_domains
bad_domains = ['.gov','.edu','.org','.int','.mil']
global foreign_domains
foreign_domains = ['.sg','.se','.cn','.de','.eu','.in','.nl','.au','.uk','.nz','.tv','.ie']
global irrelevant_urls
irrelevant_urls = ['www.indeed.com',
                   'www.cnet.com',
                   'www.washingtonpost.com',
                   'www.quora.com',
                   'www.nytimes.com',
                   'www.bloomberg.com',
                   'www.bbc.com',
                   'finance.yahoo.com',
                   'www.seekingalpha.com',
                   'www.prnewswire.com',
                   'www.capterra.com',
                   'www.softwareadvice.com',
                   'www.g2crowd.com',
                   'www.financesonline.com',
                   'www.honeywellaccess.com',
                   'www.pfind.com',
                   'dbworks.com',
                   'techcrunch.com',
                   'www.youtube.com',
                   'www.amazon.com',
                   'www.medium.com',
                   'medium.com',
                   'www.ibm.com',
                   'www.vimeo.com',
                   'financesonline.com',
                   'www.serchen.com',
                   'www.getapp.com',
                   'www.trustradius.com',
                   'www.nbc-2.com',
                   'www.researchnreports.com',
                   'www.wave3.com',
                   'www.steemit.com',
                   'www.cmswire.com',
                   'www.htfmarketreport.com',
                   'www.reportsnreports.com',
                   'www.dell.com',
                   'www.researchgate.net',
                   'www.linkedin.com']


'''num is the number of urls it scrapes per iteration. 
start is the ID of the first url to be taken
start and stop is the range of urls it is scraping'''


def crawl(query, auto_add=True):

    for raw_url in search(query, tld='com', lang='en', num=40, start=0, stop=200, pause=2.5):
        slash_count = 0
        url = ''
        i = 0
        skip_to_next_url = False
        while i < len(raw_url) and not skip_to_next_url:
            char = raw_url[i]

            # start scraping after 2 slashes
            if char == '/':
                slash_count += 1
            elif slash_count == 2:
                url += char
            if slash_count == 3:

                # the last four characters and the last 3 characters
                last_4 = url[-4:]
                last_3 = url[-3:]

                # if the url is irrelevant (news, analysis,...)
                if url in url_list or url in irrelevant_urls:
                    skip_to_next_url = True

                # if the url has bad domain
                elif last_4 in bad_domains:
                    skip_to_next_url = True


                # if the url is foreign
                elif last_3 in foreign_domains:
                    skip_to_next_url = True

                # put url in local database, print it on the console
                else:

                    # checks for duplicates in db
                    try:
                        with open('database.csv', 'r') as file:
                            reader = csv.reader(file)
                            for row in reader:
                                website = row[2]
                                if url == website:
                                    skip_to_next_url = True

                            # all clear
                            if not skip_to_next_url:
                                url_list.append(url)
                                print(url)

                                # if auto_add boolean is true, add to database
                                if auto_add:
                                    db.add_companies(url, 'crawler_auto')
                                skip_to_next_url = True
                    except IOError as e:
                        print(e)
            i += 1

    # print everything onto csv
    try:
        # variable query is defined from crawl.py
        with open('Crawler_' + query + '.csv', 'w+', newline='') as file:
            writer = csv.writer(file)
            csv_content = [
                ['Status','Email Status','Reviewer Notes','Reviewed by','Organization - Analyst','Person - Analyst','Skip','Analyst Skip','Quick Check',
                 'Email Check','Organization - Name','Notes - Content','Organization - Revenue(MM)','Organization - Employee Count','Organization - Year Founded',
                 'Organization - Website','Person - Phone','State','Organization - Address','Key Executives (Current and Prior)','Raw Address',
                 'Organization - Industry','Organization - Snippet', 'Person - Full Name', 'Person - First Name',
                 'Person - Last Name', 'Person - Type', 'Person - Email', 'Person - Age','High/Low']]
            for url in url_list:
                csv_row = ['','','','','','','','','','','','','','','', url]
                csv_content.append(csv_row)
            writer.writerows(csv_content)
    except IOError as e:
        print(e)


