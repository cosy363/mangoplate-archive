import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os

def mango(keyword):
    
    mangoplateurl = "https://www.mangoplate.com"
    option = Options()
    option.add_argument('--blink-settings=imagesEnabled=false') #브라우저에서 이미지 로딩을 하지 않습니다.

    browser = webdriver.Chrome(options=option)

    mangoData = pd.DataFrame(columns = ["title", "location", "estimation", "viewCount", "reviewCount"]) 

    end = 19

    for page in range(1, end): 
        mangoplateURL = "https://www.mangoplate.com/search/?keyword=" + keyword + "&page=" + str(page)
        browser.get(mangoplateURL)

        # search_button = browser.find_element_by_xpath("/html/body/div[2]/div/div/button[1]")
        # search_button.click()
        # time.sleep(20000)
        # browser.execute_script("closeAd()")
        
        # print(a)

        time.sleep(1)

        pageSource = BeautifulSoup(browser.page_source)
        infoList = pageSource.find_all("div", attrs = {"class" : "info"}) 
        # print(infoList)
        flag = True
        
        for info in infoList[0:20]:
            try:
                title = info.find("h2", attrs = {"class" : "title"}).get_text() 
                detailURL = info.find("a")["href"]

                # time.sleep(2)

                try:
                    estimation = info.find("strong").get_text()
                except:
                    estimation = info.find("strong").get_text() 
                
                if float(estimation) < 3.8:
                    flag = False
                    break


                viewCount = info.find("span", attrs = {"class" : "view_count"}).get_text()
                reviewCount = info.find("span", attrs = {"class" : "review_count"}).get_text()
                
                title = title.strip()
                detailURL = "https://www.mangoplate.com" + detailURL

                if estimation != '':
                    estimation = float(estimation)
                else:
                    estimation = 0

                viewCount = float("".join(viewCount.split(",")))
                reviewCount = float("".join(reviewCount.split(",")))

                # if estimation <= float(3.5):
                #     break

                # print(title,detailURL,estimation,viewCount,reviewCount)

                browser.get(detailURL)
                time.sleep(1)
                pageSource = BeautifulSoup(browser.page_source)
                # print(pageSource)
                try:
                    location = pageSource.find("span", attrs = {"class" : "Restaurant__InfoAddress--Text"}).get_text()
                except:
                    location = "주소없음"

                # infotable = pageSource.find("table", attrs= {"class" : "info"})
                # time.sleep(1000)

                try:
                    infotable = pageSource.find("table", attrs= {"class" : "info"})
                except:
                    infotable = pageSource.find("table", attrs= {"class" : "info no_menu"})

                # print(infotable)
                tbody = infotable.find("tbody")

                food_type = "없음"
                money_range = "없음"
                open_time = "없음"
                break_time = "없음"
                menus = []

                for tr in tbody.find_all("tr"):
                    title2 = tr.find("th").get_text()

                    if title2 == "음식 종류":
                        food_type = tr.find("td").get_text()
                    
                    if title2 == "가격대":
                        money_range = tr.find("td").get_text()
                    
                    if title2 == "영업시간":
                        open_time = tr.find("td").get_text()

                    if title2 == "휴일":
                        break_time = tr.find("td").get_text()

                    if title2 == "메뉴":
                        td = tr.find("td")
                        ul = td.find("ul")
                        li_list = ul.find_all("li")

                        for li in li_list:
                            a = li.find("span", attrs= {"class" : "Restaurant_Menu"}).get_text()
                            b = li.find("span", attrs= {"class" : "Restaurant_MenuPrice"}).get_text()
                            menus.append([a,b])


                # print(food_type,money_range,open_time,break_time,menus)

                # Metro 불러오기
                d = browser.find_element(By.XPATH, "/html/body/main")
                metro_station = d.get_attribute('data-metro_str')

                reviews = []

                # 리뷰정보 불러오기
                
                reviewpage = pageSource.find("section",attrs= {"class" : "RestaurantReviewList"})
                review_ul = reviewpage.find("ul",attrs= {"class" : "RestaurantReviewList__ReviewList"})
                review_list = review_ul.find_all("li",attrs= {"class" : "RestaurantReviewItem RestaurantReviewList__ReviewItem"})

                for reviewdata in review_list:
                    rating = reviewdata.find("span", attrs= {"class" : "RestaurantReviewItem__RatingText"}).get_text()
                    review = reviewdata.find("p", attrs= {"class" : "RestaurantReviewItem__ReviewText"}).get_text()
                    reviews.append([rating,review])
                    # print(rating,review)
                
                newData = {
                        "title" : [title], 
                        "location" : [location], 
                        "estimation" : [estimation], 
                        "viewCount" : [viewCount], 
                        "reviewCount" : [reviewCount],
                        "reviews" : [reviews],
                        "menus" : [menus],
                        "food_type" : [food_type],
                        "money_range" : [money_range],
                        "open_time" : [open_time],
                        "break_time" : [break_time],
                        "metro_station" : [metro_station]
                        } 
                
                newData = pd.DataFrame(newData)
                mangoData = pd.concat((mangoData, newData)).reset_index(drop = True)
                dest_name = keyword + ".csv"
                mangoData.to_csv(dest_name,sep=',',na_rep='NaN')
                # time.sleep(2000)
            except:
                None

        dest_name = keyword + ".csv"
        mangoData.to_csv(dest_name,sep=',',na_rep='NaN')
        
        if flag == False:
            break



f = open("real.csv","rt",encoding="utf-8")

while True:
    line = f.readline()
    if line == '':
        break
    line = line.replace("\n", "")
    print("현재는 " + line)
    mango(line)
    # mango("안국역")
