import re

with open('./Barley_101_D1_10Aug2020.txt', 'rb') as f:
    lines = f.readlines()

with open('./Barley_101_10Aug2020 copy.txt', 'rb') as g:
    lines_copy = g.readlines()

lines_copy[3]=lines[3]

for i in range(10):
    print(lines[i])


with open('./output.txt', 'wb') as oup:
    for line in lines:
        oup.write(line)



# with open('./output.txt', 'w', encoding="latin-1") as oup:
#     for line in lines:
#         oup.write(line)
#     oup.write("-----------------\n")
    
#     for i in [0,5,9,13]:
#         oup.write(lines[i][-30:])
# def extract_jpegs(file_path):
#     with open(file_path, 'rb') as file:
#         data = file.read()

#     start_marker = b'\xFF\xD8'
#     end_marker = b'\xFF\xD9'

#     image_count = 0
#     start_pos = 0
#     while True:
#         start_pos = data.find(start_marker, start_pos)
#         if start_pos == -1:
#             break

#         end_pos = data.find(end_marker, start_pos)
#         if end_pos == -1:
#             break

#         image_data = data[start_pos:end_pos + 2]
#         image_filename = f'image_{image_count}.jpg'

#         with open(image_filename, 'wb') as image_file:
#             image_file.write(image_data)

#         image_count += 1
#         start_pos = end_pos + 2

#     print(f"{image_count} JPEG images extracted.")

# # Example usage:
# file_path = "./Barley_101_10Aug2020.rsp"
# # extract_jpegs(file_path)

# with open('./Barley_101_10Aug2020 copy.rsp', 'r', encoding='latin-1') as file:
#     data = file.read()

# with open('test.png', 'wb') as img:
#     img.write(data.encode('latin-1'))