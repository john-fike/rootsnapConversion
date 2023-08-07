import glob
import os
from tqdm import tqdm
import matplotlib.pyplot as plt

def extract_pngs_from_text_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
    except Exception as e:
        print("There was an error opening rsp: " + file_path)

    start_marker = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
    end_marker = b'IEND'
    
    image_count = 0
    start_pos = 0
    scanCount = 0
    saveCount = 0
    largeScanCount = 0

    savedImageSizes = []
    allImageSizes = []
    try:
        while True:
            start_pos = data.find(start_marker, start_pos)
            if start_pos == -1:
                break

            end_pos = data.find(end_marker, start_pos)
            if end_pos == -1:
                break

            end_pos += 4  # Add 4 bytes for the "IEND" chunk

            image = data[start_pos:end_pos]
            allImageSizes.append(len(image))

            scanCount += 1
            fileName = f.name
            DIndex = fileName.find("_") + 5
            try:
                imageName = "./allAdjustedImages/" + fileName[6:DIndex] + "S" + str(scanCount) + "_" + fileName[DIndex:-3] + "PNG"
                with open(imageName, 'wb') as imageFile:
                    imageFile.write(image)
            except Exception as e:
                print("There was an error saving scan: " + imageName)


            if(len(image)>5000000):
                largeScanCount += 1
                if(largeScanCount % 2 == 0):
                    saveCount += 1
                    savedImageSizes.append(len(image))
                    fileName = f.name
                    DIndex = fileName.find("_") + 5
                    imageName = "./adjustedImages/" + fileName[6:DIndex] + "D" + str(saveCount) + "_" + fileName[DIndex:-3] + "PNG"
                    try:
                        with open(imageName, 'wb') as image_file:
                            image_file.write(image)  
                        if(saveCount > 4):
                            print("   The rsp containing image: " + imageName + " is weird and you should probably check it")
                    except Exception as e:
                        print("There was an error saving scan: " + imageName)

            image_count += 1
            start_pos = end_pos
        return [savedImageSizes, allImageSizes]
    except Exception as e:
        print("There was an error while extracting PNG from scan: " + file_path)
        return None
        

def displaySizeGraph(savedImageSizes, allImageSizes):
    try:
        flattened_image_sizes = [size for sublist in savedImageSizes for size in sublist]
        plt.plot(range(len(flattened_image_sizes)), flattened_image_sizes, marker='o', linestyle='-')
        plt.xlabel('Image')
        plt.ylabel('Image Size')
        plt.title('Image Sizes in CVAT')
        plt.grid(True)
        plt.show()

        flattened_all_image_sizes = [size for sublist in allImageSizes for size in sublist]
        plt.plot(range(len(flattened_all_image_sizes)), flattened_all_image_sizes, marker='o', linestyle='-')
        plt.xlabel('Image')
        plt.ylabel('Image Size')
        plt.title('Image Sizes in RSP Files')
        plt.grid(True)
        plt.show()
    except Exception as e:
        print("There was an error while making image size graphs ")


savedImageSizes = []
allImageSizes = []

folderPath = './rsp'
xmlFiles = glob.glob(os.path.join(folderPath, "*.rsp"))
for filepath in tqdm(xmlFiles):
    imsz = extract_pngs_from_text_file(filepath)
    savedImageSizes.append(imsz[0].copy())
    allImageSizes.append(imsz[1])

displaySizeGraph(savedImageSizes, allImageSizes)