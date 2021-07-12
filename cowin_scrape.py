import requests
import selenium.common.exceptions
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from chromedriver_py import binary_path  # pip install chromedriver-py==91.0.4472.19


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-infobars")
prefs = {"profile.default_content_setting_values.notifications": 1}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(executable_path=binary_path, options=chrome_options)


clickDistOption = ""
clickStateSelect = ""
selectStateTarget = ""
clickDistrictSelect = ""
selectDistrictTarget = ""
searchBtn = ""


def init_var():
    global clickDistOption, clickStateSelect, selectStateTarget, clickDistrictSelect, selectDistrictTarget, searchBtn
    # initialising Cowin Variables
    clickDistOption = '//div[@id="mat-tab-label-0-1"]'
    clickStateSelect = '//span[@class="mat-select-placeholder mat-select-min-line ng-tns-c82-22 ng-star-inserted"]'
    selectStateTarget = '//mat-option[@id="mat-option-17"]'
    clickDistrictSelect = '//span[@class="mat-select-placeholder mat-select-min-line ng-tns-c82-24 ng-star-inserted"]'
    selectDistrictTarget = '//mat-option[@id="mat-option-48"]'
    searchBtn = '//button[@class="searchBtn pin-search-btn district-search"]'


def start(url):
    init_var()
    global driver
    global clickDistOption, clickStateSelect, selectStateTarget, clickDistrictSelect, selectDistrictTarget, searchBtn

    driver.get(url)

    print("Getting list of hospitals in Thiruvananthapuram, Kerala")

    _clickDistrict = driver.find_element_by_xpath(clickDistOption).click()

    _clickKerala = driver.find_element_by_xpath(clickStateSelect).click()
    target = driver.find_element_by_xpath(selectStateTarget)

    actions = ActionChains(driver)
    actions.move_to_element(target)
    actions.perform()

    target.click()

    time.sleep(1)

    _clickTVM = driver.find_element_by_xpath(clickDistrictSelect).click()

    target = driver.find_element_by_xpath(selectDistrictTarget)

    actions = ActionChains(driver)
    actions.move_to_element(target)
    actions.perform()

    target.click()

    _clickSearchBtn = driver.find_element_by_xpath(searchBtn).click()


def error_return(parent, path):
    try:
        parent.find_element_by_xpath(path)
        return path
    except selenium.common.exceptions.NoSuchElementException:
        return False


def data_scrape():
    global driver
    main_data = driver.find_elements_by_xpath('//div[@class="row ng-star-inserted"]')
    dict_mainData = []
    if main_data:
        for i in main_data:
                dict_data = {}

                dose1, dose2, vaccine, age, days = [], [], [], [], []
                hospital_name = i.find_element_by_xpath(
                    './/div[@class="row-disp"]//h5[@class="center-name-title"]').text
                hospital_add = i.find_element_by_xpath('.//div[@class="row-disp"]//p[@class="center-name-text"]').text
                data = i.find_elements_by_xpath('.//li[@class="ng-star-inserted"]')
                day = 0
                for j in data:
                    day = day + 1
                    many_slots = error_return(j, './/div[@class="slots-box ng-star-inserted"]')
                    few_slots = error_return(j, './/div[@class="slots-box less-seat ng-star-inserted"]')
                    error_notFound = False
                    if many_slots:
                        error_notFound = many_slots
                    elif few_slots:
                        error_notFound = few_slots
                    else:
                        continue
                    dose1.append(j.find_element_by_xpath(str(error_notFound) + '//div[@class="dosetotal"]//span[@title="Dose 1"]').text)
                    dose2.append(j.find_element_by_xpath(str(error_notFound) + '//div[@class="dosetotal"]//span[@title="Dose 2"]').text)
                    vaccine.append(j.find_element_by_xpath(str(error_notFound) + '//div[@class="vaccine-cnt"]//h5[@class="name"]').text)
                    age.append(j.find_element_by_xpath(str(error_notFound) + '//div[@class="ng-star-inserted"]//span[@class="age-limit"]').text)
                    days.append(day)

                if len(dose1) > 0:
                    dict_data["Hospital_Name"] = hospital_name
                    dict_data["Hospital_Address"] = hospital_add
                    dict_data["Dose 1"] = dose1
                    dict_data['Dose 2'] = dose2
                    dict_data["Vaccine"] = vaccine
                    dict_data["Age"] = age
                    dict_data["Days"] = days

                if len(dict_data) > 0:
                    dict_mainData.append(dict_data)

    else:
        print("UNABLE TO READ DATA.!!!!!")

    return dict_mainData





def start_scrape():
    WebUrl = 'https://www.cowin.gov.in/home'
    print("Starting Cowin Scrape")
    start(WebUrl)
    count = 0
    while True:
        count = count + 1
        print("Searching #" + str(count))
        time.sleep(2)
        data_scrape()
        time.sleep(1)


def reset():
    _clickSearchBtn = driver.find_element_by_xpath('//button[@class="searchBtn pin-search-btn district-search"]').click()

# start_scrape()
