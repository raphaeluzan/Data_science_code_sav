#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 22:23:59 2019

@author: raphaeluzan
"""

import numpy as np
import matplotlib.pyplot as plot  # créer des graph
import pandas as pd  # manipuler les donnes facilement 

#jeu d entraînement
# création d un dataframe grâce a panda 
# on selection la cologne open 

#Jeu de donee data 
dataset_train = pd.read_csv("/Users/raphaeluzan/Desktop/deep_learning_finance/google_stock_price_train.csv", delimiter=';')


training_set= dataset_train[["Open"]].values

#crochet   .value transforme ca en array 
# feature scaling


from sklearn.preprocessing import MinMaxScaler

sc = MinMaxScaler(feature_range= (0,1))
training_set_scaled = sc.fit_transform(training_set)

#creation de la structure avec 60 timesteps = x train #et 1 sortie = Y train 
X_train = []
y_train = []
for i in range(60,1006):
    X_train.append(training_set_scaled[(i-60): i, 0])
    y_train.append(training_set_scaled[i,0])
X_train = np.array(X_train)
y_train = np.array(y_train)
# rechape les données

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

#partie 2
#librairie 

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout 

Regressor = Sequential()
# couche lstm +dropout
Regressor.add(LSTM(units=50, return_sequences=True, input_shape= (X_train.shape[1], 1 )))
Regressor.add(Dropout( 0.2))
# 2 âme couche lstm
Regressor.add(LSTM(units=50, return_sequences=True)),
Regressor.add(Dropout( 0.2))
 #3 âme couche 
Regressor.add(LSTM(units=50, return_sequences=True))
Regressor.add(Dropout( 0.2))
 #4eme couche 
Regressor.add(LSTM(units=50))
Regressor.add(Dropout( 0.2))
# couche de sortie
Regressor.add(Dense(units= 1))

#compilation 
Regressor.compile(optimizer = "adam", loss= "mean_squared_error")
# entrainement
Regressor.fit(X_train, y_train, epochs=100, batch_size= 32)
# prend 20 min a tourner c est trop long 

#partie3 
dataset_test = pd.read_csv("/Users/raphaeluzan/Desktop/deep_learning_finance/google_stock_price_train.csv", delimiter=';')

real_stock_price= dataset_test[["Open"]].values
#predictions de 2017

dataset_train
dataset_test
dataset_total = pd.concat((dataset_train["Open"], dataset_test["Open"]), axis= 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60 :].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_test = []
for i in range( 60, 80):
    X_test.append(inputs[(i-60): i,0])
X_test = np.array(X_train)
X_test = np.reshape(X_test,(X_test.shape[0], X_test.shape[1], 1))

predicted_stock_price = Regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

#Visualisation sur graph
import matplotlib.pyplot as plt
plt.plot(real_stock_price, color="red", 
              label = "Prix reel de L’action  de Google")
	
plt.plot(predicted_stock_price, color="green",  label = "Prix prédit de L’action  de Google")
plt.title("Prédiction de L’action Google")
plt.xlabel("Jour")
plt.ylabel("Prix de L’action")
plt.legend()
plt.show()

