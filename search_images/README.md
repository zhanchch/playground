# Search images by tag

This is a MVP that will:

	* Tag each image found in './images.txt' file using Clarifai API Python Client
	* Provide a very simple interface that repeatedly reads from STDIN in a string tag name and returns a sorted list of at most 10 of the most probable images.


Installation
---------------------
This program requires

	* Python 2.7
	* Clarifai API Python client

To install Python 2.7 please refer: https://www.python.org/download/releases/2.7/

To insatll Clarifai API Python client
```
pip install clarifai==2.0.18
```

Getting Started
---------------------
This program uses "CLARIFAI_APP_ID" and "CLARIFAI_APP_SECRET" environment variables to get an access token. Please replace "{clientId}" and "{clientSecret}" with your id and secret respectively.

Run program with
```
CLARIFAI_APP_ID={clientId} CLARIFAI_APP_SECRET={clientSecret} python search.py 
```
Program will prompt "Enter tag name: " when it's done processing the images, this will take couple minutes.

Program will repeatedly read from STDIN in a string tag name and returns a sorted list of at most 10 of the most probable images.

Program will terminate when an empty string is received.

Running with Docker
---------------------
This program uses "CLARIFAI_APP_ID" and "CLARIFAI_APP_SECRET" environment variables to get an access token. Please replace "{clientId}" and "{clientSecret}" with your id and secret respectively.

Run program with docker
```
docker build -t clarifai_search_images .
docker run -e CLARIFAI_APP_ID={clientId} -e CLARIFAI_APP_SECRET={clientSecret} -it clarifai_search_images
```
Program will prompt "Enter tag name: " when it's done processing the images, this will take couple minutes.

Program will repeatedly read from STDIN in a string tag name and returns a sorted list of at most 10 of the most probable images.

Program will terminate when an empty string is received.
