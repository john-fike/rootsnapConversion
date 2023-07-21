import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

import os
import glob

#########################################################################################
#####################convert RSP file to XML#############################################
#remove jpg binary data, isolate xml metadata containing root annotations and save them to [filename]_clipped
#########################################################################################
def convertRSPtoXML(inputFile):

    outputFilepath = ".\\" + inputFile + "_clipped.xml"

    print("Loading RSP file...")
    with open(inputFile, "r", encoding = "latin-1") as f:
        data = f.read()
    

    clippedData = data[data.index('<ProjectXML') : data.index('</ProjectXML')].strip()


    with open(outputFilepath, 'w') as oup:
        oup.write(clippedData)


convertRSPtoXML('Barley_101_10Aug2020.rsp')

