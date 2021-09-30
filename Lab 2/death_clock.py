import time
from datetime import date
from time import strftime
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
big_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

birth_pile = 0
death_pile = 0
quarter_secs = 0
row_size = 110


while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # fractional time
    quarter_secs += 1
    if (quarter_secs >= 4):
        quarter_secs = 0

    # Birth Count
    draw.text((0, 0), 'Births', font=big_font, fill="#FFFFFF")
    birth_date = date(1165, 1, 1)
    birth_days = (date.today() - birth_date).days
    birth_seconds = birth_days * 86400
    birth_seconds += int(time.time()) % 86400
    birth_count = birth_seconds * 4
    birth_count += 1
    '{:,}'.format(birth_count)
    draw.text((0, 30), f'{birth_count:,}', font=font, fill="#FFFFFF")
    # Pile
    birth_pile += 1
    if (birth_pile > 110 * 85):
        birth_pile = 0
        death_pile = 0
    a = int(birth_pile / row_size)
    draw.rectangle((0, 134-a, row_size, 135), outline=0, fill="#FFFFFF") # completed rows
    draw.rectangle((0, 133-a, birth_pile%row_size, 135-a), outline=0, fill="#FFFFFF") # current row
    draw.text((min(birth_pile%row_size, 85), 118-a), str(birth_pile), font=font, fill="#FFFFFF")

    # Death Counter
    draw.text((120, 0), 'Deaths', font=big_font, fill="#FF000000")
    death_date = date(415,1,1)
    death_days = (date.today() - death_date).days
    death_seconds = death_days * 86400
    death_seconds += int(time.time()) % 86400
    death_count = death_seconds * 2
    death_count += 1 if quarter_secs % 2 == 0 else 0
    '{:,}'.format(death_count)
    draw.text((120, 30), f'{death_count:,}', font=font, fill="#FF0000")
    # Pile
    death_pile += 1 if quarter_secs % 2 == 0 else 0
    b = int(death_pile / row_size)
    draw.rectangle((120, 134-b, 120+row_size, 135), outline=0, fill="#FF0000") # completed rows
    draw.rectangle((120, 133-b, 120+death_pile%row_size, 135-b), outline=0, fill="#FF0000") # current row

    draw.text((min(death_pile%row_size + 120, 205), 118-b), str(death_pile), font=font, fill="#FF0000")

    # Display image.
    disp.image(image, rotation)
    time.sleep(0.25)
