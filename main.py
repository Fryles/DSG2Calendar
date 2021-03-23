from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import sys,os,time,pytz
from datetime import datetime
import config as cfg
import Service as srv
username = cfg.kronos['user']
password = cfg.kronos['password']
#days out to check schedule, keep this as a const for now..
days_out = 14

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920x1080")

#For linux:
#chrome_driver = os.path.dirname(os.path.realpath(__file__))+"\\Drivers\\linchromedriver"
chrome_driver = os.path.dirname(os.path.realpath(__file__))+'\\Drivers\\winchromedriver'


def get_dates():
	url = 'https://workforcemobile.dcsg.com/wfc/logon'
	driver.get(url)
	driver.find_element_by_id('username').send_keys(username)
	driver.find_element_by_id('passInput').send_keys(password)
	driver.find_element_by_id('loginSubmit').click()
	
	#this is the xpath for the button to bring up the timecard
	tcbtn = '/html/body/krn-app/krn-navigator-container/ui-view/krn-workspace-manager-container/krn-workspace/krn-related-items/div/ul/li[3]/div/div'
	WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, tcbtn)))
	driver.find_element_by_xpath(tcbtn).click()
	#need to switch to widget iframe for getting schedule dates
	driver.switch_to.frame('widgetFrame2299')
	times = {}#dict with date as the keys and arr of times as the values
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'column-scheduleShift-Row-0')))
	driver.find_element_by_xpath('//*[@id="context"]/section/div/div/div[1]/div/div[1]/button').click()
	driver.find_element_by_xpath('//*[@id="context"]/section/div/div/div[1]/div/div[1]/ul/li[14]').click()
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'column-scheduleShift-Row-14')))
	for i in range(days_out):
		t = driver.find_element_by_xpath('//*[@id="column-scheduleShift-Row-'+str(i)+'"]/div').text
		if t != '':
			t = t.split('-')
			d = driver.find_element_by_xpath('//*[@id="column-Date-Row-'+str(i)+'"]/div').text.split(' ')[1]
			times[d] = t
	print(times)
	return times

def add_to_cal(dates):
	service = srv.getService()
	now = datetime.now()
	for date, time in dates.items():
		st = datetime.strptime(time[0], '%I:%M%p')
		et = datetime.strptime(time[1], '%I:%M%p')
		sh,sm = st.hour, st.minute
		eh,em = et.hour, et.minute
		m,d = [int(z) for z in date.split('/')]
		start = datetime(now.year, m, d, sh, sm, 0, 0).isoformat()
		end = datetime(now.year, m, d, eh, em, 0, 0).isoformat()
		event = {
			'summary': 'Work',
			'location': '231 W Esplanade Dr, Oxnard, CA 93036',
			'description': 'Building bikes...',
			'start': {
				'dateTime': start,
				'timeZone': 'America/Chicago',#this is so hacky but its fine for now
			},
			'end': {
				'dateTime': end,
				'timeZone': 'America/Chicago',#this is so hacky but its fine for now
			}
		}
		event = service.events().insert(calendarId='primary', body=event).execute()


if __name__ == "__main__":
	driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
	dates = get_dates()
	add_to_cal(dates)
	#driver.close()