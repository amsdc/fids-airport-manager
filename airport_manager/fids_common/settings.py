import os
import configparser

SETTINGS_FILE_NAME = "fids.cfg"
DEFAULT_SETTINGS = {
    "auth": {
        "autologin": False,
        "host": "localhost",
        "user": "root",
        "database": "fids",
    },
    "client": {"poll_update": 5000},
}

settings = configparser.ConfigParser()
# Default settings
settings.read_dict(DEFAULT_SETTINGS)


def write():
    with open(SETTINGS_FILE_NAME, "w") as f:
        settings.write(f)


def _read_config():
    settings.read(SETTINGS_FILE_NAME)


def read_config():
    if not os.path.isfile(SETTINGS_FILE_NAME):
        write()
    _read_config()


def getstring(section, option, default=configparser._UNSET):
    return settings.get(section, option, vars=DEFAULT_SETTINGS, fallback=default)


def getint(section, option, default=configparser._UNSET):
    return settings.getint(section, option, vars=DEFAULT_SETTINGS, fallback=default)


def getfloat(section, option, default=configparser._UNSET):
    return settings.getfloat(section, option, vars=DEFAULT_SETTINGS, fallback=default)


def getbool(section, option, default=configparser._UNSET):
    return settings.getboolean(section, option, vars=DEFAULT_SETTINGS, fallback=default)


def get(section, option, default=configparser._UNSET):
    st = getstring(section, option, default)
    if st.isdigit():
        return getint(section, option, default)
    elif st.count(".") == 1 and st.replace(".", "").isdigit():
        return getfloat(section, option, default)
    elif st.lower() in ("true", "false"):
        return getbool(section, option, default)
    else:
        return st


def set(section, option, value):
    if type(value) == bool:
        value = str(value).lower()
    elif type(value) != str:
        value = str(value)

    try:
        settings.set(section, option, value)
    except configparser.NoSectionError:
        settings.add_section(section)
        set(section, option, value)
    else:
        write()


# main work - autoread cfg on import
read_config()
