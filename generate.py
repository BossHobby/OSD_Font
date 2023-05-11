import os

from wand.color import Color
from wand.image import Image

char_width = 12
char_height = 18
char_count_width = 16
char_count_height = 32

source_file = "source/QUIC.svg"
source_dpi = 48

hdzero_output_path = "hdzero/QUIC.bmp"
hdzero_bg_color = Color('rgb(127, 127, 127)')

dji_output_path = "dji/font_quic%s.bin"
dji_scale = 3
dji_hd_output_path = "dji/font_quic_hd%s.bin"
dji_hd_scale = 2
dji_bg_color = Color('transparent')

ws_output_path = "walksnail/WS_QUIC_%d.png"
ws_bg_color = Color('transparent')

def generate_hdzero():
    with Image(filename=source_file, background=hdzero_bg_color) as img:
        with img.convert('BMP3') as output_img:
            os.makedirs(os.path.dirname(hdzero_output_path), exist_ok=True)
            print("generating %s" % hdzero_output_path)
            output_img.save(filename=hdzero_output_path)
 

def generate_dji(output_path, scale):
    glyphs = []
    with Image(filename=source_file, resolution=source_dpi*scale, background=dji_bg_color) as img:
        for y in range(char_count_height):
            for x in range(char_count_width):
                pixels = img.export_pixels(x * scale * char_width, y * scale * char_height, scale * char_width, scale * char_height, 'RGBA')
                glyphs.append(bytes(pixels))

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
    glyphs = []
    with Image(filename=source_file, resolution=source_dpi*scale, background=ws_bg_color) as img:
        for y in range(char_count_height):
            for x in range(char_count_width):
                pixels = img.export_pixels(x * scale * char_width, y * scale * char_height, scale * char_width, scale * char_height, 'RGBA')
                glyphs.append(pixels)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with Image(width=scale * char_width, height=len(glyphs) * scale * char_height, background=ws_bg_color) as img:
        for i, g in enumerate(glyphs):
            img.import_pixels(0, i * scale * char_height, scale * char_width, scale * char_height, 'RGBA', 'char', g)
        print("generating %s" % output_path)
        img.save(filename=output_path)


generate_hdzero()
generate_dji(dji_output_path, dji_scale)
generate_dji(dji_hd_output_path, dji_hd_scale)
generate_ws(ws_output_path % 24, 2)
generate_ws(ws_output_path % 36, 3)