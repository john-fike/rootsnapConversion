
from tqdm import tqdm
import extractRSPAnnotations
from bs4 import BeautifulSoup
import os
import glob
from PIL import Image, ImageDraw
from ultralytics import SAM
from PIL import Image

#recusivley go through all root elements and extract roots, then subroots, then subroots of subroots... etc
def extractRootSubroots(node, target_name, depth):
    if depth >= 2:
        return []

    elements = []
    for child in node.find_all(recursive=False):
        if child.name == target_name:
            elements.append(float(child.text)) 
        elements.extend(extractRootSubroots(child, target_name, depth + 1))
    
    return elements

#use all roots, scan ID (this is also the image name), x offset, and image size. use to build dictionary
def buildDictionary(roots, scanID, xOffset, imgSize):
    #imgSize[0] imgSize[1] = width, height
    try:
        xRoots = []        
        yRoots = []

        #make a list of all x coordinates, and a list of all y coordinates
        for root in roots:
            xRoots.append(extractRootSubroots(root, 'X', 0))
            yRoots.append(extractRootSubroots(root, 'Y', 0))
            subRoots = root.findAll('SubRoot')
            for subRoot in subRoots:
                xRoots.append(extractRootSubroots(subRoot, 'X', 0))
                yRoots.append(extractRootSubroots(subRoot, 'Y', 0))
        #xRoots[i] and yRoots[i] contain the points for each root

        CVATPoints = []
        YOLOPoints = []
        YOLOBoxes  = []
        #grab one in every 10 x,y coord pair, make a 2D list of coord pairs
        #each row in list contains coords that correspond to a root
        for i in range(len(xRoots)):
            tempCVAT = []
            tempYOLO = []
            tempYOLOBoxes = []

            #------------------------------------------------------------------------------------------------------------poly line points
            # this iterates through all of these points and adds them to the tempCVAT and tempYOLO lists
            # as long as they are not in top corner (which is for some reason a problem)
            for j in range(0, len(xRoots[i])):
                if(xRoots[i][j]-xOffset > 10 or yRoots[i][j] > 10):
                    tempCVAT.append(str(xRoots[i][j]-xOffset) + "," + str(yRoots[i][j]) + ";")
                    #yolo points are scaled to a value 0-1 so that you can squish the image to 1:1 and reapply coords later 
                    tempYOLO.append(str((xRoots[i][j]-xOffset) / imgSize[0]) + " " + str((yRoots[i][j]) / imgSize[1]) + " ")
            #add polyline points if they have at least 2 points
            if(len(tempCVAT)>1):
                CVATPoints.append(tempCVAT)
                YOLOPoints.append(tempYOLO)

            #------------------------------------------------------------------------------------------------------------yolo boxes
            #find the x,y points for the center of the box, plus its width and heigh.
            #scale to 0-1 using image size so that you can squish the image to 1:1 and reapply coords later
            YOLO_box_x = (sum(xRoots[i]) / len(xRoots[i])) / imgSize[0]
            YOLO_box_y = (sum(yRoots[i]) / len(yRoots[i])) / imgSize[1]
            YOLO_box_width = (max(xRoots[i]) - min(xRoots[i])) / imgSize[0]
            YOLO_box_height = (max(yRoots[i]) - min(yRoots[i])) / imgSize[1]

            #add the box to the list of boxes IF it isn't too big or small
            # if(YOLO_box_width > 0.01 and YOLO_box_height > 0.01 and YOLO_box_width < 0.5 and YOLO_box_height < 0.5):       
            YOLOBoxes.append("0 " + str(YOLO_box_x) + " " + str(YOLO_box_y) + " " + str(YOLO_box_width) + " " + str(YOLO_box_height))
            # print("0 " + str(YOLO_box_x) + " " + str(YOLO_box_y) + " " + str(YOLO_box_width) + " " + str(YOLO_box_height))
 
        return dict(scanID = scanID, points = CVATPoints, yoloPoints = YOLOPoints, yoloBoxes = YOLOBoxes)
    except Exception as e:
        print("An error occured while building coordinate dictionary:", e)
        return None



#returns:
# a list of 4 dictionaries, each containing the scan name (ex. Barley_316_D4_12August2020.PNG) and a 2D array of points, where each row is a root 
#points are delimited by ',' and pairs by ';'
def extractRootCoords(filePath):
    try:
        with open(filePath,'r') as f:
            data = f.read()
        soup = BeautifulSoup(data, 'xml')
        scans = soup.find_all('Scan')

        fileName = f.name
        DIndex = fileName.find("_") + 5
        scanID_0 = fileName[6:DIndex] + "D1_" + fileName[DIndex:-15] + "PNG"
        scanID_1 = fileName[6:DIndex] + "D2_" + fileName[DIndex:-15] + "PNG"
        scanID_2 = fileName[6:DIndex] + "D3_" + fileName[DIndex:-15] + "PNG"
        scanID_3 = fileName[6:DIndex] + "D4_" + fileName[DIndex:-15] + "PNG"

        imageFolderPath = './gimpRepair/BarleyAdjustedImages/'
        
        #if more than 4 scans are detected in the XML data, nothing happens. 
        #you will have to go through and manually eradicate the extra data
        #tip: the raw rsp data has everything it contains listed at the bottom of the file
        if len(scans) == 4:      
                roots = scans[0].find_all('Root')
                scanDict_0 = buildDictionary(roots, scanID_0, findXOffset(scans[0]), getImgSize(imageFolderPath + scanID_0))

                roots = scans[1].find_all('Root')
                scanDict_1 = buildDictionary(roots, scanID_1, findXOffset(scans[1]), getImgSize(imageFolderPath + scanID_1))

                roots = scans[2].find_all('Root')
                scanDict_2 = buildDictionary(roots, scanID_2, findXOffset(scans[2]), getImgSize(imageFolderPath + scanID_2))

                roots = scans[3].find_all('Root')
                scanDict_3 = buildDictionary(roots, scanID_3, findXOffset(scans[3]), getImgSize(imageFolderPath + scanID_3))

                return [scanDict_0, scanDict_1, scanDict_2, scanDict_3]
    
        else:
            raise ValueError("Incorrect number of scans in file: ")
    except Exception as e:
        print("An error occured while extracting root coordinates:", e)
        return None        



#returns height and width of image
def getImgSize(imgPath):
    try:
        with Image.open(imgPath) as img:
            width, height = img.size
            return width, height
    except IOError as e:
        print(f"Error opening the image: {e}")
        return None

#some rsp files have an x offset value that shifts the points, but the y offset is zero
#i'd reccomend printing the y offset of your files if you are having issues with offset 
def findXOffset(scan):
    try:
        offset = (scan.find('ImageOffset').find('X')).text
        if offset is None:
            return 0
        else:
            return float(offset)
    except Exception as e:
        print("An error occured while finding image X offset: ", e)

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
                    print(len(scanDict[s]["yoloBoxes"]))
                    for i in range(len(scanDict[s]["yoloBoxes"])):                    
                            temp = ''.join(scanDict[s]["yoloBoxes"][i])
                            f.write(temp + '\n')            
               
        except Exception as e:
            print("An error occured while writing to YOLOv8 annotation file:", e)

