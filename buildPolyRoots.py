import extractRSProots
import xml.etree.ElementTree as ET



# folderPath = './samplePoints.xml'

scanDict = extractRSProots.extractRootCoords('./samplePoints.xml') 
# print(scanDict)

with open('./output.txt','w') as oup:
    for dict in scanDict:
        for key, value in dict.items():
            oup.write(f"{key}: {value}\n")

with open('./output.txt', 'a') as oup:
    for i in range(len(scanDict[0]["points"])):
            for j in range(len(scanDict[0]["points"][i])):
                oup.write(scanDict[0]["points"][i][j])

# with open('./testCVATAnnotations.xml', 'a') as oup:
image = ET.Element("image")

for i in range(len(scanDict[0]["points"])):
    # for j in range(len(scanDict[0]["points"][i])):
        # for root in scanDict[0]["points"][i]:
    pointStr = ''.join(scanDict[0]["points"][i])
    print(pointStr)
    polyline = ET.Element("polyline", points = pointStr)
    image.append(polyline)

annotations = ET.ElementTree(image)
annotations.write('./testCVATAnnotations.xml')



# for i in range(len(scanDict[0]["rootXVals"])):
#     for j in range(len(scanDict[0]["rootXVals"][i])):
#         print(scanDict[0]["rootYVals"][i][j]) 
#         # print(scanDict[0]["rootXVals"][i][j])
#         print(",") 



# for filePath in xmlFiles:
#     try:
#         with open('./output.txt','a') as oup:
#             for dict in scanDict:
#                 for key, value in dict.items():
#                     oup.write(f"{key}: {value}\n")           
#     except Exception as e:
#         print(f"Error while processing {filePath}: {e}")
