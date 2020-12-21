import os
import progressbar
from shutil import copy2

PATH_TO_EXTRACT_DATASET = "C:\\Users\\ASUS\Desktop\\CORSI_MAGISTRALE\\II ANNO\\I SEMESTRE\\Artificial Vision\\progetto\\train\\"
PATH_TO_TRAINING_DIR = "C:\\Users\\ASUS\\Desktop\\CORSI_MAGISTRALE\\II ANNO\\I SEMESTRE\\Artificial Vision\\progetto\\training_set\\"
MAX_VALUE = 790488

def extract_jpgs(splitted_dict_samples, set_type): #{id:{"train":[jpgs]}}
    cnt = 0

    print("Extracting to {}...".format(PATH_TO_TRAINING_DIR))
    with progressbar.ProgressBar(max_value=MAX_VALUE) as bar:
        ids = list(splitted_dict_samples.keys())
        ids.sort()
        for id in ids:
            os.mkdir(PATH_TO_TRAINING_DIR + id)
            jpgs = list(splitted_dict_samples[id][set_type])
            jpgs.sort()
            for jpg in jpgs:
                cnt += 1
                src = PATH_TO_EXTRACT_DATASET + id + jpg    # train/id/jpg
                dst = PATH_TO_TRAINING_DIR + id + jpg       # training_set/id/jpg
                copy2(src, dst)
                bar.update(cnt)
    print("Extracting...DONE")


