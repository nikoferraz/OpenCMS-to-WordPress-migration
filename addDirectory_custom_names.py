# Created by Nick Ferraz
# See bottom comments for further details
from bs4 import BeautifulSoup
import os
topdir = input("Enter directory path:")
list_of_directories=[]
temp=""
def addDirectory(dirName, path):
    fullName = os.path.join(path, dirName)  
    if os.path.isfile(path+"\\index.html"):
        os.rename(path+"\\index.html", fullName+".html")
        print("Index file renamed")
        return str(dirName+".html")
    if dirName.lower() in ["images", "css", "media"]:
        print("CSS and Images directories will not be included.")
    else:
        markup = '<title>'+dirName+'</title>'
        soup = BeautifulSoup(markup, 'html.parser')
        with open(fullName+".html", 'w') as file:
            file.write(str(soup))
            file.close()
        return str(dirName+".html")
for dirpath, dirnames, files in os.walk(topdir):
    for name in dirnames:
       temp = addDirectory(name, dirpath+"\\"+name)
       if type(temp) == str and temp not in list_of_directories:
            list_of_directories.append(temp)
print(list_of_directories)
with open(".\\directory_list.txt", 'w') as file:
        file.write(", ".join(list_of_directories))
        file.close()
# ABOUT:       
# This script is meant to generate WordPress directories used 
# in conjunction with the HTML Import 2 plugin. 
# Since directories in WordPress are pages, the plugin
# asks for default directory names. This script works by 
# creating pages with title elements and names corresponding to their
# respective parent directory. 
# If there is an index.html file this will rename the file instead of 
# creating a new one.
# Additionally, the script will create a txt file at the toplevel
# containing a list of all directories generated. This list must 
# be used in the default directory field in the HTML Import 2 plugin