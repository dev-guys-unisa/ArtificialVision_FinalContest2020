import tensorflow as tf
import numpy as np
import cv2 as cv

'''
    This function creates the format required for reading the record.
    It returns a dictionary containing the fields to be read.
'''
def _get_format(test=False):
    if test:
        tfrecord_format = (
        {
            "path": tf.io.FixedLenFeature([], tf.string),
            "image_raw": tf.io.FixedLenFeature([], tf.string),
        }
    )

    else:
        tfrecord_format = (
        {
            "path": tf.io.FixedLenFeature([], tf.string),
            "image_raw": tf.io.FixedLenFeature([], tf.string),
            "width": tf.io.FixedLenFeature([], tf.int64),
            "height": tf.io.FixedLenFeature([], tf.int64),
            "label": tf.io.FixedLenFeature([], tf.int64),
        }
    )

    return tfrecord_format

'''
    This function maps a record of the dataset passed as input to the 
    fields of the format dictionary created according to parameter "test".
'''
def _extract_fn(tfrecord):
    global test

    # Extract features using the keys set during creation
    tfrecord_format = _get_format(test=test)
    
    # Extract the data record
    sample = tf.io.parse_single_example(tfrecord, tfrecord_format)
    path = sample["path"]
    image = tf.io.decode_jpeg(sample["image_raw"], channels=3)
    if not test:
        width = tf.cast(sample["width"], tf.int32)
        height = tf.cast(sample["height"], tf.int32)
        label = tf.cast(sample["label"], tf.int32)

    if test:
        return [image, path]
    else:
        return [image, path, width, height, label]

'''
    This function reads and shows the informations contained in the
    entire TFRecord whose path is passed as input.
'''
def read_tfrecord(path_tfrecord):
  global test

  dataset = tf.data.TFRecordDataset(path_tfrecord)
  dataset1 = dataset.map(_extract_fn,num_parallel_calls=1)
  iterator = iter(dataset1)

  # count number of occurences in the tfrecord
  #cnt = dataset.reduce(np.int64(0), lambda x, _: x+1)
  #print("{} records".format(cnt.numpy()))

  done = False
  while not done:
    print("notdone")
    try:
        print("iterator")
        if test: 
            image, path = iterator.get_next()
        else: 
            image, path, width, height, label = iterator.get_next()
            width = int(width.numpy())
            heigth = int(height.numpy())
            label = int(label.numpy())
        path = path.numpy().decode('utf-8')
        image = image.numpy()
        if image is not None: cv.imshow("figure",image)
        else: print("Image not found")
        cv.waitKey(0)
    except tf.errors.OutOfRangeError: 
        print("Iterator exhausted")
        done=True

print("Reading TFrecord...")

# modify to indicate where the TFRecord to be read is placed
PATH_TO_TFRECORD = "E:/tfrecords/training_set_cropped.record"
test = False # indicate if a test TFRecord has to be read

read_tfrecord(PATH_TO_TFRECORD, test=test)
print("Reading TFrecord...DONE")