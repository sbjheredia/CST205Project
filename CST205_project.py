from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_bootstrap import Bootstrap
from PIL import Image
from util import fit
from util import apply_filter as apply_preview_filter
import os
import shutil
import base64
from io import BytesIO

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
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg') or filename.lower().endswith('.png'):
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
    
    if file and (file.filename.lower().endswith('.jpg') or file.filename.lower().endswith('.jpeg') or file.filename.lower().endswith('.png')):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        title = request.form['title']
        description = request.form['description']
        filter_option = request.form['filter']
        
        file.save(file_path)

        modified_image = fit(GalleryImage(file_path, title, description, filter_option))
        modified_image.save(file_path)

        return jsonify({'success': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400
    

# This deals with applying filters to the preview image
@app.route('/apply_filter', methods=['POST'])
def apply_filter():
    if 'image_data' not in request.form:
        return jsonify({'error': 'No image data'}), 400

    image_data = request.form['image_data']
    filter_type = request.form['filter']

    image_data = image_data.split(",")[1]
    image = Image.open(BytesIO(base64.b64decode(image_data)))

    if image.mode == 'RGBA':
        image = image.convert('RGB')

    filtered_image = apply_preview_filter(image, filter_type)

    buffered = BytesIO()
    filtered_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    img_data = f"data:image/jpeg;base64,{img_str}"

    return jsonify({'filtered_image_url': img_data})


# This is so that the html page can properly source the image location
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

class GalleryImage:
    ''' a class that represents the images in the gallery '''
    def __init__(self, path, title, description, filter):
        self.path = path
        self.title = title
        self.description = description
        self.filter = filter