import sys
import os
BASE_PATH = os.path.abspath(os.path.dirname(__file__))

sys.path.append("../face_extraction/")
from extract_face import custom_resize, vggface2_preprocessing

import tensorflow as tf
import numpy as np
import os
import csv
import cv2 as cv
from matplotlib import pyplot as plt
import progressbar

sys.path.append("../csv_preprocessing/")
from get_ages_from_csv import read_csv

TARGET_SHAPE = (224,224,3)
MAX_VALUE = 169396

def _int64_feature(value):
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _bytes_feature(value):
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def convert_to(dataset_path, ages):
  cnt = 0
  filename = "E:/tfrecords/"+dataset_path.split("/")[-1] + '.record'
  writer = tf.io.TFRecordWriter(filename)

  os.chdir(dataset_path)
  all_dirs = os.listdir(".") 

  print("Have to process {} identities".format(MAX_VALUE))

  with progressbar.ProgressBar(max_value=MAX_VALUE) as bar:
      for d in all_dirs:
        if os.path.isdir(d): #identity
          id_dir = os.path.join(os.getcwd(), d)
          for f in os.listdir(id_dir): #read all jpgs
            jpg_dir = os.path.join(id_dir, f)
            if os.path.isfile(jpg_dir):
              path = jpg_dir.split('\\')[-2]+"/"+jpg_dir.split('\\')[-1]
              age = ages[d]["/"+f]
              img = cv.imread(jpg_dir, cv.IMREAD_UNCHANGED)
              img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
              #preprocessing
              #img = extract_face(img)
              img = vggface2_preprocessing(img)
              img = custom_resize(img, img.shape[0], img.shape[1], TARGET_SHAPE)
              img = np.asarray(img)
              image_shape = img.shape
              is_success, im_buf_arr = cv.imencode(".jpg", img)
              image_string = im_buf_arr.tobytes()
              example = tf.train.Example(features=tf.train.Features(feature={
              'path': _bytes_feature((path).encode('utf-8')),
              'width': _int64_feature(image_shape[1]),
              'height': _int64_feature(image_shape[0]),
              'label': _int64_feature(int(age)),
              'image_raw': _bytes_feature(image_string)
              }))
              writer.write(example.SerializeToString()) # write path-image to tfrecord
              cnt += 1
              bar.update(cnt)
            else:
              print("Unexpected directory{}".format(f))
        else:
          print("Unexpected file {}".format(d))


def convert_to_test(dataset_path, ages): #path, ages
  cnt = 0
  filename = "E:/tfrecords/"+dataset_path.split("/")[-1] + '.record'
  writer = tf.io.TFRecordWriter(filename)

  os.chdir(dataset_path)
  all_dirs = os.listdir(".") 

  print("Have to process {} identities".format(MAX_VALUE))

  with progressbar.ProgressBar(max_value=MAX_VALUE) as bar:
    with open('E:/own_test_set_gt.csv', mode='w', newline="", encoding="utf-8") as csv_file:
      csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      for d in all_dirs:
        if os.path.isdir(d): #identity
          id_dir = os.path.join(os.getcwd(), d)
          for f in os.listdir(id_dir): #read all jpgs
            jpg_dir = os.path.join(id_dir, f)
            if os.path.isfile(jpg_dir):
              path = jpg_dir.split('\\')[-2]+"/"+jpg_dir.split('\\')[-1]
              age = ages[d]["/"+f]
              csv_writer.writerow([path, age]) # write path-age to gt csv

              img = cv.imread(jpg_dir, cv.IMREAD_UNCHANGED)
              img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
              #preprocessing
              #img = extract_face(img)
              img = vggface2_preprocessing(img)
              img = custom_resize(img, img.shape[0], img.shape[1], TARGET_SHAPE)
              img = np.asarray(img)
              is_success, im_buf_arr = cv.imencode(".jpg", img)
              image_string = im_buf_arr.tobytes()
              example = tf.train.Example(features=tf.train.Features(feature={
              'path': _bytes_feature((path).encode('utf-8')),
              'image_raw': _bytes_feature(image_string)
              }))
              writer.write(example.SerializeToString()) # write path-image to tfrecord
              cnt += 1
              bar.update(cnt)
            else:
              print("Unexpected directory{}".format(f))
        else:
          print("Unexpected file {}".format(d))


PATH_TO_CROPPED_TS = "E:/vggface2_test_cropped"
PATH_TO_CSV = BASE_PATH+"../train.age.detected.csv"
test=True

print("Recovering ages...")
ages = read_csv(PATH_TO_CSV, test=test)
print("Recovering ages...DONE")
print("Creating TFRecord...")
convert_to(PATH_TO_CROPPED_TS, ages) if test else convert_to_test(PATH_TO_CROPPED_TS,ages)
print("Creating TFRecord...DONE")