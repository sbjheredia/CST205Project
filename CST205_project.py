from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_bootstrap import Bootstrap
from PIL import Image
import os
import shutil

app = Flask(__name__)
bootstrap = Bootstrap(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#images will go in this list
gallery_images = []

# This function makes sure the uploads folder is primed
def initialize_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    elif os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)
        os.makedirs(UPLOAD_FOLDER)

# Root url
@app.route('/')
def home():
    initialize_upload_folder()
    gallery_images = []

    return render_template('home.html')

# Url for gallery. Renders gallery.html and gives it a list of images
@app.route('/gallery')
def gallery():
    gallery_images = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            gallery_images.append(filename)
    return render_template('gallery.html', images=gallery_images)


# This handles the file upload system
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and (file.filename.endswith('.jpg') or file.filename.endswith('.png')):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        # TODO
        '''
            As it is now, the raw images the user uploads are placed into
            the uploads folder. This is done in the file.save(file_path) below.
            I believe we want to turn the image into a Pillow image first, so
            we can modify it (resize, apply filters, etc.) before we place it
            into the uploads folder.

            The way I think we should do this is as follows.

            1. This function is called in home.html so we should take data from
            text fields there and modify the function to take that data as
            parameters. For example if they pick to put a sepia filter we'd
            pass a parameter that can be used in an if statement

            2. Now that we have that data available here, we can call a function
            here that turns the image into a Pillow image and applies the needed
            modifications.

            3. Once that is done we can then place that new image into uploads and
            continue like normal and it'll show properly on the gallery
        '''
        # PROPOSED FUNCTION GOES HERE
        
        file.save(file_path)
        return jsonify({'success': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400


# This is so that the html page can properly source the image location
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)