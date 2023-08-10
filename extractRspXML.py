import glob
import os



# extract XML from all rsp files in folderpath
# remove jpg binary data, isolate xml metadata containing root annotations and save them to [filename]_clipped.xml
def convertRSPtoXML(folderPath):
    rspFiles = glob.glob(os.path.join(folderPath, "*.rsp"))
    for filePath in rspFiles:
        convertRSPtoXML(filePath)
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

