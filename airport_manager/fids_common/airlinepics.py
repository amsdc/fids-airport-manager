import os

from PIL import ImageTk, Image 

HEIGHT = 50


def get_airline_logo(iata, ht=HEIGHT):
    filename = os.path.join('airline_logos', (iata.upper())+".png")
    if not os.path.isfile(filename):
        filename = os.path.join('airline_logos', "NULL_AIRLINE.png")
    img = Image.open(filename)
    aspect_ratio = img.width / img.height

    new_height = ht
    new_width = round(new_height * aspect_ratio)

    resized_image = img.resize((new_width, new_height))

    return ImageTk.PhotoImage(resized_image)