
def extract_pngs_from_text_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    start_marker = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
    end_marker = b'IEND'
    
    image_count = 0
    start_pos = 0
    saveCount = 0
    while True:
        start_pos = data.find(start_marker, start_pos)
        if start_pos == -1:
            break

        end_pos = data.find(end_marker, start_pos)
        if end_pos == -1:
            break

        end_pos += 4  # Add 4 bytes for the "IEND" chunk

        if ((image_count - 1) % 4 == 0):
            saveCount += 1
            image = data[start_pos:end_pos]
            fileName = f.name
            DIndex = fileName.find("_") + 5
            imageName = fileName[:DIndex] + "D" + str(saveCount) + "_" + fileName[DIndex:-3] + "PNG"
            with open(imageName, 'wb') as image_file:
                image_file.write(image)

        image_count += 1
        start_pos = end_pos

# Example usage:
file_path = "./Barley_101_10Aug2020.rsp"
extract_pngs_from_text_file(file_path)


