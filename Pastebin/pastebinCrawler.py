import scrapy
import bs4
from bs4 import BeautifulSoup
import os
import glob
import io
import mysql.connector

class pastebin(scrapy.Spider):
    name = "pastebin"
    allowed_domains = ['pastebin.com']

    def start_requests(self):
        openSites = open('oneMoreTime.txt', "r")
        urls = openSites.read().split()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = response.url.replace("https://pastebin.com/", "").replace("/", "-") + '.html'
        filename1 = response.url
        with open(filename, 'wb') as f:
            f.write(response.body)
            with io.open(filename, "r", encoding="utf-8", errors = "ignore") as f:
                contents = f.read()
                post = bs4.BeautifulSoup(contents, features='lxml')

            smartFilter = post.find('div', {'class': 'content__title'}).get_text()
            if(smartFilter == 'Warning - Potentially offensive content ahead!'):
                print("Button Found")
                button_variable = open("oneLastTimeButtons.txt", 'a')
                button_variable.write(filename1 + '\n')
            
            else:  
                try:
                    postTitle = post.find('div', {'class': 'info-top'}).get_text()
                    # print(postTitle)

                    username1 = post.find('div', {'class': 'username'}).get_text()
                    username = username1.replace(" ", "")
                    # print(username)

                    postDate = post.find('div', {'class': 'date'}).get_text()
                    # print(postDate)

                    postViews1 = post.find('div', {'class': 'visits'}).get_text()
                    postViews = postViews1.replace(" ", "")
                    # print(postViews)

                    postExpire1 = post.find('div', {'class': 'expire'}).get_text()
                    postExpire = postExpire1.replace(" ", "")
                    # print(postExpire)

                    syntax = post.find('div', {'class': 'left'}).get_text().strip()
                    # print(Syntax)

                    rev_postSyntax = syntax[::-1]
                    position1 = (rev_postSyntax.find(" "))
                    position2 = (rev_postSyntax.find(" ", position1 + 1))
                    rev_syntax = rev_postSyntax[position2:]
                    rev_size = rev_postSyntax[0:position2]
                    postSyntax = rev_syntax[::-1]
                    # print(postSyntax)
                    postSize = rev_size[::-1]
                    # print(postSize)
                    
                    postContent = post.find('textarea', {'class': 'textarea'}).get_text()
                    # print(postContent)
                except:
                    print("post not found")
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
                sql = "INSERT INTO pastebin (postTitle, username, postDate, postViews, postExpire, postSyntax, postSize, postContent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (postTitle, username, postDate, postViews, postExpire, postSyntax, postSize, postContent) 
                mycursor.execute(sql, val)
                connection.commit()
                print(mycursor.rowcount, "Record Inserted")

        os.remove(filename)
        print("File successfully deleted")
