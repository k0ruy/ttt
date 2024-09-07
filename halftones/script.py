import numpy as np
from PIL import Image, ImageOps, ImageDraw

def image_to_halftone_inverted(image_path, dot_size=10, output_path='halftone_image.png', white_threshold=230):
    # Load image and convert to grayscale
    img = Image.open(image_path)
    img = ImageOps.grayscale(img)
    
    # Resize image to reduce the resolution
    img_resized = img.resize((img.width // dot_size, img.height // dot_size), Image.BILINEAR)
    
    # Convert to numpy array
    img_array = np.array(img_resized)
    
    # Create a blank black image for the halftone output (inverted, background black)
    halftone_image = Image.new('L', img.size, color=255)
    draw = ImageDraw.Draw(halftone_image)
    
    # Iterate through the resized image pixels and draw corresponding white dots
    for y in range(img_array.shape[0]):
        for x in range(img_array.shape[1]):
            # Pixel intensity (0 is black, 255 is white)
            pixel_intensity = img_array[y, x]

            # Skip if the pixel intensity is close to white
            if pixel_intensity >= white_threshold:
                continue
            
            # Radius is proportional to the pixel intensity (lighter areas have larger dots)
            radius = pixel_intensity / 255 * dot_size
            
            # Calculate the center of the dot
            center_x = x * dot_size + dot_size // 2
            center_y = y * dot_size + dot_size // 2
            
            if radius > 0:
                draw.ellipse(
                    (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
                    fill=0  # White color for dots
                )
    
    
    # Save the halftone image
    halftone_image.save(output_path)
    return output_path

def image_to_halftone_tattoo(image_path, dot_size=10, output_path='halftone_image_tattoo.png', white_threshold=230, spacing_factor=2, threshold=10):
    # Load image and convert to grayscale
    img = Image.open(image_path)
    img = ImageOps.grayscale(img)
    
    # Resize image to reduce the resolution, scaling down based on the spacing factor
    img_resized = img.resize((img.width // 2 // spacing_factor, img.height // 2 // spacing_factor), Image.BILINEAR)
    
    # Convert to numpy array
    img_array = np.array(img_resized)
    
    # Create a larger blank white image for the embroidery output (scaling the size by the spacing factor)
    image = Image.new('L', (img.width, img.height), color=255)
    draw = ImageDraw.Draw(image)
    
    # Iterate through the resized image pixels and draw corresponding stitches, skipping white areas
    for y in range(img_array.shape[0]):
        for x in range(img_array.shape[1]):
            # Pixel intensity (0 is black, 255 is white)
            pixel_intensity = img_array[y, x]
            
            # Skip if the pixel intensity is close to white
            if pixel_intensity >= white_threshold:
                continue
            
            # Length of the "stitch" is proportional to the pixel intensity
            radius = int(pixel_intensity / 255 * 10) * 2 > threshold

            # Calculate the center of the dot
            center_x = x * 2 * spacing_factor + (2 // 2) 
            center_y = y * 2 * spacing_factor + (2 // 2)
            
            if radius:
                draw.ellipse(
                    (center_x - dot_size, center_y - dot_size, center_x + dot_size, center_y + dot_size),
                    fill=0  # White color for dots
                )
            

    # Save the spaced embroidery image
    image.save(output_path)
    return output_path

def image_to_embroidery(image_path, stitch_size=10, output_path='embroidery_image_no_spacing.png', white_threshold=230):
    # Load image and convert to grayscale
    img = Image.open(image_path)
    img = ImageOps.grayscale(img)
    
    # Resize image to reduce the resolution, scaling down based on the spacing factor
    img_resized = img.resize((img.width // stitch_size, img.height // stitch_size), Image.BILINEAR)
    
    # Convert to numpy array
    img_array = np.array(img_resized)
    
    # Create a larger blank white image for the embroidery output (scaling the size by the spacing factor)
    embroidery_image = Image.new('L', (img.width, img.height), color=255)
    draw = ImageDraw.Draw(embroidery_image)
    
    # Iterate through the resized image pixels and draw corresponding stitches, skipping white areas
    for y in range(img_array.shape[0]):
        for x in range(img_array.shape[1]):
            # Pixel intensity (0 is black, 255 is white)
            pixel_intensity = img_array[y, x]
            
            # Skip if the pixel intensity is close to white
            if pixel_intensity >= white_threshold:
                continue
            
            # Length of the "stitch" is proportional to the pixel intensity
            stitch_length = pixel_intensity / 255 * stitch_size
            
            # Calculate the start and end points of the stitch with added spacing factor
            start_x = x * stitch_size 
            start_y = y * stitch_size
            end_x = start_x + stitch_length
            end_y = start_y + stitch_length
            
            # Draw diagonal "stitches" (cross-stitch style) in black on a white background
            draw.line((start_x, start_y, end_x, end_y), fill=0)  # Black color stitch
            draw.line((start_x, end_y, end_x, start_y), fill=0)  # Second diagonal stitch
    
    # Save the spaced embroidery image
    embroidery_image.save(output_path)
    return output_path

def image_to_embroidery_spacing(image_path, stitch_size=10, output_path='embroidery_image.png', white_threshold=230, spacing_factor=2):
    # Load image and convert to grayscale
    img = Image.open(image_path)
    img = ImageOps.grayscale(img)
    
    # Resize image to reduce the resolution, scaling down based on the spacing factor
    img_resized = img.resize((img.width // stitch_size // spacing_factor, img.height // stitch_size // spacing_factor), Image.BILINEAR)
    
    # Convert to numpy array
    img_array = np.array(img_resized)
    
    # Create a larger blank white image for the embroidery output (scaling the size by the spacing factor)
    embroidery_image = Image.new('L', (img.width, img.height), color=255)
    draw = ImageDraw.Draw(embroidery_image)
    
    # Iterate through the resized image pixels and draw corresponding stitches, skipping white areas
    for y in range(img_array.shape[0]):
        for x in range(img_array.shape[1]):
            # Pixel intensity (0 is black, 255 is white)
            pixel_intensity = img_array[y, x]
            
            # Skip if the pixel intensity is close to white
            if pixel_intensity >= white_threshold:
                continue
            
            # Length of the "stitch" is proportional to the pixel intensity
            stitch_length = pixel_intensity / 255 * stitch_size
            
            # Calculate the start and end points of the stitch with added spacing factor
            start_x = x * stitch_size * spacing_factor
            start_y = y * stitch_size * spacing_factor
            end_x = start_x + stitch_length
            end_y = start_y + stitch_length
            
            # Draw diagonal "stitches" (cross-stitch style) in black on a white background
            draw.line((start_x, start_y, end_x, end_y), fill=0)  # Black color stitch
            draw.line((start_x, end_y, end_x, start_y), fill=0)  # Second diagonal stitch
    
    # Save the spaced embroidery image
    embroidery_image.save(output_path)
    return output_path

# Example usage
image_path = 'input/flower.jpg'
# image_to_halftone_tattoo(image_path, dot_size=1, spacing_factor=2, threshold=8)

image_to_embroidery(image_path, stitch_size=4, white_threshold=215)