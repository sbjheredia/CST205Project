from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from random import shuffle
from PIL import Image
import os

# test
#boom test again

app = Flask(__name__)
bootstrap = Bootstrap5(app)

gallery_images = []

@app.route('/')
def home():
    '''
        uploaded photos are to be turned into GalleryImage objects
        and used to populate gallery_images here I think

        So we'd have the code to handle the forms and uploading of
        the images here. maybe idk
    '''
    return render_template('home.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html', images=gallery_images)


class GalleryImage:
    '''
        a class that represents the images
        that are to be sent to the gallery

        image is a Pillow Image object
    '''
    # If we want to add more details, they'll go here
    def __init__(self, image, title, description, filter, frame):
        self.image = image
        self.title = title
        self.description = description
        self.filter = filter
        self.frame = frame
