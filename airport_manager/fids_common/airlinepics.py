import os

from PIL import ImageTk, Image 


def _get_airline_logo(iata):
    if os.path.isfile(os.path.join('airline_logos', iata+".png")):
        pass