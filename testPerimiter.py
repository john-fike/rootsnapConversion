from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image

def extract_elements_with_name(node, target_name, scale, depth):
    if depth >= 2:
        return []

    elements = []
    for child in node.find_all(recursive=False):
        if child.name == target_name:
            elements.append(float(child.text)/scale) 
        elements.extend(extract_elements_with_name(child, target_name, scale, depth + 1))
    
    return elements

def buildBox(roots, scanID, xOffset, imWidth, imHeight):
    try:
        xTemp = []
        yTemp = []

        for root in roots:
            xTemp.append(extract_elements_with_name(root, 'X', imWidth, 0))
            yTemp.append(extract_elements_with_name(root, 'Y', imHeight, 0))
            subRoots = root.findAll('SubRoot')
            for subRoot in subRoots:
                xTemp.append(extract_elements_with_name(subRoot, 'X', imWidth, 0))
                yTemp.append(extract_elements_with_name(subRoot, 'Y', imHeight, 0))

        print(xTemp)
        print(yTemp)
        return dict(x=xTemp, y=yTemp)
    except Exception as e:
        print("An error occured while building boxes: ")



def display_boxes(image_path, boxDict):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load image.")
        return
    height, width = image.shape[:2]

    image = cv2.imread(image_path)

    # Loop through each box in the list
    for i in range(len(boxDict['x'])):
        for j in range(1, len(boxDict['x'][i]), 1):
            x1 = int(boxDict['x'][i][j-1] * width)
            y1 = int(boxDict['y'][i][j-1] * height)
            x2 = int(boxDict['x'][i][j] * width)
            y2 = int(boxDict['y'][i][j] * height)

            print("(" + str(x1) + "," + str(y1) + ")")
            image = cv2.line(image, (x1,y1), (x2,y2), (0,255,0))


    # Display the image with boxes
    cv2.imshow('Root Points', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def findXOffset(scan):
    try:
        offset = (scan.find('ImageOffset').find('X')).text
        if offset is None:
            return 0
        else:
            return float(offset)
    except Exception as e:
        print("An error occured while finding image X offset: ", e) 

        


with open('Barley_103_12Aug2020.rsp_clipped.xml','r') as f:
    data = f.read()
soup = BeautifulSoup(data, 'xml')
scans = soup.find_all('Scan')
roots = scans[3].find_all('Root')

image_path = 'Barley_103_D4_12Aug2020.PNG'

image = Image.open(image_path)
imWidth, imHeight = image.size


boxDict = buildBox(roots, 'scanID', 0, imWidth, imHeight)

image_path = './black.jpg'
display_boxes(image_path, boxDict)



