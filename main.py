import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os

# f = open("real.csv","rt",encoding="utf-8")
# rdr = csv.reader(f)

csv = pd.read_csv('real.csv',
                  names=['number',
                         'title',
                         'location',
                         'estimation',
                         'viewCount',
                         'reviewCount',
                         'reviews',
                         'menus',
                         'food_type',
                         'money_range',
                         'open_time',
                         'break_time',
                         'metro_station'
                         'success'], 
                  encoding='utf-8')

print(csv)