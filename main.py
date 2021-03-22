from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import sys,os,time
import config as cfg
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




if __name__ == "__main__":
	driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
	get_dates()
	#driver.close()