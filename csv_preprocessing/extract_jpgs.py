'''
    This function allows to recover, from the given training set, the files corresponding to the images
    chosen for each identity according to the specific split done.
    It takes:
        - splitted_dict_samples -> {id:{"<set>":[jpgs]}} of images chosen for a particular set
        - a string representing the type of set to extract
'''

import os
import progressbar
from shutil import copy2

PATH_TO_EXTRACT_DATASET = "E:\\train\\"
PATH_TO_EXTRACTING_DIR = "E:\\test_set\\"

MAX_VALUES = {"train":790488, "validation":344795, "test":126179}

def extract_jpgs(splitted_dict_samples, set_type): #{id:{"train":[jpgs]}}
    try:
        MAX_VALUE = MAX_VALUES[set_type]
    except KeyError:
        print("Unvalid set type")
        return

    cnt = 0

    print("Extracting to {}...".format(PATH_TO_EXTRACTING_DIR))
    with progressbar.ProgressBar(max_value=MAX_VALUE) as bar:
        ids = list(splitted_dict_samples.keys())
        ids.sort()
        for id in ids:
            os.mkdir(PATH_TO_EXTRACTING_DIR + id)
            jpgs = list(splitted_dict_samples[id][set_type])
            jpgs.sort()
            for jpg in jpgs:
                cnt += 1
                src = PATH_TO_EXTRACT_DATASET + id + jpg    # train/id/jpg
                dst = PATH_TO_EXTRACTING_DIR + id + jpg     # training_set/id/jpg
                copy2(src, dst)
                bar.update(cnt)
    print("Extracting...DONE")