'''
Description: This file contains the function designed to create a Pillow Image
                that can be shown in the gallery
'''

from PIL import Image, ImageDraw, ImageFont
import textwrap


def fit(src_image):
    # TODO make the text one
    image = Image.open(src_image.path)

    if image.mode == 'RGBA':
        image = image.convert('RGB')
    
    image = resize(image)
    image = apply_filter(image, src_image.filter)
    image = put_text(image, src_image.title, src_image.description)
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

        acting_width = width - (width % 4)
        acting_height = height - (height % 4)

        for source_x in range(0, acting_width, 4):
            for source_y in range(0, acting_height, 4):
                pixel = image.getpixel((source_x, source_y))
                small_image.putpixel((source_x // 4, source_y // 4), pixel)

        filtered_image = small_image.resize((width, height), Image.NEAREST)
        return filtered_image


def resize(image):
    desired_height = 1000 # change this to mess with the size of images

    scaling_factor = desired_height / image.height
    width, height = int(image.width * scaling_factor) , int(image.height * scaling_factor)
    resized_image = image.resize((width, height), Image.Resampling.LANCZOS)

    return resized_image

def put_text(image, title, description):
    draw = ImageDraw.Draw(image)

    font_path = 'static/fonts/LibraSans.ttf'
    font_desc = ImageFont.truetype(font_path, 40)
    font_title = ImageFont.truetype(font_path, 60)
    
    # center title
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    title_position = ((image.width - title_width) // 2, 10)
    
    # outline text vibe
    outline_width = 4  # Width of the outline
    for x_offset in (-outline_width, 0, outline_width):
        for y_offset in (-outline_width, 0, outline_width):
            if x_offset != 0 or y_offset != 0:
                draw.text((title_position[0] + x_offset, title_position[1] + y_offset), title, font=font_title, fill="black")
    draw.text(title_position, title, font=font_title, fill="white")
    
    # Description on bottom with semi-working wrapping
    max_width = image.width - 20  
    sample_text = "A" * 10
    sample_text_bbox = draw.textbbox((0, 0), sample_text, font=font_desc)
    char_width = (sample_text_bbox[2] - sample_text_bbox[0]) / 10
    chars_per_line = max_width // char_width
    
    wrapped_description = textwrap.wrap(description, width=int(chars_per_line))  
    line_height = sample_text_bbox[3] - sample_text_bbox[1]  
    y_text = image.height - 20 - len(wrapped_description) * (line_height + 2) 
    
    # outline description vibe
    for line in wrapped_description:
        for x_offset in (-outline_width, 0, outline_width):
            for y_offset in (-outline_width, 0, outline_width):
                if x_offset != 0 or y_offset != 0:
                    draw.text((10 + x_offset, y_text + y_offset), line, font=font_desc, fill="black")
        
        draw.text((10, y_text), line, font=font_desc, fill="white")
        y_text += line_height + 2  # move to next line
    
    return image
