#!/usr/bin/env python3

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ssottori <ssottori@student.42london.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 00:12:41 by ssottori          #+#    #+#              #
#    Updated: 2024/11/21 00:18:31 by ssottori         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from os.path import isfile
from PIL import Image
from PIL.ExifTags import TAGS
from exif import Image as ExifImage
from sys import argv

IMG_TYPE = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
#argv.remove(argv[0])

def show_img_info(file):
	try:
		with Image.open(file) as img:
			print(f"{file}")
			print(f"-  Format: {img.format}")
			print(f"-  Size: {img.size}")
			print(f"-  Width: {img.width}")
			print(f"-  Height: {img.height}")
			print(f"-  Color Mode: {img.mode}")
	except Exception as e:
		print(f"Error while reading the {file}: {e}")


def exif_data(file):
	try:
		with Image.open(file) as img:
			exifs = img.getexif()
			if exifs is None:
				print(f"Sorry, image has no exif data.")
				return
			print("EXIF Data:...")
			for tag_id, value in exifs.items():
				tag_name = TAGS.get(tag_id, tag_id)
				print(f"    {tag_name:25}: {value}")
	except Exception as e:
		print(f"Error extracting EXIF data: {e}")
		

def is_valid(file):
	if not isfile(file):
		print(f"Error: {file} does not exist.")
		return False
	if not file.lower().endswith(tuple(IMG_TYPE)):
		print(f"Error: {file} is not a valid image file.")
		return False
	return True

#files = argv[1:]
#valid_f = [file for file in files if is_valid(file)]

def scorpion(file):
	for file in files:
		show_img_info(file)
		exif_data(file)
		print("-------------------")
		print("")

if __name__ == "__main__":
	files = argv[1:]
	if not files:
		print("No valid files to process.")
		exit(0)
	valid_f = [file for file in files if is_valid(file)]
	if not valid_f:
		print("No valid files to process.")
	else:
		scorpion(valid_f)