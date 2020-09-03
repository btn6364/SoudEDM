from PIL import Image, ImageTk

def resize_images(image_paths):
    resized_images = []
    for image_path in image_paths:
        image = Image.open(image_path)
        image = image.resize((50, 50), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        resized_images.append(photo)
    return resized_images
