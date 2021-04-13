#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

if len(sys.argv) < 3:
    print("usage: python3 m3u_to_channels.py infile.m3u outfile.txt")
    sys.exit() 
else:
    text = open(sys.argv[1], "r").read()
    chList = []
    urlList = []
    mlist = text.splitlines()

    for line in mlist:
        if line.startswith("#EXTINF"):
            ch = line.partition('tvg-name="')[2].partition('" ')[0]
            if ch == "":
                ch = line.partition(',')[2]
            chList.append(ch)
        if line.startswith("http"):
            urlList.append(line)

    with open(sys.argv[2], "w") as f:
        for x in range(len(chList)):
            if not "***" in chList[x]:
                f.write(f"{chList[x].replace('Pluto ', '').replace(' Made In Germany', '')},{urlList[x]}\n")
                
    f.close()
