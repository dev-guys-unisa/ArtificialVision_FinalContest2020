import csv
import os
import cv2 as cv
import progressbar

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PATH_TO_CSV = os.path.join(BASE_PATH,"../training_set_face_annotations/train.detected.csv")
PATH_TO_TS = os.path.join(BASE_PATH, "../training_set")
PATH_TO_CROPPED_TS = os.path.join(BASE_PATH, "../training_set_cropped")
MAX_VALUE = 790488

def get_bboxes ():
    cnt = 0
    with open(PATH_TO_CSV) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ')
        with progressbar.ProgressBar(max_value=MAX_VALUE) as bar:
            for row in csvreader:
                split = row[0].split(",")
                path = split[2]
                dir_path, file_path = path.split("/")[0], path.split("/")[1]
                id_folder = os.path.join(PATH_TO_CROPPED_TS, dir_path)
                #print(id_folder)
                x,y = int(split[4]), int(split[5])
                if x<0:
                    x=0
                if y<0:
                    y=0
                width = int(split[6])
                height = int(split[7])

                img = cv.imread(os.path.join(PATH_TO_TS, path),cv.IMREAD_UNCHANGED)
                if img is not None: #esiste
                    if not os.path.exists(id_folder): #creo cartella identità
                        os.mkdir(id_folder)
                    cnt += 1
                    crop_img = img[y:y+height, x:x+width]
                    if crop_img.size!=0:
                        cv.imwrite(os.path.join(PATH_TO_CROPPED_TS, path), crop_img)
                    else:
                        print("Empty {}".format(os.path.join(PATH_TO_TS, path)))
                    bar.update(cnt)

get_bboxes()
        

        
