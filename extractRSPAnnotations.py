from bs4 import BeautifulSoup
from PIL import Image



#----------------------------------------------------------------------------------------
def buildDictionary(roots, scanID, xOffset, imgSize):
    try:
        xRoots = []        
        yRoots = []
        CVATPoints = []
        YOLOPoints = []

        for root in roots:
            xVals = root.find_all('X')  
            yVals = root.find_all('Y')
            xRoots.append([float(xVal.text) for xVal in xVals])
            yRoots.append([float(yVal.text) for yVal in yVals])

        for i in range(len(xRoots)):
            tempCVAT = []
            tempYOLO =[]
            for j in range(0, len(xRoots[i]), 10):
                if(xRoots[i][j]-xOffset > 10 or yRoots[i][j] > 10):
                    tempCVAT.append(str(xRoots[i][j]-xOffset) + "," + str(yRoots[i][j]) + ";")
                    tempYOLO.append(str((xRoots[i][j]-xOffset) / imgSize[0]) + " " + str((yRoots[i][j]) / imgSize[1]) + " ")
            if(len(tempCVAT)>3):
                CVATPoints.append(tempCVAT)
                YOLOPoints.append(tempYOLO)
        

        return dict(scanID = scanID, points = CVATPoints, yoloPoints = YOLOPoints)
    except Exception as e:
        print("An error occured while building coordinate dictionary:", e)
        return None



#returns a list of 4 dictionaries, each containing the scan name (ex. Barley_316_D4_12August2020.PNG) 
#and a 2D array of points, where each row is a root 
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

def getImgSize(imgPath):
    try:
        with Image.open(imgPath) as img:
            width, height = img.size
            return width, height
    except IOError as e:
        print(f"Error opening the image: {e}")
        return None

#----------------------------------------------------------------------------------------
def findXOffset(scan):
    try:
        offset = (scan.find('ImageOffset').find('X')).text
        if offset is None:
            return 0
        else:
            return float(offset)
    except Exception as e:
        print("An error occured while finding image X offset: ", e)
