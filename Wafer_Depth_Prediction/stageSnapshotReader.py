import os
import csv


def check(string, sub_str):
    if (string.find(sub_str) == -1):
        return bool(False)
    else:
        return bool(True)

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            if check(fullPath,"AMACDiag"):
                print(check(fullPath,"AMACTrace"))
                allFiles.append(fullPath)
                
    return allFiles


dirName = 'E:\\DL\\5X_center_dies_MOI_items\\5X_center_dies_MOI';
    
# Get the list of all files in directory tree at given path
listOfFiles = getListOfFiles(dirName)

# Print the files
for elem in listOfFiles:
    print(elem)
print ("****************")


import matplotlib.pyplot as plt
import csv 
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

  
x =[5, 7, 8, 7, 2, 17, 2, 9,
    4, 11, 12, 9, 6] 
  
y =[99, 86, 87, 88, 100, 86, 
    103, 87, 94, 78, 77, 85, 86]
  
#plt.scatter(x, y, c ="blue")
  
# To show the plot
#plt.show()
a = []
b = []
c = []

from csv import DictReader # open file in the read mode
# with open('E:\\DL\\5X_center_dies_MOI_items\\5X_center_dies_MOI\\StageSnapshot_20211115052711\\AMACDiagRecorder_20211115052711.csv', 'r') as read_obj: # pass the file object to DictReader() to get the DictReader object
#     dict_reader = DictReader(read_obj) # get a list of dictionaries from dct_reader
#     list_of_dict = list(dict_reader) # print list of dict i.e. rows
#     print(list_of_dict)
import pandas as pd
for elem in listOfFiles:
    with open(elem, 'r') as read_obj: # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj) # Get all rows of csv from csv_reader object as list of tuples
        list_of_tuples = list(map(tuple, csv_reader)) # display all rows of csv
        # print(list_of_tuples[0])
        # print(list_of_tuples[1])
        # print(list_of_tuples[2])
        # print(list_of_tuples[6])
        # print(list_of_tuples[7])


    # print(int(list_of_tuples[7][1]))
    # print(int(list_of_tuples[7][9]))
    for i in range(7,len(list_of_tuples)-1):
        a.append(int(list_of_tuples[i][1]))
        b.append(int(list_of_tuples[i][9]))
        c.append(int(list_of_tuples[i][4]))

# Program to draw scatter plot using Dataframe.plot
# Import libraries

    
# Prepare data
data={'X': a, 'Y':b}
# Load data into DataFrame
df = pd.DataFrame(data = data);

# Draw a scatter plot
df.plot.scatter(x = 'X', y = 'Y', s = 100);

plt.show()

# plt.scatter(a, b, c ="blue")   
# plt.show()


fig = pyplot.figure()
ax = Axes3D(fig)

# sequence_containing_x_vals = list(range(0, 100))
# sequence_containing_y_vals = list(range(0, 100))
# sequence_containing_z_vals = list(range(0, 100))

# random.shuffle(sequence_containing_x_vals)
# random.shuffle(sequence_containing_y_vals)
# random.shuffle(sequence_containing_z_vals)

ax.scatter(a, c, b)
pyplot.show()