from django.db import models
from datetime import datetime
#from sorl.thumbnail import ImageField, get_thumbnail
from PIL import Image as PIL_Image
import os

def generate_filename(self, filename):
    url = "original_image" + os.sep + "%s_%s" % (datetime.now().strftime('%Y%m%d%H%M%S'), filename)
    return url

# Create your models here.
class Image(models.Model):
    image_title = models.CharField(max_length=250)
    image_category = models.CharField(max_length=250)
    image_description = models.CharField(max_length=1000)
    image_file = models.ImageField(upload_to=generate_filename)
    image_tags = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now=True)

    def save(self, size=(200, 200)):
        if not self.id and not self.image_file:
            return

        super(Image, self).save()

        filename = str(self.image_file.path)
        image = PIL_Image.open(filename)

        image.thumbnail(size,PIL_Image.ANTIALIAS)
        #index = filename.rfind(os.sep)
        #thumbnil_file =  filename[:index]+ os.sep + "thumbnail" + filename[index:]
        thumbnil_file = filename.replace(os.sep + "original_image" + os.sep, os.sep + "thumbnail" + os.sep)
        image.save(thumbnil_file)

    def __str__(self):
        return self.image_title


class FavouriteList(models.Model):
    device_id = models.CharField(max_length=250, unique=True)
    favouriteList = models.CharField(max_length=2000)

    def __str__(self):
        return self.device_id
