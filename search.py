'''Google's Paid Scraper'''


from googleapiclient.discovery import build
import pprint


my_api_key = 'AIzaSyC5X0sStlMR8uUBpIkKw0a17f1mHkQ9FMk'
my_cse_id  = '016259665263182537934:ebnvzmoyvgu'


def google_search(search_term, api_key, cse_id):
    service = build("customsearch", "v1", developerKey=api_key)
    l = []
    for i in range(0,1):
        position = i*10 + 1
        res = service.cse().list(q=search_term, exactTerms=search_term, cx=cse_id, num=10, start=position).execute()
        try:
            l.append(res['items'])
        except KeyError:
            return l
    return l

results = google_search(
    'nearshore', my_api_key, my_cse_id)

for result in results:
    try:
        pprint.pprint(result['pagemap']['localbusiness'][0]['name'])
    except KeyError:
        print('no name for this company')
    try:
        pprint.pprint(result['pagemap']['webpage'][0]['url'])
    except KeyError:
        print('no url for this company')
    try:
        pprint.pprint(result['pagemap']['webpage'][0]['description'])
    except KeyError:
        print('no description for this company')