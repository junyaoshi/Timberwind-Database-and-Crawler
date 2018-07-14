'''database internal code'''
import csv


def read_file(f, is_netadvantage = True):
    '''This function reads five columns of the input file'''
    try:
        l = []
        with open(f,'r') as file:
            reader = csv.reader(file)
            for row in reader:
                new_list = []
                # name
                new_list.append(row[10])
                # year founded
                new_list.append(row[14])
                # website
                new_list.append(row[15])
                # phone
                new_list.append(row[16])
                # address
                new_list.append(row[18])
                # source (NA or Scraper)
                if is_netadvantage:
                    new_list.append('NetAdvantage')
                else:
                    new_list.append('Crawler')
                l.append(new_list)
        del(l[0])
        return l
    except IOError:
        print("Could not read file: " + f)


def read_raw(f):
    '''This function reads the database and return the content of the database as a list of lists variable'''
    try:
        l=[]
        with open(f, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                l.append(row)
        return l
    except IOError as e:
        print(e)


def add_companies(f, the_type='NetAdvantage'):
    try:
        with open('database.csv', 'a') as file:
            writer = csv.writer(file)

            # adding to db automatically while crawling
            if the_type == 'crawler_auto':
                line = ['','',f,'','','Crawler']
                writer.writerow(line)

            # adding to db manually after crawling
            elif the_type == 'crawler_manual':
                l = read_file(f, False)
                for line in l:
                    writer.writerow(line)

            # adding from NetAdvantage
            else:
                l = read_file(f)
                for line in l:
                    if not process_companies(line, 'line', False):
                        writer.writerow(line)
    except IOError as e:
        print(e)


def process_companies(comp, the_type='file', is_netadvantage=True):
    db = read_raw('database.csv')

    # if checking a line (used by add_companies)
    if the_type == 'line' and not is_netadvantage:
        for i in range(len(db)):

            # checking against crawler data (check only website)
            if db[i][0] == '':
                if comp[2] == db[i][2]:
                    return True

            # checking against NA data (check 4 entries)
            elif comp[1] == db[i][1] and comp[2] == db[i][2] and comp[3] == db[i][3] and comp[4] == db[i][4]:
                return True
        return False

    # if checking a crawler file
    elif the_type == 'file' and not is_netadvantage:
        l = read_raw(comp)
        try:
            with open(comp, 'w') as file:
                writer = csv.writer(file)
                for i in range(1, len(l)):
                    line = l[i]
                    website = line[15]

                    #checking only website
                    for j in range(len(db)):
                        if website == db[j][2]:
                            l[i][6] = 1
                writer.writerows(l)
        except IOError as e:
            print(e)


    # if checking a netadvantage file
    elif the_type == 'file' and is_netadvantage:
        l = read_raw(comp)
        try:
            with open(comp, 'w') as file:
                writer = csv.writer(file)
                for i in range(1, len(l)):
                    line = l[i]
                    name = line[10]
                    year = line[14]
                    website = line[15]
                    phone = line[16]
                    address = line[18]
                    for j in range(len(db)):

                        # checking all data against crawler data
                        if db[j][0] == '':
                            if website == db[j][2]:
                                l[i][6] = 1

                        # checking data with non_blank website field against NA data
                        elif website != '' and website == db[j][2]:
                            l[i][6] = 1

                        # checking data with blank website field against NA data
                        elif website == '' and name == db[j][0] and year == db[j][1] and phone == db[j][
                            3] and address == db[j][4]:
                            l[i][6] = 1
                writer.writerows(l)
        except IOError as e:
            print(e)
