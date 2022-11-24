import tkinter.font as tkFont

import toml

THEME_FILE_NAME = "themes/default.toml"

current_theme = {}

def load_theme(theme_name=THEME_FILE_NAME):
    global current_theme
    with open(theme_name) as f:
        current_theme = toml.load(f)


def get_style(style_name):
    return current_theme["style_name"]
    

def get_font(style):
    fontname = style["font"].get("family")
    fontsize = style["font"].get("size")
    wt = "bold" if style["font"].get("bold") else "normal"
    slnt = style["font"].get("slant")
    undr = style["font"].get("underline", 0)
    ovst = style["font"].get("overstrike", 0)
    return tkFont.Font(family=fontname,
                       size=fontsize,
                       weight=wt,
                       slant=slnt,
                       underline=undr,
                       overstrike=ovst)

def get_label_attr(style):
    psty = style.get("padding", {})
    pady = str(psty.get("y", 0))+"p"
    padx = str(psty.get("x", 0))+"p"
    return dict(font=get_font(style),
                fg=style["foreground"],
                bg=style["background"],
                borderwidth=style["borderwidth"],
                anchor=style.get("anchor"),
                padx=padx,
                pady=pady)


def get_grid_attr(style):
    return dict(sticky=style["grid"]["sticky"],
                padx=style["grid"]["padding"]["x"],
                pady=style["grid"]["padding"]["y"])

def get_style(name):
    return current_theme.get(name, {})
                

# load_theme()
