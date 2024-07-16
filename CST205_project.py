from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap
from random import shuffle
from PIL import Image
import os
import shutil

# test
#boom test again

app = Flask(__name__)
bootstrap = Bootstrap(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#images will go in this list
gallery_images = []


if os.path.exists(UPLOAD_FOLDER):
    shutil.rmtree(UPLOAD_FOLDER)
os.makedirs(UPLOAD_FOLDER)


@app.route('/')
def home():
    '''
        uploaded photos are to be turned into GalleryImage objects
        and used to populate gallery_images here I think

        So we'd have the code to handle the forms and uploading of
        the images here. maybe idkslacj
    '''
    gallery_images = []
    return render_template('home.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return redirect(request.url)
    
    files = request.files.getlist('files')
    
    if not files or files[0].filename == '':
        return redirect(request.url)
    
    for file in files:
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            gallery_images.append(GalleryImage(filepath, "example title", Image.open(filepath)))


    
    return render_template('home.html', message="Image Uploaded!")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/gallery')
def gallery():
    return render_template('gallery.html', files=gallery_images)


class GalleryImage:
    '''
        a class that represents the images
        that are to be sent to the gallery

        image is a Pillow Image object
    '''
    # If we want to add more details, they'll go here
    # def __init__(self, image, title, description, filter, frame):
    #     self.image = image
    #     self.title = title
    #     self.description = description
    #     self.filter = filter
    #     self.frame = frame

    def __init__(self, source, title, image):
        self.image = image
        self.source = source
        self.title = title
