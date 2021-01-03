from mtcnn.mtcnn import MTCNN
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
import numpy as np

import sys
sys.path.append("../GenderRecognitionFramework/training")
from dataset_tools import mean_std_normalize

'''
  This function preprocess the image passed as input, applying a normalization
  consisting in the subtraction of the mean of 3 color channel over all the dataset.
  Taken from https://github.com/MiviaLab/GenderRecognitionFramework/blob/ddc06241c823b4fb307b7ff751d4683b7ca681ce/training/dataset_tools.py#L376
  modifying the means of the dataset to subtract
'''
def vggface2_preprocessing(img):
  ds_means = np.array([131.0912, 103.8827, 91.4953]) # RGB
  ds_stds = None
  img = mean_std_normalize(img, ds_means, ds_stds)
  if (len(img.shape)<3 or img.shape[2]<3):
      img = np.repeat(np.squeeze(img)[:,:,None], 3, axis=2)
  return img

'''
  This function resizes the image passed as input to the target shape indicated.
  If the actual dimensione of the image is less than the target, the resize is made by adding black padding
  around the image, otherwise the resizing is preceeded by the application of an anti-aliasing filter.
'''
def custom_resize(image, h, w, t_shape):
  #print("Resizing to {}".format(shape))
  if h < t_shape[0] and w < t_shape[1]:
      image = tf.image.resize_with_crop_or_pad(image, t_shape[0], t_shape[1])
  else:
    image = tf.image.resize(
        image, (t_shape[0],t_shape[1]), antialias=True
    )
  return image

'''
  This function extracts the max area corresponding to a face detected in the given image
'''
def extract_face(img):
  if img is not None:
    detector = MTCNN()
    # detect all faces presented in the image
    results = detector.detect_faces(img)
    # compute max detected area for choosing face in close-up
    max_area = 0
    index = 0 
    if len(results) == 0: #if no faces are detected, return original image
      return img
    else:
      for i in range(0, len(results)):
        x1, y1, width, height = results[i]['box']
        area = width*height
        if area>=max_area:
          max_area = area
          index = i

      # crop faces using parameters of max detected area
      x_o, y_o, width, height = results[index]['box']
      if width >= 10 and height >= 10: #if detected area too small, return original image
        # check if top-left point is negative, that means faces outside limits of image
        if x_o >= 0:
          x_o = 0
        if y_o >=0:
          y_o = 0
        # crop
        x1, y1 = x_o, y_o
        x2, y2 = x_o + width, y_o+height
        face = img[y1:y2, x1:x2]
        return face
      else:
        return img
  else:
    print("Image {} not found".format(img))
    return img