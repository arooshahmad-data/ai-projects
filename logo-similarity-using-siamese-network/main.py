import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Lambda
from tensorflow.keras.optimizers import RMSprop
from model import create_base_network, euclidean_distance
from load_data import load_images_from_folder

# Load images
folder = "K:\Project\Data\LLD-logo_sample"  # replace with your folder path
images = load_images_from_folder(folder)

# Create pairs and labels
def create_pairs_and_labels(images):
    num_images = len(images)
    pairs = []
    labels = []

    for i in range(num_images):
        # Positive pair
        pairs.append([images[i], images[(i+1)%num_images]])
        labels.append(1)

        # Negative pair
        pairs.append([images[i], images[(i+2)%num_images]])
        labels.append(0)

    return np.array(pairs), np.array(labels)

pairs, labels = create_pairs_and_labels(images)

# Create model
input_shape = images.shape[1:]
base_network = create_base_network(input_shape)
input_a = Input(shape=input_shape)
input_b = Input(shape=input_shape)
processed_a = base_network(input_a)
processed_b = base_network(input_b)
distance = Lambda(euclidean_distance)([processed_a, processed_b])
model = Model([input_a, input_b], distance)

# Compile model
rms = RMSprop(learning_rate=0.001)
model.compile(loss='binary_crossentropy', optimizer=rms, metrics=['accuracy'])

# Train model
model.fit([pairs[:, 0], pairs[:, 1]], labels, epochs=10)


# Save model
model.save_weights('siamese_model_weights.h5')
