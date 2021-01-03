# ArtificialVision_FinalContest2020
The aim of this project is to design a DCNN (as regressor or classifier) for age estimation.

## Preparation of the dataset to give as input to DCNN
For dealing with [Google Colab](https://colab.research.google.com/), it's convenient to use a special format to compat data, TFRecord. 

In order to create this files, first of all you have to choose the datasets (training, validation and test sets) to be used for training and evaluate the model; our implementation (due to limits imposed by Colab's GPU usage) consists in using a subpart of the original training set of [VggFace2](https://github.com/ox-vgg/vgg_face2) composed by at most by 150 images per identity; afterwards, it's divided in 70% for training, 20% for validation and 10% for test. To choose the subpart from the entire dataset, we divide the age range of each identity of the dataset in 4 groups, randomly taken a fixed number of images for each group; this number is 30, execpt for the 3rd group in which we take 60 elements in order to respect the original data distribution. If an identity has less than 150 images, it has taken entirely without age grouping; moreover if, after the age grouping, a group has less than 30 elements, it is taken entirely and the remaining images to reach the threshold of 150 are randomly chosen from the images of the other groups not already taken.

In order to reproduce our experiment, you have to launch the script [process_csv.py](csv_preprocessing/process_csv.py) 
<addr>python3
which:
* recovers the ages from the CSV file containing the annotations
* groups files of the 
