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
import configparser

config = configparser.ConfigParser()




GW_PATH = "C:\Program Files (x86)\Guild Wars 2"
GW_CONFIG_PATH = GW_PATH+"\gw2_arc_up.conf"
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
    if config['MAIN']['last_updated'] == current_date:
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
        config['MAIN']['last_updated'] = getCurrentDateOfDll()
        with open(GW_CONFIG_PATH,'w') as file:
            config.write(file)
        print("Update done and a config file for storing the last known update date is created")

def main():
    #################### READING THE MAIN CONFIG FILE ######################
    if len(config.read('gw2_arc_up.conf')) < 1:
        print("Config file could not be found, or invalid, please use the config template from github for modification")
    else:
        print("Config file found, and seems valid")
    ########################################################################
    try:
       open(GW_PATH +"\gw2_arc_up.conf")
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