import sys
import os
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_PATH)

import tensorflow as tf
import numpy as np
import os
import cv2 as cv
from get_ages_from_csv import read_csv
from PIL import Image
from matplotlib import pyplot as plt

def _int64_feature(value):
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _bytes_feature(value):
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def convert_to(dataset_path, ages): #path, ages
  filename = os.path.join(BASE_PATH, "../tfrecord_processing/"+dataset_path.split("/")[-1] + '.record')
  writer = tf.io.TFRecordWriter(filename)

  os.chdir(dataset_path)
  all_dirs = os.listdir(".")

  d=all_dirs[0]
  if os.path.isdir(d): #identity
    id_dir = os.path.join(os.getcwd(), d)
    for f in os.listdir(id_dir): #read all jpgs
      jpg_dir = os.path.join(id_dir, f)
      if os.path.isfile(jpg_dir):
        age = ages[d]["/"+f]
        img = cv.imread(jpg_dir, cv.IMREAD_UNCHANGED)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        image_shape = img.shape
        is_success, im_buf_arr = cv.imencode(".jpg", img)
        image_string = im_buf_arr.tobytes()
        example = tf.train.Example(features=tf.train.Features(feature={
        'width': _int64_feature(image_shape[1]),
        'height': _int64_feature(image_shape[0]),
        'label': _int64_feature(int(age)),
        'image_raw': _bytes_feature(image_string)
        }))
        writer.write(example.SerializeToString())
      else:
        print("Unexpected directory{}".format(f))
  else:
    print("Unexpected file {}".format(d))

def _extract_fn(tfrecord):
    # Extract features using the keys set during creation
    tfrecord_format = (
        {
            "image_raw": tf.io.FixedLenFeature([], tf.string),
            "width": tf.io.FixedLenFeature([], tf.int64),
            "height": tf.io.FixedLenFeature([], tf.int64),
            "label": tf.io.FixedLenFeature([], tf.int64),
        }
    )
    # Extract the data record
    sample = tf.io.parse_single_example(tfrecord, tfrecord_format)
    image = tf.io.decode_jpeg(sample["image_raw"], channels=3)
    width = tf.cast(sample["width"], tf.int32)
    height = tf.cast(sample["height"], tf.int32)
    label = tf.cast(sample["label"], tf.int32)

    return [image, label, width, height]

def read_tfrecord(path_tfrecord):
  '''for record in tf.python.python_io.tf_record_iterator(path_tfrecord):
    example = tf.train.Example()
    example.ParseFromString(record)

    img_string = (example.features.feature['image_raw']
        .bytes_list
        .value[0])

    label = (example.features.feature['label']
        .Int64List
        .value[0])

    width = (example.features.feature['width']
        .Int64List
        .value[0])

    heigth = (example.features.feature['height']
        .Int64List
        .value[0])

    width = np.fromstring(width, dtype=np.uint8)
    heigth = np.fromstring(heigth, dtype=np.uint8)
    label = np.fromstring(label, dtype=np.uint8)

    img_1d = np.fromstring(img_string, dtype=np.uint8)
    reconstructed_img = img_1d.reshape((heigth, width, -1))

    plt.imshow(reconstructed_img)
    plt.show()
    print(label)'''



  dataset = tf.data.TFRecordDataset(path_tfrecord)
  dataset1 = dataset.map(_extract_fn,num_parallel_calls=1)

  iterator = iter(dataset1)

  done = False
  while not done:
    image, label, width, heigth = iterator.get_next()
    #image = tf.reshape(image, (width,heigth,3))
    #print(img.shape)
    cv.imshow("figure",image.numpy())
    #plt.show()
    cv.waitKey(0)
    print(label)


PATH_TO_CROPPED_TS = os.path.join(BASE_PATH, "../training_set")

ages = {}
print("Recovering ages...")
ages = read_csv(ages)
print("Recovering ages...DONE")
print("Creating TFRecord...")
convert_to(PATH_TO_CROPPED_TS, ages)
print("Creating TFRecord...DONE")

'''print("Reading TFrecord...")
read_tfrecord(os.path.join(BASE_PATH,"..\\tfrecord_processing\\training_set.record"))
print("Reading TFrecord...DONE")'''