'''
    MAIN FILE
    Launch this from obtaining all needed sets to give to the CNN
'''

import os

from get_ages_from_csv import read_csv
from group_ages import group_ages
from recover_identities import recover_identities
from plot_utils import vs_plot
from dataset_split import train_test_val_split
from extract_jpgs import extract_jpgs

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PATH_TO_CSV_FILE = os.path.join(BASE_PATH,"../face_annotations/test.detected.csv")

print("Getting ages...")
ages = read_csv(PATH_TO_CSV_FILE, test=False)
print("Getting ages... DONE")

print("Grouping ages...")
grouped_ages, final_dict = group_ages(ages)
print("Grouping ages... DONE")

print ("Recovering identities from groups...")
final_dict = recover_identities(grouped_ages,final_dict)
print ("Recovering identities from groups...DONE")

print("NUMBER OF TAKEN IDENTITIES: {}".format(len(final_dict.keys()))) #8421
cnt = 0
for jpgs in final_dict.values():
    cnt += len(jpgs)
print("NUMBER OF TAKEN SAMPLES: {}".format(cnt)) #1261462

print("Splitting dataset...")
splitted_dict_samples, splitted_dict_labels = train_test_val_split(ages, final_dict) #70% training, 20% validation, 10% test
n_train, n_val, n_test = 0,0,0
for id in list(splitted_dict_samples.keys()):
    n_train += len(list(splitted_dict_samples[id]["train"]))
    n_val += len(list(splitted_dict_samples[id]["val"]))
    n_test += len(list(splitted_dict_samples[id]["test"]))
print ("TRAINING={}, VALIDATION={}, TEST={}".format(n_train, n_val, n_test)) # TRAINING=790488, VALIDATION=344795, TEST=126179
print("Splitting dataset...DONE")

print ("Plotting...")
vs_plot(ages, final_dict, splitted_dict_labels)
print ("Plotting...DONE")

print("Recovering files of the chosen images ...")
set_type = "train" # to modify if the set to extract is another (validation or test)
extract_jpgs(splitted_dict_samples, set_type)
print("Recovering files of the chosen images ... DONE")

