import glob
import os
from tqdm import tqdm
import matplotlib.pyplot as plt

def extract_pngs_from_text_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    start_marker = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
    end_marker = b'IEND'
    
    image_count = 0
    start_pos = 0
    saveCount = 0

    imageSizes = []
    allImageSizes = []
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

        if ((image_count - 1) % 4 == 0):
            saveCount += 1
            image = data[start_pos:end_pos]
            imageSizes.append(len(image))
            fileName = f.name
            if(len(image)<10000000):
                print(fileName + "Is all fucked up!")
            # DIndex = fileName.find("_") + 5
            # imageName = "./adjustedImages" + fileName[5:DIndex] + "D" + str(saveCount) + "_" + fileName[DIndex:-3] + "PNG"
            # with open(imageName, 'wb') as imageFile:
            #     imageFile.write(image)

        image_count += 1
        start_pos = end_pos
    return [imageSizes, allImageSizes]
        

imageSizes = []
allImageSizes = []

folderPath = './rsp'
xmlFiles = glob.glob(os.path.join(folderPath, "*.rsp"))
for filepath in tqdm(xmlFiles):
    imsz = extract_pngs_from_text_file(filepath)
    imageSizes.append(imsz[0].copy())
    allImageSizes.append(imsz[1])

transposed_values = list(zip(*imageSizes))
flattened_image_sizes = [size for sublist in imageSizes for size in sublist]
plt.plot(range(len(flattened_image_sizes)), flattened_image_sizes, marker='o', linestyle='-')
plt.xlabel('Image')
plt.ylabel('Image Size')
plt.title('Image Sizes in CVAT')
plt.grid(True)
plt.show()

transposed_allValues = list(zip(*allImageSizes))
flattened_all_image_sizes = [size for sublist in allImageSizes for size in sublist]
plt.plot(range(len(flattened_all_image_sizes)), flattened_all_image_sizes, marker='o', linestyle='-')
plt.xlabel('Image')
plt.ylabel('Image Size')
plt.title('Image Sizes in RSP Files')
plt.grid(True)
plt.show()

