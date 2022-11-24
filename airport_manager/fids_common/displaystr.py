import json

IATA_FILE_NAME = "resources/iatacity.json"

_data_iata = dict()

def load_file_iata():
    global _data_iata
    with open(IATA_FILE_NAME, "r") as f1:
        _data_iata = json.load(f1)


def get_city(iata):
    return _data_iata.get(iata, iata)

load_file_iata()
