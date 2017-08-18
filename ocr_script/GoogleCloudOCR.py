#!/usr/bin/env python

"""
This script is to test Google Cloud Vision OCR (text detect) API

Example CLI:
> python GoogleCloudOCR.py ./ch4_test/

Notice: need to create folders out_file, out_file3, out_file4 before run this.
"""

# for CLI parameter
import argparse

# for seraching folder and file IO
import base64
import os
import re
import sys

# for accessing Google Cloud API
from googleapiclient import discovery
from googleapiclient import errors
from oauth2client.client import GoogleCredentials

is_verbose = False
do_show = False
if do_show:
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg

# [START detect_text]
DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'  # noqa
BATCH_SIZE = 10


class VisionApi:
    """Construct and use the Google Vision API service."""

    def __init__(self, api_discovery_file='vision_api.json'):
        self.credentials = GoogleCredentials.get_application_default()
        self.service = discovery.build(
            'vision', 'v1', credentials=self.credentials,
            discoveryServiceUrl=DISCOVERY_URL)

    def detect_text(self, input_filenames, num_retries=3, max_results=6):
        """Uses the Vision API to detect text in the given file.
        """
        images = {}
        for filename in input_filenames:
            with open(filename, 'rb') as image_file:
                images[filename] = image_file.read()

        batch_request = []
        for filename in images:
            batch_request.append({
                'image': {
                    'content': base64.b64encode(
                            images[filename]).decode('UTF-8')
                },
                'features': [{
                    'type': 'TEXT_DETECTION',
                    'maxResults': max_results,
                }]
            })
        request = self.service.images().annotate(
            body={'requests': batch_request})

        try:
            responses = request.execute(num_retries=num_retries)
            if 'responses' not in responses:
                return {}
            text_response = {}
            for filename, response in zip(images, responses['responses']):
                if 'error' in response:
                    print("API Error for %s: %s" % (
                            filename,
                            response['error']['message']
                            if 'message' in response['error']
                            else ''))
                    continue
                if 'textAnnotations' in response:
                    text_response[filename] = response['textAnnotations']
                else:
                    text_response[filename] = []
            return text_response
        except errors.HttpError as e:
            print("Http Error for %s: %s" % (filename, e))
        except KeyError as e2:
            print("Key error: %s" % e2)
# [END detect_text]



# [START get_text]
def get_text_from_files(vision, input_filenames, input_dir):
    """Call the Vision API on a file. """
    texts = vision.detect_text(input_filenames)
    len_dir = len(input_dir)
    for filename, text in texts.items():
        # create result file for each image
        import codecs
        out_file = './outfile_1/' + 'res_' + filename[len_dir : -3] + 'txt'
        csvfile = codecs.open(out_file, 'wb', 'UTF-8')
        out_file3 = './outfile_3/' + 'res_' + filename[len_dir : -3] + 'txt'
        csvfile3 = codecs.open(out_file3, 'wb', 'UTF-8')
        out_file4 = './outfile_4/' + 'res_' + filename[len_dir : -3] + 'txt'
        csvfile4 = codecs.open(out_file4, 'wb', 'UTF-8')
        if len(text) <= 1:
            print "===================="
            print "file name: %s\n" % (filename)
            print "detect nothing!"
            continue

        for e in text[1:]:
            try:
                vertices = []
                for bound in e['boundingPoly']['vertices']:
                    x, y = bound['x'], bound['y']
                    if x <= 0:
                        print('file name: {}:  x = {} < 0'.format(filename, x))
                        x = 1
                    elif x >= 1280:
                        print('file name: {}:  x = {} > 1280'.format(filename, x))
                        x = 1279
                    if y <= 0:
                        print('file name: {}:  y = {} < 0'.format(filename, y))
                        y = 1
                    elif y >= 1280:
                        print('file name: {}:  y = {} > 1280'.format(filename, y))
                        y = 1279
                    vertices.append(str(x) + ',' + str(y))

            except KeyError, er:
                print "===================="
                print "file name: %s\n" % (filename)
                print('Key Error: {}'.format(er))
                print e['boundingPoly']['vertices']
                continue
            out_str = [e['description']]
            csvfile.write(','.join(vertices)+'\r\n')
            csvfile3.write(filename[len_dir+1:] + ',' + e['description'] + '\r\n')
            #out_str.extend(vertices)
            vertices.extend(out_str)
            csvfile4.write(','.join(vertices)+'\r\n')
            if is_verbose:
                print('{}'.format(','.join(out_str)))
        csvfile.close()
        csvfile3.close()
        csvfile4.close()


def batch(iterable, batch_size=BATCH_SIZE):
    """Group an iterable into batches of size batch_size.

    >>> tuple(batch([1, 2, 3, 4, 5], batch_size=2))
    ((1, 2), (3, 4), (5))
    """
    b = []
    for i in iterable:
        b.append(i)
        if len(b) == batch_size:
            yield tuple(b)
            b = []
    if b:
        yield tuple(b)


def main(input_dir):
    """Walk through all the not-yet-processed image files in the given
    directory, extracting any text from them and adding that text to an
    inverted index.
    """
    # Create a client object for the Vision API
    vision = VisionApi()

    allfileslist = []
    # Recursively construct a list of all the files in the given input
    # directory.
    for folder, subs, files in os.walk(input_dir):
        for filename in files:
            allfileslist.append(os.path.join(folder, filename))

    fileslist = []
    for filename in allfileslist:
        fileslist.append(filename)

    for filenames in batch(fileslist):
        get_text_from_files(vision, filenames, input_dir)
# [END get_text]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Detects text in the images in the given directory.')
    parser.add_argument(
        'input_directory',
        help='the image directory you\'d like to detect text in.')
    args = parser.parse_args()

    main(args.input_directory)

    if do_show:
        image = mpimg.imread('./test_img/IMG_0531.JPG')
        plt.imshow(image,cmap='gray')
        plt.show()

