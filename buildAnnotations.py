from tqdm import tqdm
import extractRSPAnnotations
from bs4 import BeautifulSoup
import os
import glob
import cv2
import time
from PIL import Image, ImageDraw
from ultralytics import SAM
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
                    polyline = soup.new_tag("polyline", "", label = "root", source = "manual", occluded = "0", points = pointStr)
                    image.append(polyline)
            with open('./annotations.xml', 'w') as f:
                f.write(str(soup))
        except AttributeError as nf:
            print(" WARNING: could not find scan:" + scanDict[s]["scanID"])
        except Exception as e:
            print("An error occured while writing to CVAT annotation file:", e)


#this function builds box annotations for YOLOv8
def buildYOLOAnnotations(folderPath):
    print('Building YOLOv8 Segmentation Annotations')

    #get all xml files in folder 
    xmlFiles = glob.glob(os.path.join(folderPath, "*.rsp_clipped.xml"))
    for filePath in tqdm(xmlFiles):
        try:
            scanDict = extractRSPAnnotations.extractRootCoords(filePath) 
            for s in range(len(scanDict)):
                annotationOutputPath = './test/' + scanDict[s]["scanID"][:-4] + '.txt'
                with open(annotationOutputPath, 'w+') as f:
                    # print the size of the yoloboxes list in dictonary scanDict[s]
                    # print(len(scanDict[s]["YOLOPoints2"]))
                    for i in range(len(scanDict[s]["yoloPoints"])):                    
                            temp = ''.join(scanDict[s]["yoloPoints"][i])
                            f.write(temp + '\n')            
               
        except Exception as e:
            print("An error occured while writing to YOLOv8 annotation file:", e)




buildYOLOAnnotations('./rsp')
# buildCVATAnnotations('./rsp')