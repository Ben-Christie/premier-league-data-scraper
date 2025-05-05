from selenium import webdriver
from selenium.webdriver.common.by import By
from helper import csv_split
from fbref_scraper import fbref
from sofifa_scraper import sofifa
from transfermarkt_scraper import transfermarkt

# init web driver
driver = webdriver.Chrome()

# init players data dictionary
players = {}

# run scrapers and append data to players data dictionary
# fbref scraper is responsible for gathering initial dataset of players, without it running no scraper will be able to append data
fbref(players, driver)
sofifa(players, driver)
transfermarkt(players, driver)

# Close the webdriver instance
driver.quit()

# split into CSVs
csv_split(players)
