import os

from wand.color import Color
from wand.image import Image

source_dpi = 48
char_width = 12
char_height = 18

font_file = "source/Font.svg"
font_height = 32 # in char sizes
font_width = 16 # in char sizes

logo_file = "source/Logo.svg"
logo_height = 4 # in char sizes
logo_width = 24 # in char sizes

hdzero_output_path = "hdzero/QUIC.bmp"
hdzero_scale = 2
hdzero_bg_color = Color('rgb(127, 127, 127)')

dji_output_path = "dji/font_quic%s.bin"
dji_scale = 3
dji_hd_output_path = "dji/font_quic_hd%s.bin"
dji_hd_scale = 2
dji_bg_color = Color('transparent')

ws_output_path = "walksnail/WS_QUIC_%d.png"
ws_bg_color = Color('transparent')

def extract_glyphs(scale, background):
    glyphs = []
    with Image(filename=font_file, resolution=source_dpi*scale, background=background) as img:
        for y in range(font_height):
            for x in range(font_width):
                pixels = img.export_pixels(x * scale * char_width, y * scale * char_height, scale * char_width, scale * char_height, 'RGBA')
                glyphs.append(bytes(pixels))
    
    with Image(filename=logo_file, resolution=source_dpi*scale, background=background) as img:
        for y in range(logo_height):
            for x in range(logo_width):
                pixels = img.export_pixels(x * scale * char_width, y * scale * char_height, scale * char_width, scale * char_height, 'RGBA')
                glyphs[font_width * 10 + y*logo_width + x] = bytes(pixels)

    return glyphs


def generate_hdzero(output_path, scale):
    glyphs = extract_glyphs(scale, hdzero_bg_color)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with Image(width=font_width * scale * char_width, height=font_height * scale * char_height, background=hdzero_bg_color) as img:
        for y in range(font_height):
            for x in range(font_width):
                img.import_pixels(x * scale * char_width, y * scale * char_height, scale * char_width, scale * char_height, 'RGBA', 'char', glyphs[y * font_width + x])
    
        with img.convert('BMP3') as output_img:
            print("generating %s" % output_path)
            output_img.save(filename=output_path)
 

def generate_dji(output_path, scale):
    glyphs = extract_glyphs(scale, dji_bg_color)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path % '', "wb") as f:
        print("generating %s" % f.name)
        for i in range(256):
            f.write(glyphs[i])

    with open(output_path % '_2', "wb") as f:
        print("generating %s" % f.name)
        for i in range(256, 512):
            f.write(glyphs[i])


def generate_ws(output_path, scale):
    glyphs = extract_glyphs(scale, ws_bg_color)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with Image(width=scale * char_width, height=len(glyphs) * scale * char_height, background=ws_bg_color) as img:
        for i, g in enumerate(glyphs):
            img.import_pixels(0, i * scale * char_height, scale * char_width, scale * char_height, 'RGBA', 'char', g)
        print("generating %s" % output_path)
        img.save(filename=output_path)


generate_hdzero(hdzero_output_path, hdzero_scale)
generate_dji(dji_output_path, dji_scale)
generate_dji(dji_hd_output_path, dji_hd_scale)
generate_ws(ws_output_path % 24, 2)
generate_ws(ws_output_path % 36, 3)