#!/bin/python

import requests
import os
import json
import sys
import argparse

f = open('./config.json', 'r')
settings = json.load(f.read())
api_key = settings['api_key']
temp_dir = settings['temp_dir']
save_dir = settings['save_dir']
payload = settings['payload']


def incrementIndex():
    inc = getCurrentIndex()+1
    f = open(temp_dir+"/index", "w")
    f.write(str(inc))


def getCurrentIndex():
    f = open(temp_dir+"/index")
    current = int(f.readline())
    f.close()
    if (current >= 24):
        current = 0
        getPapeList()
        f = open(temp_dir+"/index", 'w')
        f.write("0")
    return current


def getPapeList():
    response = requests.get('https://wallhaven.cc/api/v1/search',
                            params=payload)
    dictionary = response.json()
    f = open("/tmp/wallhaven_response", 'w')
    f.write(json.dumps(dictionary))


def getLink(index: int):
    if (not os.path.exists("/tmp/wallhaven_response")):
        getPapeList()
    dictionary = json.loads(open("/tmp/wallhaven_response", 'r').read())
    return dictionary['data'][index]['path']


def dlPape(link: str, filename: str):
    image = requests.get(link)
    f = open(filename, 'wb')
    f.write(image.content)


def setWallpaper(link: str):
    dlPape(link, "/tmp/lastpape")
    os.system("xwallpaper --zoom " + "/tmp/lastpape")
    incrementIndex()


def main():
    index = getCurrentIndex()
    if (len(sys.argv) != 1):
        if (sys.argv[1] == "s"):
            filename = os.path.split(getLink(index-1))
            dlPape(getLink(index-1), save_dir+filename[1])
            print("Pape saved to " + save_dir+filename[1])
    else:
        path = getLink(index)
        setWallpaper(path)


if __name__ == "__main__":
    main()
