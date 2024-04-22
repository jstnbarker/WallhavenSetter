#!/bin/python

import requests
import os
import json
import sys

last_pape_tracker = "/tmp/last_pape_tracker"
directory = "/tmp/wallpaper.from.wallhaven"


def incrementIndex():
    inc = getCurrentIndex()+1
    f = open(last_pape_tracker, "w")
    f.write(str(inc))


def getCurrentIndex():
    f = open(last_pape_tracker)
    current = int(f.readline())
    f.close()
    if (current >= 24):
        current = 0
        getPapeList()
        f = open(last_pape_tracker, 'w')
        f.write("0")
    return current


def getPapeList():
    payload = {'categories': '010',
               'atleast': '2560x1440',
               'sorting': 'random',
               'ratios': 'landscape',
               'purity': '110',
               }
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
    saveDir = "/home/jstn/img/walls/"
    index = getCurrentIndex()
    if (len(sys.argv) != 1):
        if (sys.argv[1] == "s"):
            filename = os.path.split(getLink(index-1))
            dlPape(getLink(index-1), saveDir+filename[1])
            print("Pape saved to " + saveDir+filename[1])
    else:
        path = getLink(index)
        setWallpaper(path)


if __name__ == "__main__":
    main()
