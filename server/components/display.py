import os
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

WIDTH = 128
HEIGHT = 64
I2C_ADDR = 0x3c
BORDER = 15
FONT_PATH = "./unispace bd.ttf"

I2C = busio.I2C(board.SCL, board.SDA)


def resolve_pin(name):
    return board.__dict__[name]


def load_font(path, size):
    if os.path.exists(path):
        font = ImageFont.truetype(path, size)
    else:
        # Load default font.
        font = ImageFont.load_default()
    return font


class Display:
    def __init__(self, width=WIDTH, height=HEIGHT, SCL="SCL", SDA="SDA", addr=I2C_ADDR,
                 font_path=FONT_PATH, primary_font_size=12, secondary_font_size=40):
        self.width = width
        self.height = height
        self.i2c = busio.I2C(resolve_pin(SCL), resolve_pin(SDA))
        self.addr = addr
        self.primary_font = load_font(font_path, primary_font_size)
        self.secondary_font = load_font(font_path, secondary_font_size)
        self.primary_text = "TPaaS System"
        self.secondary_text = ""

        self.oled = adafruit_ssd1306.SSD1306_I2C(
            self.width, self.height, self.i2c, addr=60)

    def clear(self):
        self.oled.fill(0)
        self.oled.show()

    def draw(self):
        image = Image.new("1", (self.width, self.height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, self.width, 16), outline=0, fill=0)
        draw.rectangle((0, 16, self.width, self.height), outline=255, fill=255)
        draw.text((5, 0), self.primary_text, font=self.primary_font, fill=255)
        draw.text((16, 16), self.secondary_text,
                  font=self.secondary_font, fill=0)
        self.oled.image(image)
        self.oled.show()

    def message(self, primary=None, secondary=None):
        if primary is not None:
            self.primary_text = str(primary)
        if secondary is not None:
            self.secondary_text = str(secondary)
        self.draw()

    def show(self, text):
        self.message(None, text)


if __name__ == "__main__":
    d = Display()
    d.message("TPaaS Display Test", "YAY!")
