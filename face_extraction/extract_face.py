
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
import numpy as np

import sys
sys.path.append("../../GenderRecognitionFramework/training")
from dataset_tools import mean_std_normalize

'''
  This function preprocess the image passed as input, applying a normalization
  consisting in the subtraction of the mean of 3 color channel over all the dataset. 
'''
def vggface2_preprocessing(img):
  #(rivedere perchè non dovrebbero essere le medie nostre avendo preso meno dataset)
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