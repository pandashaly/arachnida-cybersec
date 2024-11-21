#!/usr/bin/env python3

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ssottori <ssottori@student.42london.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 00:12:49 by ssottori          #+#    #+#              #
#    Updated: 2024/11/20 00:12:49 by ssottori         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import requests
import re
import os
import signal
import argparse
import urllib.request
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from alive_progress import alive_bar

IMG_TYPES = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
visited_urls = set()

def url_valid(url):
	parsed = urlparse(url)
	return bool (parsed.netloc) and bool(parsed.scheme)

def sig_handler(arg_1, arg_2):
	print('SIGINT received, aborting the program')
	exit(1)

def download_image(url, save_as):
	if url_valid(url):
		response = requests.get(url, stream=True)
		if (response.status_code == 200):
			os.makedirs(os.path.dirname(save_as), exist_ok=True)
			with open(save_as, 'wb') as file:
				for chunk in response.iter_content(1024):
					file.write(chunk)
			print(f"Success: URL valid - Image saved: {save_as}")
		else:
			print(f"Failed to download image: {url}")
	else:
		print(f"Invalid URL: {url}")

def extractorrr(base_url, html):
	soup = BeautifulSoup(html, "html.parser")
	image_urls = []
	for img in soup.find_all("img", src=True):
		img_url = urljoin(base_url, img["src"])
		if any(img_url.lower().endswith(ext) for ext in IMG_TYPES):
			image_urls.append(img_url)
	return image_urls

def blackwidow(url, depth, save_dir):
	if depth == 0:
		return
	print(f"Crawling: {url}, Depth: {depth}")
	try:
		response = requests.get(url)
		if response.status_code == 200:
			# Extract and download images
			image_urls = extractorrr(url, response.text)
			with alive_bar(len(image_urls), title="Downloading images") as bar:
				for img_url in image_urls:
					filename = os.path.basename(urlparse(img_url).path)
					save_path = os.path.join(save_dir, filename)
					download_image(img_url, save_path)
					bar()

			soup = BeautifulSoup(response.text, "html.parser")
			for a in soup.find_all("a", href=True):
				link = urljoin(url, a["href"])
				if url_valid(link):
					blackwidow(link, depth - 1, save_dir)
		else:
			print(f"Failed to access {url}")
	except Exception as e:
		print(f"Error crawling {url}: {e}")

def main():
	signal.signal(signal.SIGINT, sig_handler)
	parser = argparse.ArgumentParser(description="Spider Program to Download imgs.")
	parser.add_argument("url", help="URL to scrape")
	parser.add_argument("-r", action="store_true", help="Enable recursive imagage downloading")
	parser.add_argument("-l", type=int, default=5, help="Max recursion depth level (default: 5)")
	parser.add_argument("-p", default="./data/", help="Directory to save downloaded images")
	args = parser.parse_args()

	blackwidow(args.url, args.l if args.r else 0, args.p)

if __name__ == "__main__":
	main()
