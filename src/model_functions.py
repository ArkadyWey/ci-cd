import numpy as np

import tensorflow as tf
from tensorflow.keras import Input
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dropout, Dense


def get_keras_model():
    return tf.keras.Sequential(
        [
                Input(shape=(28, 28, 1)),
                Conv2D(32, kernel_size=(3, 3), activation='relu'),
                MaxPooling2D(pool_size=(2, 2)),
                Conv2D(64, kernel_size=(3, 3), activation="relu"),
                MaxPooling2D(pool_size=(2, 2)),
                Flatten(),
                Dropout(rate=0.5),
                Dense(10, activation="softmax"),
        ]
    )


def get_training_set():
  (x_train, y_train), (_, _) = tf.keras.datasets.mnist.load_data()
  x_train = x_train.astype('float32') / 255
  x_train = np.expand_dims(x_train, -1)
  x_train = x_train[:256]
  y_train = tf.keras.utils.to_categorical(y_train, 10)
  y_train = y_train[:256]

  return x_train, y_train


def fit_model(model, x_train, y_train):
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    loss = tf.keras.losses.CategoricalCrossentropy()

    model.compile(loss=loss, optimizer=optimizer, metrics=["accuracy"])
    model.fit(x_train, y_train, batch_size=128, epochs=1, validation_split=0.1)