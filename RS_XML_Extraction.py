import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

import os
import glob

#----------------------------------------------------------------------------------------
# convert RSP file to XML
# remove jpg binary data, isolate xml metadata containing root annotations and save them to [filename]_clipped
def convertRSPtoXML(filePath):
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

def buildDictionaries(filePath):
    try:
        with open(filePath,'r') as f:
            data = f.read()
        soup = BeautifulSoup(data, 'xml')

        scans = soup.find_all('Scan')
        if len(scans) == 4:
            scan = scans[0]
            roots = scan.find_all('Root')
            scanDict_0 = {
                "scanID" : 0,
                "roots" : roots
            }
            scan = scans[1]
            roots = scan.find_all('Root')
            scanDict_1 = {
                "scanID" : 1,
                "roots" : roots
            }
            
            scan = scans[2]
            roots = scan.find_all('Root')
            scanDict_2 = {
                "scanID" : 2,
                "roots" : roots
            }
            
            scan = scans[3]
            roots = scan.find_all('Root')
            scanDict_3 = {
                "scanID" : 3,
                "roots" : roots
            }        
        else:
            raise ValueError("Incorrect number of scans in file:" + filePath)
        return [scanDict_0, scanDict_1, scanDict_2, scanDict_3]
    except Exception as e:
        print("An error occured while finding a nested element:", e)
        return None        



# convertRSPtoXML('Barley_101_10Aug2020.rsp')

folderPath = "./"  # Replace this with the path to your folder containing the .rsp files

# grab all .rsp files in folderPath, convert them to xml (pull all metadata and put it in [filename]_clipped)
rspFiles = glob.glob(os.path.join(folderPath, "*.rsp"))

for filePath in rspFiles:
    try:
        print("Extracting metadata for " + filePath)
        convertRSPtoXML(filePath)
    except Exception as e:
        print(f"Error while processing {filePath}: {e}")

# grab all .xml files in folderPath, make 4 dictionaries, 
xmlFiles = glob.glob(os.path.join(folderPath, "*.rsp_clipped.xml"))

for filePath in xmlFiles:
    try:
        print("Building dictionary for: " + filePath)
        buildDictionaries(filePath)            
    except Exception as e:
        print(f"Error while processing {filePath}: {e}")
            

