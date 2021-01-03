# ArtificialVision_FinalContest2020
This repository is created for the final contest of Artificial Vision subject at University of Salerno.The aim of this project is to design a DCNN (as regressor or classifier) for age estimation on [VggFace2 dataset](https://github.com/ox-vgg/vgg_face2).

## **Preparation of the dataset to give as input to DCNN**
For dealing with [Google Colab](https://colab.research.google.com/), we to use a special format to compat data, TFRecord. 

In order to create this files, first of all you have to choose the datasets (training, validation and test sets) to be used for training and evaluate the model; **our implementation** (due to limits imposed by Colab's GPU usage) consists in using a subpart of the original training set of [the dataset VggFace2](https://github.com/ox-vgg/vgg_face2) composed by at most 150 images per identity; afterwards, it's divided in 70% for training, 20% for validation and 10% for test. To **choose the subpart** from the entire dataset, we divide the age range of each identity of the dataset in 4 groups, randomly taken a fixed number of images for each group; this number is 30, execpt for the 3rd group in which we take 60 elements in order to respect the original data distribution. If an identity has less than 150 images, it has taken entirely without age grouping for that identity; moreover if, after the age grouping, a group has less than 30 elements (40 for the 3rd group), it is taken entirely and the remaining images to reach the threshold of 150 are randomly chosen from the images of the other groups not already taken.

In order to **reproduce our experiment**, first of all you have to launch the script [process_csv.py](csv_preprocessing/process_csv.py) from its [directory](csv_preprocessing) with the command
```python
python3 process_csv.py
```

This script:
* recovers the ages from the CSV file containing the annotations (which has to be placed [here](CSV%20file%20for%20ages%20here))
    ```python
    ages = read_csv(PATH_TO_CSV_FILE, test=test)
    ```
* groups images into 4 age groups, according to the age range of the specific identity
    ```python
    grouped_ages, final_dict = group_ages(ages)
    ```
* randomly takes the desired number of images from each group of each identity
    ```python
    final_dict = recover_identities(grouped_ages,final_dict)
    ```
* split previous chosen images into training, test and validation set
    ```python
    splitted_dict_samples, splitted_dict_labels = train_test_val_split(ages, final_dict)
    ```
* starting from the prevous splits (which works on images' path), recovers the corresponding images' files saving it to a specific folder
    ```python
    extract_jpgs(splitted_dict_samples, set_type)
    ```
<br/>

At this point, you have the 3 needed sets and you can pass to phase of **face extraction**, done with the script [get_bboxes_from_csv.py](face_extraction/get_bboxes_from_csv.py) launched from [its directory](face_extraction/) with
```python
python3 get_bboxes_from_csv.py
```
It recovers faces bounding boxes informations from the CSV annotation file (to be placed [here](face_annotations/CSV%20files%20for%20crop%20here)):
```python
split = row[0].split(",")
path = split[2]
dir_path, file_path = path.split("/")[0], path.split("/")[1]
id_folder = os.path.join(PATH_TO_CROPPED_TS, dir_path)
x,y = int(split[4]), int(split[5])
# if top-left point of the bbox has a negative coordinate, set it to 0 because it probably means that the face is outside the limits of the image
if x<0:
    x=0
if y<0:
    y=0
width = int(split[6])
height = int(split[7])
```
and then crop the face:
```python
crop_img = img[y:y+height, x:x+width]
if crop_img.size!=0:
    cv.imwrite(os.path.join(PATH_TO_CROPPED_TS, path), crop_img)
```
<br/>

Once cropped all sets, you can **generate the TFRecord files** using the script [create_tfrecord.py](tfrecord_management/create_tfrecord.py) which distingueshes (through the parameter _test_ to set at line 145) between test record made of record of the type:
```python
example = tf.train.Example(features=tf.train.Features(feature={'path': _bytes_feature((path).encode('utf-8')),
 'image_raw': _bytes_feature(image_string)
}))
```
and other set type record of the type:
```python
example = tf.train.Example(features=tf.train.Features(feature={
'path': _bytes_feature((path).encode('utf-8')),
'width': _int64_feature(image_shape[1]),
'height': _int64_feature(image_shape[0]),
'label': _int64_feature(int(age)),
'image_raw': _bytes_feature(image_string)
}))
```
Moreover test TFRecord creation function also write a CSV file with the age label of each test image (in order to use it on colab for evaluate the model):

```python
# write path-age to gt csv
path = jpg_dir.split(os.sep)[-2]+"/"+jpg_dir.split(os.sep)[-1]
age = ages[d]["/"+f]
csv_writer.writerow([path, age])
```
and preprocess images before writing to record, normalizing and resizing them:
```python
img = vggface2_preprocessing(img)
img = custom_resize(img, img.shape[0], img.shape[1], TARGET_SHAPE)
```
This script has to be launched from [its directory](tfrecord_management/) with the command
```python
python3 create_tfrecord.py
```
Well done! TFRecords are created successfully!

## **DCNN model and training**