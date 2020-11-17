from selenium import webdriver
import os

browser = webdriver.Chrome(os.path.join(os.path.dirname(__file__), 'bin/chromedriver'))
browser.get('http://localhost:8000')

assert browser.page_source.find('install')