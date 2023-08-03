from tqdm import tqdm
import extractRSProots
from bs4 import BeautifulSoup

import os
import glob

##path to file containing rsp. extracted xml will be put here as well
folderPath = './rsp/'

## grab all rsp files and convert them to xml
# rspFiles = glob.glob(os.path.join(folderPath, "*.rsp"))
# for filePath in rspFiles:
#     extractRSProots.convertRSPtoXML(filePath)

#grab all the xml files you just made and create dictionaries with 
#image name and associated roots
xmlFiles = glob.glob(os.path.join(folderPath, "*.rsp_clipped.xml"))
missingImageCounter = 0
missingImageList = []
for filePath in tqdm(xmlFiles):
    # print("Inserting polylines...")
    try:
        scanDict = extractRSProots.extractRootCoords(filePath) 
        with open('annotations.xml','r') as f:
            data = f.read()
        soup = BeautifulSoup(data, 'xml')

        for s in range(len(scanDict)):
            for i in range(len(scanDict[s]["points"])):
                image = soup.find("image", attrs = {'name':scanDict[s]["scanID"]})
                pointStr = ''.join(scanDict[s]["points"][i])
                pointStr = pointStr[:-1]
                polyline = soup.new_tag("points", "", label = "root", source = "manual", occluded = "0", points = pointStr)
                image.append(polyline)
        with open('./annotations.xml', 'w') as f:
            f.write(str(soup))
    except AttributeError as nf:
        print("WARNING: could not find scan:" + scanDict[s]["scanID"])
        print("Total missing scans: " + missingImageCounter)
    except Exception as e:
        print("An error occured while writing to CVAT annotation file:", e)



