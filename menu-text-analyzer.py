#!python3.7
import io
import os
import json
import glob
from PIL import Image


# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

client = vision.ImageAnnotatorClient()
image_list = []

## First run this code after adding images to the menu images 
# folder and then comment it out
with open('menu-entities.txt', 'a') as file:
    count = 0
    # Reads all the files in the menu_images folder
    for filename in glob.glob('menu_images/*.*'): 
        print(count)
        count += 1

        # Gets the files absolute path
        file_name = os.path.abspath(filename)

        # Loads the image's data into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)

        try:
            # Reads the text from image data with Google's Cloud Vision API
            response = client.text_detection(image=image)
            texts = response.text_annotations

            # Concatinates all the individual text into one string and adds it the the menu entitites file
            full_text = '\n '.join([text.description for text in texts])
            jsonl_text = {"text_snippet": {"content": full_text}}
            file.write("\n")
            file.write(json.dumps(jsonl_text))
            print("Added to file")
        except:
            # If an error occurs reading the menu, skip the menu
            continue

## Then uncomment and run this code:
# data_type = 'train' # train, test, validation
# file_number_offset = 62 # one higher than the current largest number file
# file = open('menu-entities.txt', 'r')
# lines = file.readlines()

# # Get's the text json from the menu entities file
# for index, line in enumerate(lines):
#     menu_file = open('menu_text_files/{}/{}.txt'.format(data_type, 'menu_text_' + str(index+file_number_offset)), 'a')
#     line_json = json.loads(line)
#     texts = line_json["text_snippet"]["content"].split('\n')
#     # Adds the text to it's own file with the name of its index 
#     for text in texts:
#         menu_file.write(text)
#         menu_file.write('\n')
#     menu_file.close()
# file.close()