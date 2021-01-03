import csv
import os
import cv2 as cv
import progressbar
from shutil import copy2

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PATH_TO_CSV = os.path.join(BASE_PATH,"../face_annotations/test.detected.csv")
PATH_TO_TS = "E:/vggface2_test/test/"
PATH_TO_CROPPED_TS = "E:/vggface2_test_cropped"
if not os.path.isdir(PATH_TO_CROPPED_TS): os.mkdir(PATH_TO_CROPPED_TS)

MAX_VALUE = 169396
restore = True #decide if preserve original number of images recovering uncropped images

'''
    This function allows to crop the faces that are in the images pointed by the previous path, 
    recovering the corresponding faces' bounding boxes from the CSV in which are indicated.
'''
def get_bboxes ():
    cnt = 0
    with open(PATH_TO_CSV,encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ')
        with progressbar.ProgressBar(max_value=MAX_VALUE) as bar:
            for row in csvreader:
                #print(str(row))

                split = row[0].split(",")
                path = split[2]
                dir_path, file_path = path.split("/")[0], path.split("/")[1]
                id_folder = os.path.join(PATH_TO_CROPPED_TS, dir_path)
                #print(id_folder)
                x,y = int(split[4]), int(split[5])
                # if top-left point of the bbox has a negative coordinate, set it to 0 
                # because it probably means that the face is outside the limits of the image
                if x<0:
                    x=0
                if y<0:
                    y=0
                width = int(split[6])
                height = int(split[7])
                
                img = cv.imread(os.path.join(PATH_TO_TS, path),cv.IMREAD_UNCHANGED)
                if img is not None: #img exists
                    if not os.path.exists(id_folder): #if it's a new identity, create its folder
                        os.mkdir(id_folder)
                    cnt += 1
                    crop_img = img[y:y+height, x:x+width]
                    if crop_img.size!=0:
                        cv.imwrite(os.path.join(PATH_TO_CROPPED_TS, path), crop_img)
                    else:
                        print("Empty {}".format(os.path.join(PATH_TO_TS, path)))
                    bar.update(cnt)
                else:
                    print("image {} not found".format(os.path.join(PATH_TO_TS, path)))


'''
    This function recovers the uncropped images from the original training set, storing it as original
'''
def recover_uncropped():
    cnt = 0
    dirs = os.listdir(PATH_TO_TS)
    for d in dirs:
        dir_path = os.path.join(PATH_TO_TS,d) #origTS/id
        files = os.listdir(dir_path)
        for f in files:
            img_path = os.path.join(dir_path,f) #origTS/id/jpg
            path_to_check = os.path.join(PATH_TO_CROPPED_TS,os.path.join(d,f)) #croppedTS/id/jpg
            if not os.path.exists(path_to_check): #uncropped image -> save it as original
                #print(img_path)
                cnt += 1
                copy2(img_path, path_to_check)
    print("{} uncropped images restored".format(cnt))


print("Extracting faces...")
get_bboxes()
print("Extracting faces... DONE")

if restore:
    print("Recovering uncropped images...")
    recover_uncropped()
    print("Recovering uncropped images... DONE")    

        
