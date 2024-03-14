import os
import numpy as np
from PIL import Image
import zipfile
import shutil

# Grayscale Image Creation 
def createGrayImage(input_file, imgFormat='jpeg', imageSize=64, resampling_filter='BICUBIC'):
    """Creates a gray-level image from file and saves the image in temp_output folder"""
    try:
        with open(input_file, 'rb') as file:
            file_content = file.read()
            data = np.frombuffer(file_content, dtype=np.uint8)
            image_size = int(np.ceil(np.sqrt(len(data))))
            data = np.pad(data, (0, image_size**2 - len(data)), 'constant')
            data = data.reshape((image_size, image_size))
            image = Image.fromarray(data, 'L')
            resized_image = image.resize((imageSize, imageSize), getattr(Image, resampling_filter.upper()))
            temp_output_dir = 'temp_output'
            if not os.path.exists(temp_output_dir):
                os.makedirs(temp_output_dir)
            output_file_path = os.path.join(temp_output_dir, os.path.splitext(os.path.basename(input_file))[0] + "." +imgFormat)
            resized_image.save(output_file_path)

            return output_file_path

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Coloured Image Creation
def createColorImage(input_file, imgFormat='jpeg', imageSize=64, resampling_filter='BICUBIC'):
    """Creates a coloured image from file and saves the images in temp_output folder"""
    try:
        with open(input_file, 'rb') as file:
            file_content = file.read()
            data = np.frombuffer(file_content, dtype=np.uint8)
            image_size = int(np.ceil(np.sqrt(len(data) / 3)))
            data = np.pad(data, (0, image_size**2 * 3 - len(data)), 'constant')
            data = data.reshape((image_size, image_size, 3))
            image = Image.fromarray(data, 'RGB')
            resized_image = image.resize((imageSize, imageSize), getattr(Image, resampling_filter.upper()))
            temp_output_dir = 'temp_output'
            if not os.path.exists(temp_output_dir):
                os.makedirs(temp_output_dir)
            output_file_path = os.path.join(temp_output_dir, os.path.splitext(os.path.basename(input_file))[0] + "." + imgFormat)
            resized_image.save(output_file_path)

            return output_file_path

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Create zip file
def create_zip(target_directory, zip_filename):
    """Creates a zip file for all the files in the given directory and saves the zip file"""
    try:
        with zipfile.ZipFile(zip_filename, 'w') as zip_file:
            for root, _, files in os.walk(target_directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, target_directory))

        return zip_filename
    except Exception as e:
        print(f"An error occurred while creating the zip file: {e}")
        return None

# Convert the files into images
def convert_files(input_files, imgFormat, mode, imageSize, resampling_filter):
    """It takes a list of input files, creates images, and returns the zip file path"""
    try:
        for input_file in input_files:
            if (mode == 'gray'):
                resultant_image = createGrayImage(input_file, imgFormat, imageSize, resampling_filter)
            elif (mode == 'color'):
                resultant_image = createColorImage(input_file, imgFormat, imageSize, resampling_filter)

            if resultant_image is None:
                print(f"Error creating image for {input_file}")
                
        zip_filename = create_zip('temp_output', 'zip_output/output.zip')
        shutil.rmtree('temp_input', ignore_errors=True)
        shutil.rmtree('temp_output', ignore_errors=True)

        return zip_filename
            
    except Exception as e:
        print(f"An error occurred: {e}")




# Test Codes for this file

# def main():
#     input_files = ['../../Data/sample0.txt', '../../Data/sample1.pdf']
#     format = 'png'
#     mode = 'color'
#     result_zip = convert_files(input_files, format, mode)
#     print(f"Zip file created: {result_zip}")

# if __name__ == "__main__":
#     main()
