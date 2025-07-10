import os
import csv


def find_images_without_texts(main_folder, csv_file):
    """
    Given a main folder path, appends "images" and "texts" to the path to create the images and texts paths.
    Calculates the total number of images that have corresponding text files.
    Finds the names of images that do not have corresponding text files.
    Saves the names of images without corresponding text files to a CSV file.

    Args:
        main_folder (str): Path to the main folder containing "images" and "texts" folders.

    Returns:
        None
    """
    images_path = os.path.join(main_folder, 'images')
    texts_path = os.path.join(main_folder, 'texts')

    image_files = [f for f in os.listdir(images_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
    text_files = [f for f in os.listdir(texts_path) if f.endswith('.txt')]

    text_file_names = {os.path.splitext(f)[0] for f in text_files}

    images_without_texts = []
    total_images_with_texts = 0

    for image in image_files:
        image_name = os.path.splitext(image)[0]
        if image_name in text_file_names:
            total_images_with_texts += 1
        else:
            images_without_texts.append(image)

    # Save the names of images without corresponding text files to a CSV file
    with open(csv_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Image Name'])
        for image in images_without_texts:
            csvwriter.writerow([image])

    print(f"Total number of images with corresponding text files: {total_images_with_texts}")
    print(f"Names of images without corresponding text files have been saved to: {csv_file}")


# Example usage
main_folder = 'D:/verification tool/Data/distribution4'
csv_path = "D:/verification tool/Data/distribution4.csv"
find_images_without_texts(main_folder, csv_path)
