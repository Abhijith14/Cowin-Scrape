import cowin_scrape
import time

# import required module
from playsound import playsound


def alert():
    playsound('audio2.mp3')


WebUrl = 'https://www.cowin.gov.in'
print("Starting Cowin Scrape")
count = 0

cowin_scrape.start(WebUrl)


def start():
    global count
    while True:
        count = count + 1
        print("Searching #" + str(count))
        time.sleep(2)
        result = cowin_scrape.data_scrape()
        if len(result) != 0:
            print(result)
            for i in result:
                if "COVISHIELD" in i['Vaccine'] or "SPUTNIK V" in i['Vaccine']:
                    if str(i['Age']) == "['18 & Above']" or str(i['Age']) == "['18-44 Only']":#"['Age 18+']":
                        d1 = str(i['Dose 1']).split(r"['D1\n")
                        d1 = int(str(d1[1]).replace("']", ""))
                        if d1 > 0:
                            print("Found `" + str(i['Vaccine']))
                            print(str(i['Hospital_Name']) + " ---- " + str(i["Hospital_Address"]))
                            print(i['Dose 1'])
                            print(i['Dose 2'])
                            print(str(i['Age']))
                            alert()
            print("====================================")
        time.sleep(1)
        cowin_scrape.reset()


start()
