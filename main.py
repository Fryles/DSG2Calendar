from selenium import webdriver
import sys,os,time
import config as cfg
username = cfg.kronos.user
password = cfg.kronos.password


chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920x1080")

#For linux:
#chrome_driver = os.path.dirname(os.path.realpath(__file__))+"\\Drivers\\linchromedriver"
chrome_driver = os.path.dirname(os.path.realpath(__file__))+'\\Drivers\\winchromedriver'


def get_dates():
	url = 'https://workforcemobile.dcsg.com/wfc/logon'
	driver.get(url)
	driver.find_element_by_id('username').send_keys()



if __name__ == "__main__":
	driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
	get_dates()
	#driver.close()