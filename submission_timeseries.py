# -*- coding: utf-8 -*-
"""SUBMISSION TIMESERIES.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qcQdZu3aRG9sPrOHVizbJnBUH8Ui3uca

<h1>NAMA : DENI PRIYADI
<h1> NIM : 191410038
<H1> Alamat : Kabupaten Majalengka
"""

import zipfile
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv('/content/drive/MyDrive/DICODING/DATASET/Air Pollution Forecasting - LSTM Multivariate/LSTM-Multivariate_pollution.csv')

df.info()

df.head()

df.tail()

df = df.drop(['dew', 'temp', 'press', 'wnd_dir', 'wnd_spd', 'snow', 'rain'], axis=1)

plt.figure(figsize=(15,5))
plt.plot(df['pollution'])
plt.xlabel('Date', fontsize = 15)
plt.ylabel('Polusi', fontsize = 15)
plt.show()

df['date'] = pd.to_datetime(df['date'])

# Set 'tanggal' as the index
df.set_index('date', inplace=True)
new_df2 = df.resample('D').mean()

plt.figure(figsize=(15,5))
plt.plot(new_df2['pollution'])
plt.xlabel('Date', fontsize = 15)
plt.ylabel('Polusi', fontsize = 15)
plt.show()

scaller = MinMaxScaler(feature_range=(0,1))
new_df2[new_df2.columns] = scaller.fit_transform(new_df2)

new_df2

train = round(len(new_df2)* 0.80)
train

data_train = new_df2[:train]
data_test  = new_df2[train:]

def urutan_train_test(dataset):
                sequence = []
                label = []
                start_index = 0
                for stop_index in range(50,len(dataset)):
                    sequence.append(dataset.iloc[start_index:stop_index])
                    label.append(dataset.iloc[stop_index])
                    start_index += 1
                return (np.array(sequence),np.array(label))

train_data, label_data = urutan_train_test(data_train)
test_data, label_test = urutan_train_test(data_test)

model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(30, input_shape=(train_data.shape[1], 1), return_sequences=True),
    tf.keras.layers.LSTM(16),
    tf.keras.layers.Dense(5, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.summary()

class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('mae') <= 0.05:
            print("MAE sudah mencapai threshold")
            self.model.stop_training = True

model.compile(loss=tf.keras.losses.Huber(),
              optimizer='adam',
              metrics=["mae"])

history = model.fit(train_data,
                    label_data,
                    epochs=25,
                    validation_data=(test_data, label_test),
                    batch_size = 64,
                    callbacks=[myCallback()])

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

import matplotlib.image as mimg
import matplotlib.pyplot as plt

mae = (history.history['mae'])
val_mae = (history.history['val_mae'])
loss = (history.history['loss'])
val_loss = (history.history['val_loss'])

plt.figure(figsize = (16,8))
plt.subplot(1,2,1)

plt.plot(mae, label = 'Akurasi mae')
plt.plot(val_mae, label = 'Akurasi validasi')
plt.title = ('mae and Validation mae')
plt.xlabel('Epoch')
plt.ylabel('mae')
plt.legend(loc = 'upper right')

plt.subplot(1,2,2)
plt.plot(loss, label = 'Loss Training')
plt.plot(val_loss, label = 'Loss validasi')
plt.title = ('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('loss')
plt.legend(loc = 'upper right')

plt.show()

