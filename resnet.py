# -*- coding: utf-8 -*-
"""ResNet

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KB96tmBYDu9Pkf0SWWvcMaxhVe3Q3Fp1

# ResNet50 - Analiz
"""

from keras.preprocessing import image
from keras.applications import resnet50
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D, Input
from keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np

batch_size = 50
num_classes = 2

base_model = resnet50.ResNet50

base_model = base_model(weights='imagenet', include_top=False)
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(num_classes, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=predictions)

for layer in base_model.layers:
    layer.trainable = False

model.compile(loss='sparse_categorical_crossentropy',
              optimizer=Adam(lr=0.0001),
              metrics=['acc'])

x_train = np.random.normal(loc=127, scale=127, size=(50, 224,224,3))
y_train = np.array([0,1]*25)
x_train = resnet50.preprocess_input(x_train)


print(model.evaluate(x_train, y_train, batch_size=batch_size, verbose=0))


history = model.fit(x_train, y_train,
          epochs=5,
          batch_size=batch_size,
          shuffle=False,
          validation_data=(x_train, y_train))

print(history.history.keys())

# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

"""## ResNet50 - NESNE TANIMA

**Gerekli paketler yükleniyor**
"""

from keras.applications import ResNet50
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
from io import BytesIO
import os
import requests

"""**ImageNet veriseti ile eğitilmiş model ve ağırlıkları yükleniyor**"""

model = ResNet50(weights="imagenet")

"""**Resmi girişe uygun formata getirmek için yeniden boyutlandırma fonksiyonu tanımlanıyor**"""

def prepare_image(image, target):
	# resize the input image and preprocess it
	image = image.resize(target)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	image = imagenet_utils.preprocess_input(image)

	# return the processed image
	return image

"""**Sınıflandırma istediğiniz resmin web adresini aşağıdaki giriş alanına giriniz.**"""

ImageURL = "https://www.mailce.com/wp-content/uploads/2012/12/atlar-2.jpg" #@param {type:"string"}

"""**Girilen web adresinden resim indiriliyor**"""

response = requests.get(ImageURL)
image = Image.open(BytesIO(response.content))
image

"""**Eğitilmiş model ile sınıflandırma yapılıyor.**"""

data = {"success": False}

pre_image = prepare_image(image, target=(224, 224))

preds = model.predict(pre_image)

results = imagenet_utils.decode_predictions(preds)
data["predictions"] = []


for (imagenetID, label, prob) in results[0]:
  r = {"label": label, "probability": float(prob)}
  data["predictions"].append(r)
  
data["success"] = True

print(data)

"""**Sınıflandırma sonuçları.**"""

print("Sınıflandırma tahmini en yüksek olan {0} oranıyla {1}'dır.".format(data["predictions"][0]["probability"],data["predictions"][0]["label"]))