#Created by Nick Ferraz
#Last edited by Nick Ferraz on 5/12/2017
#See comments at the bottom for details
import os
import re
import sys
from bs4 import BeautifulSoup
topdir = input("Enter directory name:")
URL = input("Please enter the site URL, including backslash at the end:")
def updateLink(link):
    pattern_1 =re.compile(r"library\.illinois\.edu\/")
    pattern_2 = re.compile(r"http\:\/\/")
    pattern_3 = re.compile(r"www\.")
    pattern_4 = re.compile(r'illinois\.edu')
    pattern_5 = re.compile(r'mailto')
    result=""
    media_file = True
    if re.match("\.html", link):
        media_file = False
    #Is it an absolute/relative path to this website?
    if pattern_1.match(link) or not ( pattern_2.match(link) or  pattern_3.match(link)) and not  pattern_5.match(link):
        result = re.search('(\w+\.\w+)$', link)
        #Clean up link
        link = re.sub('.html', "", link)
        link = re.sub('\/export', "", link)
        #Is it a media file?
        if media_file and not pattern_4.match(str(result)) :
            try: 
                link=URL+str(result.group(0))
            except (AttributeError, IndexError) as err:
                print(err)
    return link
def removeEl(el):
    try:
        soup.el.decompose()
    except AttributeError:
        print("No "+el+" element to remove.")
def parseHTML(fileName, dirpath, remLB):
    f = os.path.join(dirpath, fileName)
    try:
        with open(f,"r", encoding='utf-8', errors='ignore') as file:
            contents = file.read()
    except OSError:
        contents = ""
    soup = BeautifulSoup(contents,'html.parser')
    try: 
        colCenter = soup.find("div",{'id':'colCenter'})
        images = colCenter.find_all('img')
         # Add a null value alt attribute if alt is not found
        for image in images:
        #Update link for image tags
            try:
                image['src']=updateLink(image['src'])
            except (KeyError, TypeError) as err:
                    print(err)
            try:
                image['alt']
            except (KeyError):
                    image['alt']=""
            except (TypeError) as err:
                print(err)
    except AttributeError as err:
        print(err)
    post = False
    try:
        if soup.find("meta",{'name':'post'}) is not None:
            post = True
    except AttributeError:
        print("Page type element.")
    except (AttributeError, TypeError) as err:
        print(err)
    #Update link for anchor tags
    try:
        links = colCenter.find_all('a')
        for link in links:
            try:
                print ("Link to update is: "+link['href'])
                link['href']=updateLink(link['href'])
            except KeyError as err:
                print(err)
    except AttributeError as err:
        print(err)
    #Remove "clearer" class <p> 
    try:
        p_clearer = colCenter.find("p",{'class':'clearer'})
        p_clearer.decompose()
    except AttributeError:
        print("No element with class clearer to remove.")
    #Remove h1 element
    try:
        h1 = str(colCenter.h1)
        soup.h1.decompose()
    except AttributeError as err:
        print(err)
    #Remove id="breadcrumb" div
    try:
        breadcrumb = colCenter.find("div",{'id':'breadcrumb'})
        breadcrumb.decompose()
    except AttributeError:
        print("No breadcrumb div to remove.")
    title = soup.title
    file.close()
    try:
        content = ""
        for i in colCenter:
            content += str(i)
        content = str(title)+"<div id='colCenter'>"+BeautifulSoup(content,'html.parser').prettify()+"</div>"
        if remLB:
            content=content.replace("\n", "").replace("\r","")
    except AttributeError:
        print("Attribute Error: No attribute to modify")
    except TypeError:
        print("'NoneType' object is not iterable")
    base = os.path.splitext(f)[0]
    fileName=base+".html"
    if post:
        fileName = base+".htm"
        os.rename(f, fileName)
    with open(fileName, 'wb') as file:
        file.write(content.encode('utf-8'))
        file.close()
#Dir tree walk
remLineBreaks=True
print("Linebreaks will be removed by default. Would like to keep them?")
keepLineBreaks=input("Yes, keep linebreaks.(y/yes)").lower()
if keepLineBreaks=="y" or keepLineBreaks=="yes":
    remLineBreaks=False
# What will be logged
for dirpath, dirnames, files in os.walk(topdir):
    for name in files:
        if name.lower().endswith('.html') or name.lower().endswith('.htm'):
        # Save to results string instead of printing
            try:
                print(os.path.join(dirpath, name))
                parseHTML(name, dirpath, remLineBreaks)
            except (UnicodeDecodeError, PermissionError, IOError) as err:
                print(err)
#About this parser
# This script is part of a series of other mirgration scripts developed for the 
# OpenCMS to WordPress migration at the UofI Urbana-Champaing library

# The script handles the following:
# 1) Cleaning HTML files from the previous CRM to remove uncessary/depracted elements
# 2) Change post type files to .htm extension to distinguish them from page files 
# 3) General parsing to allow the files to be used in conjunction with the WordPress HTML Import 2 plugin

