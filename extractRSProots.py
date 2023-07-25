import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

import os
import glob

##########################################################################################
#use this to extract xml from rsp files and build dictionaries with root



#----------------------------------------------------------------------------------------
# convert RSP file to XML
# remove jpg binary data, isolate xml metadata containing root annotations and save them to [filename]_clipped
def convertRSPtoXML(filePath):
    print("Extracting metadata for " + filePath)
    try:
        outputFilepath = ".\\" + filePath + "_clipped.xml"

        print("Loading RSP file...")
        with open(filePath, "r", encoding = "latin-1") as f:
            data = f.read()
        
        #extract metadata
        clippedData = data[data.index('<ProjectXML') : data.index('</ProjectXML')].strip()

        soup = BeautifulSoup(clippedData, 'xml')

        with open(outputFilepath, 'w') as oup:
            oup.write(clippedData)
    except Exception as e:
        print(f"Error while processing {filePath}: {e}")
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
#find an element nested in another element
def findNestedElements(soup, parent_element_name, child_element_name):
    try:
        # Find all occurrences of the parent element
        parent_elements = soup.find_all(parent_element_name)

        # Find all child elements with a different name, nested within each parent element
        results = []
        for parent_element in parent_elements:
            child_elements = parent_element.find_all(child_element_name)
            if child_elements:
                results.extend(child_elements)

        return results
    except Exception as e:
        print("An error occured while finding a nested element", e)
        return None
#----------------------------------------------------------------------------------------

def buildDictionary(roots, scanNum):
    try:
        yRoots = []
        xRoots = []
        CVATPoints = []
        for root in roots:
            xVals = root.find_all('X')
            yVals = root.find_all('Y')
            yRoots.append([float(yVal.text) for yVal in yVals])
            xRoots.append([float(xVal.text) for xVal in xVals])

        temp = ""
        for i in range(xRoots):
            for j in range(xRoots[i]):
                temp = temp + str(xRoots[i][j]) + "," + str(yRoots[i][j]) + ";"
        CVATPoints.append(temp)

        return dict(scanID = scanNum, rootXVals = xRoots, rootYVals = yRoots, points = CVATPoints)
    except Exception as e:
        print("An error occured while building coordinate dictionary:", e)
        return None

#----------------------------------------------------------------------------------------


def extractRootCoords(filePath):
    print("Extracting coordinates from: " + filePath)
    try:
        with open(filePath,'r') as f:
            data = f.read()
        soup = BeautifulSoup(data, 'xml')
        scans = soup.find_all('Scan')

        if len(scans) == 4:        
                roots = scans[0].find_all('Root')
                scanDict_0 = buildDictionary(roots,0)

                roots = scans[1].find_all('Root')
                scanDict_1 = buildDictionary(roots,1)

                roots = scans[2].find_all('Root')
                scanDict_2 = buildDictionary(roots,2)

                roots = scans[3].find_all('Root')
                scanDict_3 = buildDictionary(roots,3)

                return [scanDict_0, scanDict_1, scanDict_2, scanDict_3]
    
        else:
            raise ValueError("Incorrect number of scans in file: ")
    except Exception as e:
        print("An error occured while extracting root coordinates:", e)
        return None        


# convertRSPtoXML('Barley_101_10Aug2020.rsp')

# folderPath = "./"  # Replace this with the path to your folder containing the .rsp files

# grab all .rsp files in folderPath, convert them to xml (pull all metadata and put it in [filename]_clipped)
# rspFiles = glob.glob(os.path.join(folderPath, "*.rsp"))

# for filePath in rspFiles:
#     try:
        
#         convertRSPtoXML(filePath)
#     except Exception as e:
#         print(f"Error while processing {filePath}: {e}")

# grab all .xml files in folderPath, make 4 dictionaries, 
# xmlFiles = glob.glob(os.path.join(folderPath, "*.rsp_clipped.xml"))

# for filePath in xmlFiles:
#     try:
#         
#         buildDictionaries(filePath)            
#     except Exception as e:
#         print(f"Error while processing {filePath}: {e}")
            
# scanDictionaries = extractRootCoords('./Barley_101_10Aug2020.rsp_clipped.xml')
# with open('./output.txt','w') as oup:
#     for dict in scanDictionaries:
#         for key, value in dict.items():
#             oup.write(f"{key}: {value}\n")

