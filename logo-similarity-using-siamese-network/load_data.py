import os
from PIL import Image
import numpy as np

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(".png"):  # check if the file is a PNG image
            img = Image.open(os.path.join(folder, filename))
            if img is not None:
                img_resized = img.resize((224, 224))  # resize image to 224x224
                img_array = np.array(img_resized)  # convert image to numpy array
                images.append(img_array)
    images = np.array(images)
    return images
