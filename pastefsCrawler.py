import scrapy
import bs4
from bs4 import BeautifulSoup
import os
import glob
import io
import mysql.connector

class pastefs(scrapy.Spider):
    name = "pastefs"

    def start_requests(self):
        allowed_domains = ['pastefs.com']
        start_urls = []
        start_url = 'https://pastefs.com/pid/'
        for i in range(245000, 251039):
            start_urls.append(start_url + str(i))

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = response.url.replace("https://pastefs.com/pid/", "").replace("/", "-") + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
            with io.open(filename, "r", encoding="utf-8", errors = "ignore") as f:
                contents = f.read()
                post = bs4.BeautifulSoup(contents, features='lxml')
            
                try:
                    username = post.find('div', {'class': 'info'}).find('a').get_text()
                    # print(username)

                    postDate = post.find('div', {'class': 'info'}).find('date').get_text().strip()
                    # print(postDate)

                    postDetails1 = post.find('ul', {'class': 'pastes-list'}).find('li').get_text()
                    spaces_list = postDetails1.split(' ')

                    postViews = spaces_list[2].strip()
                    postType = spaces_list[3].strip()
                    # print(postType)
                    # print(postViews)

                    postContent1 = post.find('div', {'id': 'output_area'}).find('ol').get_text()
                    postContent = postContent1.replace('"', '')
                    # print(postContent)
                
                except:
                    print("Could not find content")
                    pass

                try:
                    connection = mysql.connector.connect(
                        host="xxx.xxx.xxx.xxx", 
                        user="xxxx", 
                        password = "xxxx", 
                        database="xxxx", 
                        auth_plugin='xxx')
                except (mysql.connector.errors.IntegrityError, mysql.connector.error.DatabaseError, mysql.connector.errors.OperationalError):
                    print("No connection")
                    pass

                mycursor = connection.cursor()
                sql = "INSERT INTO pastefs (username, postDate, postViews, postType, postContent) VALUES (%s, %s, %s, %s, %s)"
                val = (username, postDate, postViews, postType, postContent) 
                mycursor.execute(sql, val)
                connection.commit()
                print(mycursor.rowcount, "Record Inserted")

        #Deletes the file once it's put it in the database
        os.remove(filename)
        print("File successfully deleted")
