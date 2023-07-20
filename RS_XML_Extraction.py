import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


print('Loading xml file...')

# Reading the data inside the xml
# file to a variable under the name
# data
with open('test.xml', 'r') as f:
    data = f.read()
 
# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object
Bs_data = BeautifulSoup(data, "xml")
 
# Finding all instances of tag
# `unique`
b_unique = Bs_data.find_all('date')
 
print(b_unique)
 
# # Using find() to extract attributes
# # of the first instance of the tag
# b_name = Bs_data.find('child', {'name':'Frank'})
 
# print(b_name)
 
# # Extracting the data stored in a
# # specific attribute of the
# # `child` tag
# value = b_name.get('test')
 
# print(value)



#use dictionary...
