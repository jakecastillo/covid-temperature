# from selenium import webdriver 
# from selenium.webdriver.common.by import By 
# from selenium.webdriver.support.ui import WebDriverWait 
# from selenium.webdriver.support import expected_conditions as EC 
# from selenium.common.exceptions import TimeoutException

# option = webdriver.ChromeOptions()
# option.add_argument(“ — incognito”)

import pandas
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Chrome load adblocker
options = Options()
options.add_argument('--load-extension=/Users/autonomous/Downloads/uBlock0.chromium')

driver = webdriver.Chrome("/Users/autonomous/Downloads/chromedriver")
driver.get("https://www.wunderground.com/history")

# Get COVID county data
covid_data = pandas.read_csv('./covid-confirmed-usafacts.csv')

counties = [f'{covid_data.values[0][1]}, {covid_data.values[0][2]}']

for county in range(108, 3195):
  print(f'Getting data for {covid_data.values[county][1]}, {covid_data.values[county][2]} ({county})')
  # Get search bar
  location = driver.find_element_by_xpath('//*[@id="historySearch"]')
  location.send_keys(f'{covid_data.values[county][1]}, {covid_data.values[county][2]}')

  time.sleep(3)

  # Sleep to allow searching
  WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="historyForm"]/search-autocomplete/ul')))
  
  # Select first entry
  locationSelect = driver.find_element_by_xpath('//*[@id="historyForm"]/search-autocomplete/ul/li[2]/a/span[1]')
  driver.find_element_by_xpath('//*[@id="historyForm"]/search-autocomplete/ul/li[2]/a/span[1]').click()

  # Set month and day. Year is already set by default
  dateMonth = driver.find_element_by_xpath('//*[@id="dateSelect"]/div/select[1]/option[2]').click()
  dateDay = driver.find_element_by_xpath('//*[@id="dateSelect"]/div/select[2]/option[1]').click()

  # Click "View" button
  viewButton = driver.find_element_by_xpath('//*[@id="dateSelect"]/div/input').click()

  WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="inner-content"]/div[2]/div[1]/div[1]/div[1]/div/lib-link-selector/div/div/div/a[3]')))

  # Go to month view (click monthly button)
  # Wait total 5 sec, poll 0.5 sec to get data from month view
  monthView = driver.find_element_by_xpath('//*[@id="inner-content"]/div[2]/div[1]/div[1]/div[1]/div/lib-link-selector/div/div/div/a[3]').click()

  WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="inner-content"]/div[1]/lib-city-header/div[1]/div/h1/span[1]')))

  time.sleep(2)

  # Get location to cross check
  weatherHistoryLocation = driver.find_element_by_xpath('//*[@id="inner-content"]/div[1]/lib-city-header/div[1]/div/h1/span[1]')

  print(weatherHistoryLocation.text.replace(' Weather History', ''))

  data_point = {
    'county_name': covid_data.values[county][1],
    'state': covid_data.values[county][2],
    'weather_station': weatherHistoryLocation.text.replace(' Weather History', '')
  }

  WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table')))
  driver.implicitly_wait(5)

  # Get avg temperature for the days in February
  for i in range(2, 28 + 2):
    date = driver.find_element_by_xpath(f'//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table/tbody/tr/td[1]/table/tr[{i}]/td')
    temp = driver.find_element_by_xpath(f'//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table/tbody/tr/td[2]/table/tr[{i}]/td[2]')

    print(f'_2_{date.text}_20 | {temp.text}')
    data_point[f'_2_{date.text}_20'] = temp.text

  time.sleep(2)

  # Select march and click view button, wait until table loads
  marchView = driver.find_element_by_xpath('//*[@id="inner-content"]/div[2]/div[1]/div[1]/div[1]/div/lib-date-selector/div/select[1]/option[3]').click()
  marchViewButton = driver.find_element_by_xpath('//*[@id="inner-content"]/div[2]/div[1]/div[1]/div[1]/div/lib-date-selector/div/input').click()
  WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table')))
  driver.implicitly_wait(5)

  # Get avg temperature for the days in March
  for i in range(2, 31 + 2):
    date = driver.find_element_by_xpath(f'//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table/tbody/tr/td[1]/table/tr[{i}]/td')
    temp = driver.find_element_by_xpath(f'//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table/tbody/tr/td[2]/table/tr[{i}]/td[2]')

    print(f'_3_{date.text}_20 | {temp.text}')
    data_point[f'_3_{date.text}_20'] = temp.text

  time.sleep(2)

  # Select march and click view button, wait until table loads
  aprilView = driver.find_element_by_xpath('//*[@id="inner-content"]/div[2]/div[1]/div[1]/div[1]/div/lib-date-selector/div/select[1]/option[4]').click()
  aprilViewButton = driver.find_element_by_xpath('//*[@id="inner-content"]/div[2]/div[1]/div[1]/div[1]/div/lib-date-selector/div/input').click()
  WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table')))
  driver.implicitly_wait(5)

  # Get avg temperature for the days in April
  for i in range(2, 30 + 2):
    date = driver.find_element_by_xpath(f'//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table/tbody/tr/td[1]/table/tr[{i}]/td')
    temp = driver.find_element_by_xpath(f'//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table/tbody/tr/td[2]/table/tr[{i}]/td[2]')

    print(f'_4_{date.text}_20 | {temp.text}')
    data_point[f'_4_{date.text}_20'] = temp.text

  covid_temperature = pandas.read_csv('covid-temperature.csv')
  covid_temperature = covid_temperature.append(data_point, ignore_index=True)
  covid_temperature.to_csv('covid-temperature.csv', index=False)

  print(f'{data_point["weather_station"]} for {data_point["county_name"]}, {data_point["state"]} saved ({county})')

  driver.get("https://www.wunderground.com/history")

  time.sleep(2)

assert "No results found." not in driver.page_source

driver.close()
