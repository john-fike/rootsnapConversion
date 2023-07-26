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

def buildDictionary(roots, scanID):
    try:
        xRoots = []        
        yRoots = []
        CVATPoints = []
        for root in roots:
            xVals = root.find_all('X')
            yVals = root.find_all('Y')
            xRoots.append([float(xVal.text) for xVal in xVals])            
            yRoots.append([float(yVal.text) for yVal in yVals])

        for i in range(len(xRoots)):
            temp = []
            for j in range(len(xRoots[i])):
                temp.append(str(xRoots[i][j]) + "," + str(yRoots[i][j]) + ";")
            CVATPoints.append(temp)
        

        return dict(scanID = scanID, points = CVATPoints)
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

