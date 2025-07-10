# predict_similar_images.py

import os
import shutil
import numpy as np
from PIL import Image
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Flatten, Dense, Dropout, Lambda
from tensorflow.keras import backend as K
from load_data import load_images_from_folder

def euclidean_distance(vects):
    x, y = vects
    sum_square = K.sum(K.square(x - y), axis=1, keepdims=True)
    return K.sqrt(K.maximum(sum_square, K.epsilon()))

def create_base_network(input_shape):
    input = Input(shape=input_shape)
    x = Flatten()(input)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.2)(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.2)(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.2)(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.2)(x)
    x = Dense(128, activation='relu')(x)
    return Model(input, x)

def predict_similarities(model, images, input_image):
    num_images = len(images)
    input_image = np.expand_dims(input_image, axis=0)
    similarities = np.zeros(num_images)
    for i in range(num_images):
        pair = [np.expand_dims(images[i], axis=0), input_image]
        similarities[i] = model.predict(pair)
    return similarities

def get_top_100(similarities):
    return np.argsort(similarities)[-100:]

# Load images
folder = "K:\Project\Data\LLD-logo_sample"  # replace with your folder path
images = load_images_from_folder(folder)

# Input image
input_image = images[0]  # replace with your input image

# Create model
input_shape = images.shape[1:]
base_network = create_base_network(input_shape)
input_a = Input(shape=input_shape)
input_b = Input(shape=input_shape)
processed_a = base_network(input_a)
processed_b = base_network(input_b)
distance = Lambda(euclidean_distance)([processed_a, processed_b])
model = Model([input_a, input_b], distance)

# Load model weights
model.load_weights('siamese_model_weights.h5')

# Predict similarities
similarities = predict_similarities(model, images, input_image)

# Get top 100 similar images
top_100_indices = get_top_100(similarities)

# Save top 100 images to a new folder
output_folder = "TopHundred"
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.makedirs(output_folder)

for i, index in enumerate(top_100_indices):
    image = Image.fromarray(images[index])
    image.save(os.path.join(output_folder, f"image_{i}.png"))
