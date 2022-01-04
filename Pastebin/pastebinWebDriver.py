from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector 

with open("sites.txt") as f:
    for line in f:
        options = Options()
        options.headless = True

        driver = webdriver.Chrome(executable_path="C:/Users/talavahedi/Documents/Research/chromedriver", options=options)
        driver.get(line)
        print(line)

        title = driver.find_element_by_class_name('content__title').text
        if(title == 'Not Found (#404)'):
            print("post no longer available, passed")
            pass
        
        if(title == 'Warning - Potentially offensive content ahead!'):
            next_elem = driver.find_element_by_xpath('//*[@id="w0"]/div[2]/button')
            next_elem.click()
      
    
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'info-top')))
                
                # time.sleep(10)
                postTitle = driver.find_element_by_class_name('info-top').text
                # print(postTitle)

                username1 = driver.find_element_by_class_name('username').text
                username = username1.replace(" ", "")
                # print(username)

                postDate = driver.find_element_by_class_name('date').text
                # print(postDate)

                postViews1 = driver.find_element_by_class_name('visits').text
                postViews = postViews1.replace(" ", "")
                # print(postViews)

                postExpire1 = driver.find_element_by_class_name('expire').text
                postExpire = postExpire1.replace(" ", "")
                # print(postExpire)

                syntax1 = driver.find_element_by_css_selector('.left a').get_attribute('href')
                postSyntax = syntax1[29:]
                # print(postSyntax)

                postSize = driver.find_element_by_class_name('left').text
                # print(postSize)

                postContent = driver.find_element_by_class_name('textarea').text
                # print(postContent)
                driver.close()

            except:
                print("could not find contents")
                pass

            try:
                connection = mysql.connector.connect(
                    host="xxx.xxx.xxx.xxx", 
                    user="xxxx", 
                    password = "xxxx", 
                    database="xxxx", 
                    auth_plugin='xxx')
            except:
                print("No connection")
                pass


            mycursor = connection.cursor()
            sql = "INSERT INTO pastebin (postTitle, username, postDate, postViews, postExpire, postSyntax, postSize, postContent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (postTitle, username, postDate, postViews, postExpire, postSyntax, postSize, postContent) 
            mycursor.execute(sql, val)
            connection.commit()
            print(mycursor.rowcount, "Record inserted")

        
        

