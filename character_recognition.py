# -*- coding: utf-8 -*-
"""Character_Recognition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17MJtLbEWjWUrYA9V-XUEmaSwmbGEpJ9n
"""

import tensorflow as tf
from keras.utils import np_utils
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

#Initialize train, val and test arrays
x_train = np.empty([1,28,28], dtype="uint8")
y_train = np.empty(1, dtype="uint8")
x_val = np.empty([1,28,28], dtype="uint8")
y_val = np.empty(1, dtype="uint8")
x_test = np.empty([1,28,28], dtype="uint8")
y_test = np.empty(1, dtype="uint8")

from google.colab import drive
drive.mount('/content/gdrive')

#!unzip -uq "path/folder(0)" -d "path/"

import os
from PIL import Image

def load_images_to_data(image_label, image_directory, features_data, label_data, ext):
    list_of_files = os.listdir(image_directory)
    for file in list_of_files:
        image_file_name = image_directory + "/" + file
        if ext in image_file_name:
            img = Image.open(image_file_name).convert("L")
            img = np.resize(img, (28,28,1))
            im2arr = np.array(img)
            im2arr = im2arr.reshape(1,28,28,1)
            features_data = np.append(features_data, np.squeeze(im2arr,axis=3), axis=0)
            label_data = np.append(label_data, [image_label], axis=0)
    return features_data, label_data

letter_dict = {
    "10" : "A",
    "11" : "B",
    "12" : "C",
    "13" : "D",
    "14" : "E",
    "15" : "F",
    "16" : "G",
    "17" : "H",
    "18" : "I",
    "19" : "J",
    "20" : "K",
    "21" : "L",
    "22" : "M",
    "23" : "N",
    "24" : "O",
    "25" : "P",
    "26" : "Q",
    "27" : "R",
    "28" : "S",
    "29" : "T",
    "30" : "U",
    "31" : "V",
    "32" : "W",
    "33" : "X",
    "34" : "Y",
    "35" : "Z",
}

test_letter_dict = {
    "10" : "A",
    "11" : "B",
    "12" : "C",
    "13" : "D",
    "14" : "E",
    "15" : "F",
    "16" : "G",
    "17" : "H",
    "18" : "I",
    "19" : "J",
    "21" : "L",
    "22" : "M",
    "23" : "N",
    "25" : "P",
    "27" : "R",
    "28" : "S",
    "29" : "T",
    "31" : "V",
    "33" : "X",
    "35" : "Z",
}

dir_train = "/content/gdrive/My Drive/Recognition_Dataset_Train/"
dir_val = "/content/gdrive/My Drive/Recognition_Dataset_Validation/"
dir_test = "/content/gdrive/My Drive/Recognition_Dataset_Test/"

for i in letter_dict.keys():
  x_train, y_train = load_images_to_data(i, dir_train + letter_dict[i], x_train, y_train, ".jpg")
  x_val, y_val = load_images_to_data(i, dir_val + letter_dict[i], x_val, y_val, ".jpg")

for i in range(10):
  x_train, y_train = load_images_to_data(str(i), dir_train + str(i), x_train, y_train, ".jpg")
  x_val, y_val = load_images_to_data(str(i), dir_val + str(i), x_val, y_val, ".jpg")
  x_test, y_test = load_images_to_data(str(i), dir_test + str(i), x_test, y_test, ".png")

for i in test_letter_dict.keys():
  x_test, y_test = load_images_to_data(i, dir_test + letter_dict[i], x_test, y_test, ".png")

xt_orig = x_train
yt_orig = y_train
xv_orig = x_val
yv_orig = y_val
x_orig = x_test
y_orig = y_test

x_train = xt_orig
y_train = yt_orig
x_val = xv_orig
y_val = yv_orig
x_test = x_orig
y_test = y_orig

image_index = 120 
print(y_train[image_index]) 
plt.imshow(x_train[image_index], cmap='Greys')

print(x_train.shape)
print(y_train.shape)
print(x_val.shape)
print(y_val.shape)

print(x_test.shape)
print(y_test.shape)

# Reshaping the array to 4-dims so that it can work with the Keras API
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_val = x_val.reshape(x_val.shape[0], 28, 28, 1)
input_shape = (28, 28, 1)
# Making sure that the values are float so that we can get decimal points after division
x_train = x_train.astype('float32')
x_val = x_val.astype('float32')
# Normalizing the RGB codes by dividing it to the max RGB value.
x_train /= 255
x_val /= 255
print('x_train shape:', x_train.shape)
print('Number of images in x_train', x_train.shape[0])
print('Number of images in x_val', x_val.shape[0])

from keras.models import Sequential
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D
# Creating a Sequential Model and adding the layers
def create_model():
  model = Sequential()
  model.add(Conv2D(filters=64, kernel_size=2, padding='same', activation='relu', input_shape=(28,28,1))) 
  model.add(MaxPooling2D(pool_size=2))
  model.add(Dropout(0.3))
  model.add(Conv2D(filters=32, kernel_size=2, padding='same', activation='relu'))
  model.add(MaxPooling2D(pool_size=2))
  model.add(Dropout(0.3))
  model.add(Flatten())
  model.add(Dense(256, activation='relu'))
  model.add(Dropout(0.5))
  model.add(Dense(36,activation=tf.nn.softmax))
  return model

model = create_model()
model.summary()

from keras.callbacks import ModelCheckpoint
model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy', 
              metrics=['accuracy'])
checkpoint_path = "/content/gdrive/My Drive/Checkpoints_EMNIST/cp4.ckpt"
checkpoint_dir = "/content/gdrive/My Drive/Checkpoints_EMNIST/cp4.ckpt"
cp_callback = ModelCheckpoint(filepath=checkpoint_path, save_weights_only=True, verbose=1)
history = model.fit(x=x_train,y=y_train, batch_size=1024, epochs=100, validation_data=(x_val, y_val), callbacks=[cp_callback], shuffle=True)

# Plot training & validation accuracy values
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.savefig("/content/gdrive/My Drive/Checkpoints_EMNIST/acc1.png", bbox_inches='tight')
plt.show()


# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.savefig("/content/gdrive/My Drive/Checkpoints_EMNIST/loss1.png", bbox_inches='tight')
plt.show()

model.evaluate(x_val, y_val)

image_index = 100
print(x_test[image_index].shape)
print(type(x_test[image_index]))
plt.imshow(x_test[image_index].reshape(28, 28),cmap='Greys')
pred = model.predict(x_test[image_index].reshape(1, 28, 28, 1))
print(pred.argmax())

import pathlib
data = pathlib.Path('/content/gdrive/My Drive/Recognition_Dataset_Test/Z') 
test_data = list(data.glob('*.png'))
print(test_data[0])
count = len(test_data)
count

from PIL import Image
import numpy as np
fig = plt.figure(figsize = (20, 5))
count = 0
for image_path in test_data[0:20]:
    a = Image.open(str(image_path))
    a = a.resize((28,28))
    k = np.asarray(a)
    e =  np.expand_dims(k, axis=2)
    ax = fig.add_subplot(2, 10, count+1)
    plt.imshow(k,cmap='Greys')
    pred = model.predict(e.reshape(1, 28, 28, 1))
    if(pred.argmax() > 9):
      res = letter_dict[str(pred.argmax())]
    else:
      res = pred.argmax()
    count +=1
    ax.set_title(res)

#new_model = create_model()
#new_model.load_weights("/content/gdrive/My Drive/Checkpoints_EMNIST/cp.ckpt")

xnew_val = x_test.reshape(x_test.shape[0], 28, 28, 1)
input_shape = (28, 28, 1)
xnew_val = xnew_val.astype('float32')
xnew_val /= 255
model.evaluate(xnew_val, y_test)