#Script to change dates from OpenCMS posts to WordPress friendly format 
# About:
# This script was developed to be used in conjunction with HTML Import 2 
# in order to import posts with the correct timestamp. 
# Choose the option of dating the posts with a custome field
# and select the tag p with id = "timestamp" in HTML Import 2 plugin
import os
import re
from bs4 import BeautifulSoup
def parseHTML(fileName, f):
    months = {"jan":"01","feb":"02","mar":"03","apr":"04","may":"05","jun":"06","jul":"07","aug":"08",
    "sep":"09","oct":"10","nov":"11","dec":"12"}
    try:
        with open(f,"r", encoding='utf-8', errors='ignore') as file:
            contents = file.read()
    except OSError:
        contents = ""
    soup = BeautifulSoup(contents,'html.parser')
    p = soup.find("p")
    published_date = ""
    try:
        published_date = p.text.replace(",","").lstrip().split(" ")
    except AttributeError:
        print("No p attribute")
    try:
        published_date[0] = months[published_date[0].lower()]
        published_date = BeautifulSoup("<p id=timestamp class='hidden'>"+published_date[2]+"-"+published_date[0]+"-"+published_date[1]+"</p>",'html.parser')
    except (IndexError, KeyError, UnicodeEncodeError):
        print("Error")
    colCenter = soup.find("div",{'id':'colCenter'})
    try:
        colCenter.append(published_date)
    except (AttributeError, TypeError):
        print("Error")
    file.close()
    soup = str(soup)
    with open(f, 'wb') as file:
        file.write(soup.encode('utf-8'))
        file.close()
# The top argument for walk
topdir = input("Enter directory path:")
# What will be logged
for dirpath, dirnames, files in os.walk(topdir):
    for name in files:
        if name.lower().endswith('.htm'):
        # Save to results string instead of printing
            try:
                print(os.path.join(dirpath, name))
                parseHTML(name, os.path.join(dirpath, name))
            except (UnicodeDecodeError, PermissionError, IOError) as err:
                print(err)
