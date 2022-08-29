# A python script to keep GW2 ArcDPS updated

# Usage:
# Move the script, or the script-to-exe converted executable into the Guild Wars 2 installation folder
# Create a file named: gw_up.conf
# Write the full path of the Guild Wars 2 installation folder into that file, for me it is: C:\Program Files (x86)\Guild Wars 2
# From this point the script will take care of everything else, this is for my use only, was uploaded to github because I am lazy to store it anywhere else, and git is that easy to use...

# As for converting the script into an exe, I recommend auto-py-to-exe or the already built exe, if you are suspicious about it having something fishy coded into it, build it yourself
import requests
from bs4 import BeautifulSoup
import os

GW_PATH = "C:\Program Files (x86)\Guild Wars 2"
GW_CONFIG_PATH = GW_PATH+"\DU.conf"
DLL_WWW = "https://www.deltaconnected.com/arcdps/x64"
DLL_DIRECT_LINK = "https://www.deltaconnected.com/arcdps/x64/d3d11.dll"
GW_DLL_PATH = GW_PATH+"\d3d11.dll"
GW_EXECUTABLE_PATH = '"'+GW_PATH+'\Gw2-64.exe'+'" --maploadinfo'

headers = {
    'User-Agent' : 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.97 Mobile Safari/537.36',
}

def yes_file():
    CONFIG_FILE_CONTENT = open(GW_CONFIG_PATH).readline()
    current_date = getCurrentDateOfDll()
    if CONFIG_FILE_CONTENT == current_date:
        print("No update is needed")
    else:
        print("Update required")
        do_dll_update()


def do_dll_update():
    try:
        os.remove(GW_DLL_PATH)
    except:
        pass
    with open(GW_DLL_PATH,'wb') as out_file:
        content = requests.get(DLL_DIRECT_LINK,headers=headers,stream=True).content
        out_file.write(content)
        CONFIG_FILE_CONTENT = open(GW_CONFIG_PATH,'w')
        CONFIG_FILE_CONTENT.write(getCurrentDateOfDll())
        CONFIG_FILE_CONTENT.close()
        print("Config file for storing the last known update date is created")

def main():
    #################### READING THE MAIN CONFIG FILE ######################
    try:
        GW_PATH = open("gw_up.conf",'r').readline()
        print("Main config found")
    except:
        print("No config file named 'gw_up.conf' is found, this is important to get all the other files, and final execution properly set up inside the script, please create it, exiting")
        exit(0)
    ########################################################################
    try:
        open(GW_PATH + "\DU.conf")
        print("File exists")
        yes_file()
    except:
        print("No file")
        do_dll_update()
    os.system(GW_EXECUTABLE_PATH)

def getCurrentDateOfDll():
   response = requests.get(DLL_WWW, headers=headers)
   soup = BeautifulSoup(response.content, 'lxml')
   x = soup.select('#indexlist > tr.odd > td.indexcollastmod')[0].text
   return x

if __name__ == "__main__":
    main()