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
#days out to check schedule, keep this as 14 for now
days_out = 14

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-extensions")

#For linux:
#chrome_driver = os.path.dirname(os.path.realpath(__file__))+"\\Drivers\\linchromedriver"
chrome_driver = os.path.dirname(os.path.realpath(__file__))+'\\Drivers\\winchromedriver'


def get_dates():
	url = cfg.user['url']
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
	driver.implicitly_wait(10)
	for i in range(days_out):
		t = driver.find_element_by_xpath('//*[@id="column-scheduleShift-Row-'+str(i)+'"]/div').text
		if t != '':
			t = t.split('-')
			d = driver.find_element_by_xpath('//*[@id="column-Date-Row-'+str(i)+'"]/div').text.split(' ')[1]
			times[d] = t
	return times

def add_to_cal(dates):
	service = srv.getService()
	now = datetime.now()
	events_result = service.events().list(calendarId='primary', q = 'Work', timeMin=datetime.utcnow().isoformat() + 'Z', maxResults = days_out, singleEvents=True, orderBy='startTime').execute()
	events = events_result.get('items', [])
	
	for event in events:#remove events if they have been deleted/changed
		evdate = event['start'].get('dateTime')[::-1].split('-',1)[1][::-1]
		evdate = datetime.strptime(evdate, '%Y-%m-%dT%H:%M:%S')	
		for date, time in dates.items():
			date = datetime.strptime(date, '%m/%d')
			time = datetime.strptime(time[0], '%I:%M%p')
			if evdate.strftime('%m/%d') == date.strftime('%m/%d') and evdate.strftime('%I:%M%p') == time.strftime('%I:%M%p'):
				break
		else:
			to_be_del = event.get('id')
			service.events().delete(calendarId='primary', eventId=to_be_del).execute()
				

	for date, time in dates.items():#add work events
		st = datetime.strptime(time[0], '%I:%M%p')
		et = datetime.strptime(time[1], '%I:%M%p')
		sh,sm = st.hour, st.minute
		eh,em = et.hour, et.minute
		m,d = [int(z) for z in date.split('/')]
		start = datetime(now.year, m, d, sh, sm, 0, 0)
		end = datetime(now.year, m, d, eh, em, 0, 0)
		to_add = {
			'summary': cfg.user['work_title'],
			'location': cfg.user['work_address'],
			'description': cfg.user['work_description'],
			'start': {
				'dateTime': start.isoformat(),
				'timeZone': cfg.user['timezone'],
			},
			'end': {
				'dateTime': end.isoformat(),
				'timeZone': cfg.user['timezone'],
			}
		}
		for event in events:#make sure event isnt already created
			evdate = event['start'].get('dateTime')[::-1].split('-',1)[1][::-1]
			evdate = datetime.strptime(evdate, '%Y-%m-%dT%H:%M:%S')
			if evdate.strftime('%m-%d-%H') == start.strftime('%m-%d-%H'):
				break
		else:
			service.events().insert(calendarId='primary', body=to_add).execute()


if __name__ == "__main__":
	driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
	dates = get_dates()
	add_to_cal(dates)
	driver.close()