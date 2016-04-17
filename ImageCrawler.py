from Crawler import Crawler
from PIL import Image
from cStringIO import StringIO
import time
import random

class ImageCrawler(Crawler):
    def __init__(self, request_url):
        Crawler.__init__(self, request_url)

    def crop_by_diff(self, df_top, df_right, df_bottom, df_left):
        original_file = StringIO(self.read)
        original = Image.open(original_file)

        width, height = original.size   # Get dimensions
        left = df_left
        top = df_top
        right = width - df_right
        bottom = height - df_bottom
        cropped_image = original.crop((left, top, right, bottom))
        temp = self.url.split("/")
        cropped_image.save(temp[len(temp)-1])

    def crop_by_size(self, new_width, new_height):
        original_file = StringIO(self.read)
        original = Image.open(original_file)

        width, height = original.size   # Get dimensions
        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = width - left
        bottom = height - top
        cropped_image = original.crop((left, top, right, bottom))
        temp = self.url.split("/")
        cropped_image.save(temp[len(temp)-1])

    def resize(self, new_width, new_height, keepRatio, cropped):
        original_file = StringIO(self.read)
        original = Image.open(original_file)

        if keepRatio:
            width, height = original.size   # Get dimensions
            if cropped:
                if width / float(height) > new_width / float(new_height):
                    # cat theo chieu rong
                    ratio = (new_width/float(new_height))
                    temp_width = int((float(height)*float(ratio)))
                    left = (width - temp_width) / 2
                    right = width - left
                    original = original.crop((left, 0, right, height))
                elif width / float(height) < new_width / float(new_height):
                    # cat theo chieu cao
                    ratio = (new_height/float(new_width))
                    temp_height = int((float(width)*float(ratio)))
                    top = (height - temp_height) / 2
                    bottom = height - top
                    original = original.crop((0, top, width, bottom))

            width, height = original.size   # Get dimensions
            width_percent = (new_width/float(width))
            height_size = int((float(height)*float(width_percent)))
            cropped_image = original.resize((new_width, height_size), Image.ANTIALIAS)
        else:
            cropped_image = original.resize((new_width, new_height), Image.ANTIALIAS)
        return cropped_image

starting = time.time()
f = open("photo_links.txt")
image_array = [url.strip() for url in f.readlines()]
image_array_len = len(image_array)

image_width = 1920 * 4
image_height = 1080 * 3
thumbnail_width = 480
thumbnail_height = 360
ratio = image_width / thumbnail_width
background = Image.new('RGBA', (image_width, image_height), (255, 255, 255, 255))
for i in xrange((image_width * image_height) / (thumbnail_width * thumbnail_height)):
    if i < image_array_len:
        image_file = image_array[i]
    else:
        image_file = image_array[random.randint(0, image_array_len)]
    in_req = ImageCrawler(image_file)
    thumbnail = in_req.resize(thumbnail_width, thumbnail_height, True, True)
    offset = (thumbnail_width * (i % ratio), thumbnail_height * (i / ratio))
    background.paste(thumbnail, offset)
background.save("wallpaper.jpg")

ending = time.time()
difference = int(ending - starting)
print "It takes {} seconds".format(difference)