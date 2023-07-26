import extractRSProots
from bs4 import BeautifulSoup



# folderPath = './samplePoints.xml'

scanDict = extractRSProots.extractRootCoords('./samplePoints.xml') 


with open('./testCVATAnnotations.xml','r') as f:
    data = f.read()
soup = BeautifulSoup(data, 'xml')

for s in range(len(scanDict)):
    for i in range(len(scanDict[s]["points"])):
        image = soup.find("image", attrs = {'id':s})#replace 0 with s variable from dict loop
        pointStr = ''.join(scanDict[0]["points"][i])
        pointStr = pointStr[:-1]
        polyline = soup.new_tag("polyline", "\n", label = "root", source = "manual", occluded = "0", points = pointStr)
        image.append(polyline)
with open('./testCVATAnnotations.xml', 'w') as f:
    f.write(str(soup))