from selenium import webdriver
from selenium.webdriver.common.by import By
from helper import csv_split
from fbref_scraper import fbref
from sofifa_scraper import sofifa

# init web driver
driver = webdriver.Chrome()

# init players data dictionary
players = {}

# run scrapers and append data to players data dictionary
fbref(players, driver)
sofifa(players, driver)

# Close the webdriver instance
driver.quit()

# split into CSVs
csv_split(players)
