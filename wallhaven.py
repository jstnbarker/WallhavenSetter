#!/bin/python

import requests
import os
import json
import sys
import argparse

f = open('./config.json', 'r')
settings = json.loads(f.read())
api_key = settings['api_key']
temp_dir = settings['temp_dir']
save_dir = settings['save_dir']
payload = settings['payload']
setter = settings['setter']


def incrementIndex():
    inc = getCurrentIndex()+1
    f = open(temp_dir+"/index", "w")
    f.write(str(inc))


def getCurrentIndex():
    current = 0
    try:
        f = open(temp_dir+"/index")
        current = int(f.readline())
        f.close()
        if (current >= 24):
            current = 0
            getPapeList()
            raise Exception
    except (Exception):
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
    dlPape(link, temp_dir + "lastpape")
    os.system(setter + " " + temp_dir + "lastpape")
    incrementIndex()


def main():

    def savePape():
        filename = os.path.split(getLink(index-1))
        dlPape(getLink(index-1), save_dir+filename[1])
        print("Pape saved to " + save_dir+filename[1])

    index = getCurrentIndex()
    parser = argparse.ArgumentParser(
            prog=sys.argv[0],
            description="Sets x11 session wallpaper with Wallhaven API")
    parser.add_argument('-s', '--save',
                        action='store_true',
                        dest='save'
                        )
    parser.add_argument('--update',
                        action='store_true',
                        dest='update_database'
                        )
    args = parser.parse_args()
    if (args.save):
        savePape()
    if (args.update_database):
        getPapeList()
    if (len(sys.argv) == 1):
        path = getLink(index)
        setWallpaper(path)


if __name__ == "__main__":
    main()
