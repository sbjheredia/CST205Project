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
    
    elif filter == 'brightness':
        postBrightness = 1.3
        for p in image.getdata():
            if int(p[0] * postBrightness) > 255:
                red = 255
            else:
                red = int(p[0] * postBrightness)
            if int(p[1] * postBrightness) > 255:
                green = 255
            else:
                green = int(p[1] * postBrightness)
            if int(p[2] * postBrightness) > 255:
                blue = 255
            else:
                blue = int(p[2] * postBrightness)

            pixel_rgb_list.append((red, green, blue))
        filtered_image.putdata(pixel_rgb_list)

        return filtered_image
    
    elif filter == 'contrast':
        postContrast = 1.1
        for p in image.getdata():
            baseline = p[0]
            if baseline == 0:
                baseline = 1
            
            redRatio = baseline / baseline
            greenRatio = p[1] / baseline
            blueRatio = p[2] / baseline

            if int(p[0] * postContrast * redRatio) > 255:
                red = 255
            else:
                red = int(p[0] * postContrast * redRatio)

            if int(p[1] * postContrast * greenRatio) > 255:
                green = 255
            else:
                green = int(p[1] * postContrast * greenRatio)

            if int(p[2] * postContrast * blueRatio) > 255:
                blue = 255
            else:
                blue = int(p[2] * postContrast * blueRatio)

            pixel_rgb_list.append((red, green, blue))
        filtered_image.putdata(pixel_rgb_list)

        return filtered_image
    
    elif filter == 'blur':
        width, height = image.width, image.height
        small_image = Image.new('RGB', (width // 4, height // 4))

        for source_x in range(0, width - 1, 4):
            for source_y in range(0, height - 1, 4):
                pixel = image.getpixel((source_x, source_y))
                small_image.putpixel((source_x // 4, source_y // 4), pixel)

        filtered_image = small_image.resize((width, height), Image.NEAREST)

        return filtered_image



            


def resize(image):
    desired_height = 300 # change this to mess with the size of images

    scaling_factor = desired_height / image.height
    width, height = int(image.width * scaling_factor) , int(image.height * scaling_factor)
    resized_image = image.resize((width, height), Image.Resampling.LANCZOS)

    return resized_image