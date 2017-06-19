# Face Expression Recognition

[GitHub Link](https://github.com/ChesterYWChu/ferwebapp)

A face expression recognition web app powered by Deep Learning model training technique. A simple [web page](https://fer-project-170115.appspot.com/) using python Flask framework was deployed to the Google Cloud Platform for demo purpose. The data of the Kaggle challenge, [fer2013](https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/data), was used in the recognition model as training data. For now, the model is able to recognise the following 7 face expressions.

1. Angry
2. Disgust
3. Fear
4. Happy
5. Sad
6. Surprise
7. Neutral

![](http://gdurl.com/BwEf)

### Demo Page Link
[https://fer-project-170115.appspot.com/](https://fer-project-170115.appspot.com/)

### Used Tools
* Flask
* Keras
* TensorFlow
* OpenCV
* Docker
* Google App Engine
* Google Compute Engine
* Google Bucket Storage
* Nginx
* Gunicorn
* Supervisord


## Model Training

Deep Learning Library Keras with TensorFlow backend was used to specify and fill the neural network, and the network was optimised using Stochastic Gradient Descent with RMSProp optimiser.

Source Code: [https://github.com/ChesterYWChu/fer2013](https://github.com/ChesterYWChu/fer2013)

### Training Data
The training data was downloaded from a Kaggle facial expression challenge which consists of a number of 48x48 pixel grayscale face images. The face images were labeled from 0 to 6, representing 7 different emotions. There are totally 28790 training examples and 3589 test examples. Note that the disgust image examples are randomly rotated, shifted, sheared and zoomed within a limited range to increase the number of examples from 436 to 4360 to match the about numbers of other emotion examples.

* Data Download Link
[Challenges in Representation Learning: Facial Expression Recognition Challenge](https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/data)

* Number of Data Used
	* Angry - 3995
	* Disgust - 436 (Augmented to 4360 examples)
	* Fear - 4097
	* Happy - 7215
	* Sad - 4830
	* Surprise - 3171
	* Neutral - 4965
* Augmentation
```python
datagen = ImageDataGenerator(
	        rotation_range=30,
	        width_shift_range=0.1,
	        height_shift_range=0.1,
	        shear_range=0.2,
	        zoom_range=0.2,
	        horizontal_flip=True,
	        fill_mode='nearest')
```

### Model Structure
The model is start with 3 convolution network layers where each layer is followed by a 2*2 pooling layer. After that, a dense layer with 64 nodes followed by another 7 nodes dense layer were used as the final layers in the model.

```python
model = Sequential()
	model.add(Conv2D(32, (3, 3), input_shape=input_shape))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Conv2D(32, (3, 3)))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Conv2D(64, (3, 3)))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Flatten())
	model.add(Dense(64))
	model.add(Activation('relu'))
	model.add(Dropout(0.5))

	model.add(Dense(7))
	model.add(Activation('softmax'))
	
	model.compile(loss='categorical_crossentropy',
	              optimizer='rmsprop',
	              metrics=['accuracy'])

	early_stopping_monitor = EarlyStopping(monitor='val_loss', patience=5)
```

## Web App
The app is consist of two components. A frontend server hosted in a Google App Engine, and a recognition service server hosted in a docker container in a Google Compute Engine.

![](http://gdurl.com/tXLz)

### Frontend Server
The frontend server responsible for uploading user submitted images to a Google Bucket Storage, querying the recognition service server for the prediction of the image and showing the image with the prediction results to the user.

### Recognition Service Server
The server is hosted in a standard google compute engine, n1-standard-1. The incoming network traffic to its 80 port will be redirected into the docker container running on it. The container with a locally tested running environment image installed will take the http request as a input, decode the image from the payload, make a prediction base on the image using the pre-trained model, and finally return the prediction results back as a JSON string.
