import tensorflow as tf
import numpy as np
import cv2 as cv

def _get_format(test):
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

def _extract_fn(tfrecord, test):
    # Extract features using the keys set during creation
    tfrecord_format = _get_format(test=True)
    
    # Extract the data record
    sample = tf.io.parse_single_example(tfrecord, tfrecord_format)
    path = sample["path"]
    image = tf.io.decode_jpeg(sample["image_raw"], channels=3)
    if not test:
        width = tf.cast(sample["width"], tf.int32)
        height = tf.cast(sample["height"], tf.int32)
        label = tf.cast(sample["label"], tf.int32)

    return [image, path] if test else [image, path, width, height, label]

def read_tfrecord(path_tfrecord, test=False):
  dataset = tf.data.TFRecordDataset(path_tfrecord)
  dataset1 = dataset.map(_extract_fn(dataset,test=test),num_parallel_calls=1)

  iterator = iter(dataset1)

  done = False
  while not done:
    if test: image, path = iterator.get_next()
    else: image, path, width, height, label = iterator.get_next()
    path = path.numpy().decode('utf-8')
    if test:
        width = int(width.numpy())
        heigth = int(heigth.numpy())
        label = int(label.numpy())
    image = image.numpy()
    #print("{}: w={}, h={}, shape={}, age={}".format(path, width, heigth, image.shape, label))
    print(path)
    cv.imshow("figure",image)
    cv.waitKey(0)


print("Reading TFrecord...")
read_tfrecord("E:/tfrecords/own_test_set_1.record")
print("Reading TFrecord...DONE")