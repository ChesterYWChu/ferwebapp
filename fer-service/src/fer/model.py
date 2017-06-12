from keras.models import load_model
from keras.preprocessing import image
from flask import current_app
import tensorflow as tf
import numpy as np
import sys
import os
import cv2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Usage: python model.py croppedface_gray.jpg
# (0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Neutral)
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
batch_size = 1
img_width = 48
img_height = 48

face_cascade = cv2.CascadeClassifier(BASE_DIR + '/haarcascade_frontalface_default.xml')
fer_model = load_model(BASE_DIR + '/classifier_batch200_augmented_val_acc_0.5305.h5')
graph = tf.get_default_graph()

def predict(img_file):
	msg = ''
	predictions = []

	img = image.load_img(img_file, grayscale=True)
	img = image.img_to_array(img)
	img = np.array(img, dtype='uint8')
	faces = face_cascade.detectMultiScale(img, 1.3, 5)
	current_app.logger.info('Found %s face(s) by face_cascade.' % len(faces))

	if len(faces) == 0:
		msg = 'No face is found!'
		return msg, predictions
	else:
		faces = sorted(faces, key=lambda face: face[3], reverse=True)
		(x,y,w,h) = faces[0]
		img = img[y:y+h, x:x+w]

	x = cv2.resize(img, (img_width, img_height))
	x = x.reshape((1, 48, 48, 1))
	x = x / 255.0

	global graph
	with graph.as_default():
		predictions = fer_model.predict(x, batch_size=batch_size)
	results = decode_predictions(predictions)

	if results[0][0][0] == 0:
		msg = 'It is an \"Angry\" face!'
	else:
		msg = 'It is a \"%s\" face!' % results[0][0][1]
	predictions = [{'label': label, 'description': description, 'probability': probability * 100.0}
                    for label, description, probability in results[0]]
	return msg, predictions

def decode_predictions(predictions):
	result = []
	for pred in predictions:
		row = []
		for i in range(len(pred)):
			row.append((i, emotions[i], pred[i]))
		row = sorted(row, key=lambda r: r[2], reverse=True)
		result.append(row)
	return result

if __name__ == "__main__":
	predictions = predict(sys.argv[1])
	print(predictions)





