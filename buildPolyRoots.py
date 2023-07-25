import extractRSProots

import os
import glob

# folderPath = './samplePoints.xml'

scanDict = extractRSProots.extractRootCoords('./samplePoints.xml') 
# print(scanDict)
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
