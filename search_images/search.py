from clarifai.rest import ClarifaiApp
from clarifai.rest.client import TokenError
import json
import math
import time
import os
import heapq
from collections import defaultdict

def get_image_urls():
    image_urls = []

    # Read images file
    with open("images.txt", "r") as images_file:
        image_urls = images_file.read().splitlines()
    return image_urls

'''
Tag images using Clarifai API Python Client
Expecting json response from clarifai:
{
    "output":[
        {
          "input":{
            "data":{
              "image":{
                "url": "..."
              }
            }
          },
          "data":{
            "concepts":[
                {
                    "name": "...",
                    "value" "..."
                },
                ...
                ...
                ...
            ]
          }
        },
        ...
        ...
    ]
}
'''
def get_images_by_tag(image_urls, clientId, clientSecret, batch_size=128, n=10):
    app = ClarifaiApp(clientId, clientSecret)

    # Image data store
    # Key: tag
    # Value: list of image url and tag value
    images_by_tag = defaultdict(list)
    err_count = 0

    print "Tagging {} images...".format(len(image_urls))
    for i in range(int(math.ceil(len(image_urls) / (batch_size * 1.0)))):
        # Let Clarifai do its magic
        this_batch = image_urls[i * batch_size:(i + 1) * batch_size]
        tag_data = app.tag_urls(this_batch)

        # Parse response
        if "outputs" not in tag_data:
            print "Warning: failed on {} batch".format(i)
            err_count += len(this_batch)
        else:
            for t in tag_data["outputs"]:
                try:
                    image_url = t["input"]["data"]["image"]["url"]
                    for concept in t["data"]["concepts"]:
                        tag_name = concept["name"]
                        tag_value = concept["value"]

                        if len(images_by_tag[tag_name]) < n:
                            heapq.heappush(images_by_tag[tag_name], (tag_value, image_url))
                        elif tag_value > images_by_tag[tag_name][0]:
                            heapq.heappushpop(images_by_tag[tag_name], (tag_value, image_url))

                except KeyError:
                    err_count += 1

    if err_count != 0:
        print "Warning: Failed to processing {} images".format(err_count)

    for tag_name in images_by_tag:
        images_by_tag[tag_name] = [str(key[1]) for key in sorted(images_by_tag[tag_name], reverse=True)]

    return images_by_tag

def main():
    image_urls = get_image_urls()
    clientId = os.getenv('CLARIFAI_APP_ID')
    clientSecret = os.getenv('CLARIFAI_APP_SECRET')
    BATCH_SIZE = 128
    NUM_OF_IMAGES_PER_TAG = 10

    start = time.time()

    try:
        # Get sorted list of at most 10 of the most probable images for each tag
        image_data_store = get_images_by_tag(image_urls, clientId, clientSecret, BATCH_SIZE, NUM_OF_IMAGES_PER_TAG)
    except TokenError as e:
        print "Fail to get token from Clariai using environment variables 'CLARIFAI_APP_ID' and 'CLARIFAI_APP_SECRET':"
        print e
        return

    print "Process completed in {} seconds. Start searching now!".format(time.time() - start)
    while True:
        try:
            search_tag = raw_input("Enter tag name: ")
            if search_tag == "":
                break
            if search_tag in image_data_store:
                print image_data_store[search_tag] 
            else:
                print "No image found for " + search_tag
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()