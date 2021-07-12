import cowin_scrape
import time

WebUrl = 'https://www.cowin.gov.in'
print("Starting Cowin Scrape")
cowin_scrape.start(WebUrl)
count = 0


def start():
    global count
    while True:
        count = count + 1
        print("Searching #" + str(count))
        time.sleep(2)
        result = cowin_scrape.data_scrape()
        if len(result) != 0:
            print()
            print(len(result), " vaccine centers available")
            print()
            for i in result:
                print("Found " + str(i['Vaccine']))
                print(str(i['Hospital_Name']) + " ---- " + str(i["Hospital_Address"]))
                print(i['Dose 1'])
                print(i['Dose 2'])
                print(str(i['Age']))
                print()
                print("====================================")
                print()
            print()
            print()
        time.sleep(1)
        cowin_scrape.reset()


start()
