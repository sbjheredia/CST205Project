'''
Description: This file contains the function designed to create a Pillow Image
                that can be shown in the gallery
'''

from PIL import Image


def fit(src_image):
    # TODO make the text one
    image = Image.open(src_image.path)
    
    image = apply_filter(image, src_image.filter)
    image = resize(image)
    # image = put_text(image, src_image.title, src_image.description)
    # image.show()
    return image

# This function includes all the filters, decides what to apply based on argument
def apply_filter(image, filter):
    pixel_rgb_list = []
    filtered_image = Image.new('RGB', (image.width, image.height))

    if filter == 'none':
        return image

    elif filter == 'grayscale':
        for p in image.getdata():
            avg = int((p[0] + p[1] + p[2]) / 3)
            pixel_rgb_list.append((avg, avg, avg))

        filtered_image.putdata(pixel_rgb_list)

        return filtered_image

    elif filter == 'sepia':
        for p in image.getdata():
            if p[0] < 63:
                red, green, blue = int(p[0] * 1.1), p[1], int(p[2] * 0.9)
            elif p[0] > 62 and p[0] < 192:
                red, green, blue = int(p[0] * 1.15), p[1], int(p[2] * 0.85)
            else:
                red = int(p[0] * 1.08)
                green, blue = p[1], int(p[2] * 0.5)

            pixel_rgb_list.append((red, green, blue))

        filtered_image.putdata(pixel_rgb_list)

        return filtered_image
    
    elif filter == 'invert':
        for p in image.getdata():
            pixel_rgb_list.append((255-p[0], 255-p[1], 255-p[2]))

        filtered_image.putdata(pixel_rgb_list)

        return filtered_image

            


def resize(image):
    desired_height = 300 # change this to mess with the size of images

    scaling_factor = desired_height / image.height
    width, height = int(image.width * scaling_factor) , int(image.height * scaling_factor)
    resized_image = image.resize((width, height), Image.Resampling.LANCZOS)

    return resized_image