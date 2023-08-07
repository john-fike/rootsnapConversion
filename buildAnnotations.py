from tqdm import tqdm
import extractRSPAnnotations
from bs4 import BeautifulSoup

import os
import glob

##path to file containing rsp. extracted xml will be put here as well
folderPath = './rsp/'


def buildCVATAnnotations(folderPath):
    xmlFiles = glob.glob(os.path.join(folderPath, "*.rsp_clipped.xml"))
    
    foundImageCounter = 0
    foundImageList = []

    missingImageCounter = 0
    missingImageList = []

    missing = 0
    
    for filePath in tqdm(xmlFiles):
        try:
            scanDict = extractRSPAnnotations.extractRootCoords(filePath) 
            with open('annotations.xml','r') as f:
                data = f.read()
            soup = BeautifulSoup(data, 'xml')

            for s in range(len(scanDict)):
                for i in range(len(scanDict[s]["points"])):
                    image = soup.find("image", attrs = {'name':scanDict[s]["scanID"]})
                    pointStr = ''.join(scanDict[s]["points"][i])
                    pointStr = pointStr[:-1]
                    polyline = soup.new_tag("points", "", label = "root", source = "manual", occluded = "0", points = pointStr)
                    try:
                        image.append(polyline)
                    except AttributeError as e:
                        missing = 1
                        pass
            if(missing == 1):
                print("WARNING: Could not find image: " + scanDict[s]["scanID"])
                missing = 0
                missingImageCounter += 1
                missingImageList.append(f.name)
            else:
                foundImageCounter += 1
                foundImageList.append(f.name)
            with open('./annotations.xml', 'w') as f:
                f.write(str(soup))
        except Exception as e:
            print("An error occured while writing to CVAT annotation file:", e)

    with open('./report.txt', 'w') as rep:
        rep.write("MISSING: \n")
        for miss in missingImageList:
            rep.write(miss)
        rep.write("FOUND: \n")
        for found in foundImageList:
            rep.write(found)

def buildYOLOAnnotations(folderPath):
    print('Building YOLOv8 Segmentation Annotations')

    xmlFiles = glob.glob(os.path.join(folderPath, "*.rsp_clipped.xml"))
    for filePath in tqdm(xmlFiles):
        try:
            scanDict = extractRSPAnnotations.extractRootCoords(filePath) 
            for s in range(len(scanDict)):
                with open('./yolo/images/' + scanDict[s]["scanID"][:-4] + '.txt', 'w') as f:
                    f.truncate(0)
                    f.close
                for i in range(len(scanDict[s]["points"])):                    
                     with open('./yolo/images/' + scanDict[s]["scanID"][:-4] + '.txt', 'a') as f:
                        temp = ''.join(scanDict[s]["yoloPoints"][i])
                        f.write('0 ' + temp + '\n')                    
               
        except Exception as e:
            print("An error occured while writing to YOLOv8 annotation file:", e)
        


buildYOLOAnnotations('./rsp')
# buildCVATAnnotations('./rsp')