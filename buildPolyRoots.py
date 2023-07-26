import extractRSProots
from bs4 import BeautifulSoup

import os
import glob

folderPath = './'

rspFiles = glob.glob(os.path.join(folderPath, "*.rsp"))


xmlFiles = glob.glob(os.path.join(folderPath, "*.rsp_clipped.xml"))

for filePath in xmlFiles:
    try:
        scanDict = extractRSProots.extractRootCoords(filePath) 

        with open('./testCVATAnnotations.xml','r') as f:
            data = f.read()
        soup = BeautifulSoup(data, 'xml')

        for s in range(len(scanDict)):
            for i in range(len(scanDict[s]["points"])):
                print(scanDict[s]["scanID"])
                image = soup.find("image", attrs = {'name':scanDict[s]["scanID"]})
                # print(image)
                pointStr = ''.join(scanDict[s]["points"][i])
                pointStr = pointStr[:-1]
                polyline = soup.new_tag("polyline", "\n", label = "root", source = "manual", occluded = "0", points = pointStr)
                image.append(polyline)
        with open('./testCVATAnnotations.xml', 'w') as f:
            f.write(str(soup))
    except AttributeError as nf:
        print("Could not find scan:" + scanDict[s]["scanID"])
    except Exception as e:
        print("An error occured while writing to CVAT annotation file:", e)



