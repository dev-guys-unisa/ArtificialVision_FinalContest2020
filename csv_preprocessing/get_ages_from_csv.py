import os
import csv
import numpy as np

def read_csv(ages):
    with open(os.path.abspath("train.age_detected.csv")) as csvfile:
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
            age = np.round(float(split[1]))
            ages[identity][jpg] = age
    return ages
