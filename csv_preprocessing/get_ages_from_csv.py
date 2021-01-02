''' 
    This function allows to read CSV file for getting labels corresponding to every images.
    It takes the path of the CSV file to read and a boolean to indicate if it's a test CSV file,
    because in this case ages are read as float not rounded.
    It returns a dictionary {identity:{jpg_path:age}}
'''

import os
import csv
import numpy as np

def read_csv(csv_path, test=False):
    ages = {}
    with open(csv_path) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ')
        for row in csvreader:
            split = row[0].split(",")
            file_path = split[0]
            identity = file_path[:7]
            try:
                d = ages[identity]
            except:
                ages[identity] = {}
            jpg = file_path[7:]
            age = np.round(float(split[1])) if not test else float(split[1])
            ages[identity][jpg] = age
    return ages
