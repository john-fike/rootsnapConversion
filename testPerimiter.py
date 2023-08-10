from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import cv2


def buildBox(roots, scanID, xOffset, imWidth, imHeight):
    xTemp = []
    yTemp = []
    w = []
    h = []
    y = []
    x = []

    for root in roots:
        xVals = root.find_all('X')  
        yVals = root.find_all('Y')
        xTemp.append([float(xVal.text)/imWidth for xVal in xVals])
        yTemp.append([float(yVal.text)/imHeight for yVal in yVals])

    for i in range(len(xTemp)):
        x.append(sum(xTemp[i]) / len(xTemp[i]))
        y.append(sum(yTemp[i])  / len(yTemp[i]))
        w.append(max(xTemp[i]) - min(xTemp[i]))
        h.append(max(yTemp[i]) - min(yTemp[i]))

        
    return dict(x=x, y=y, w=w, h=h)



def display_boxes(image_path, boxDict):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load image.")
        return
    height, width = image.shape[:2]

    # Loop through each box in the list
    for i in range(len(boxDict['x'])):
        # x = boxDict['x'][i] * width
        # y = boxDict['y'][i] * height
        # w = boxDict['w'][i] * width
        # h = boxDict['h'][i] * height

        # x1 = int(x - w / 2)
        # y1 = int(y - h / 2)
        # x2 = int(x + w / 2)
        # y2 = int(y + h / 2)

        x = int(boxDict['x'][i] * width)
        y = int(boxDict['y'][i] * height)

        # Draw the box on the image
        # cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        image[y, x] = (0, 255, 0)


    # Display the image with boxes
    cv2.imshow('Image with Boxes', image)
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

        
image_path = './Barley_101_D1_10Aug2020_PNG.rf.6ba32f3df4fb09ad4af05eacb35af025.jpg'


with open('Barley_101_10Aug2020.rsp_clipped.xml','r') as f:
    data = f.read()
soup = BeautifulSoup(data, 'xml')
scans = soup.find_all('Scan')
roots = scans[0].find_all('Root')

image = cv2.imread(image_path)
if image is None:
    print("Error: Unable to load image.")

imWidth, imHeight = image.shape[:2]

boxDict = buildBox(roots, 'scanID', 0, imWidth, imHeight)



display_boxes(image_path, boxDict)


# image_path = './Screenshot 2023-08-08 122720.jpg'
# image = cv2.imread(image_path)
# if image is None:
#     print("Error: Unable to load image.")


