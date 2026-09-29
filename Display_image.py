import time
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

if len(sys.argv) < 2:
		sys.exit("Require an image argument")
else:
		image_file = sys.argv[1]
		
image = Image.open(image_file)

#Matrix Configuration
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.gpio_slowdown = 60
options.brightness=100

matrix = RGBMatrix(options = options)

# Make image fit screen
image.thumbnail((matrix.width, matrix.height), Image.LANCZOS)

# Create a 64x32 image canvas
#image = Image.new("RGB", (64, 32))
#draw = ImageDraw.Draw(image)

# Draw a red rectangle border and blue cross lines
#draw.rectangle((0, 0, 63, 31), outline=(255, 0, 0))
#draw.line((0, 0, 63, 31), fill=(0, 0, 255), width=1)
#draw.line((0, 31, 63, 0), fill=(0, 0, 255), width=1)

# Push cavas to screen
matrix.SetImage(image.convert('RGB'))

try:
	print("Matrix active. Press Ctrl+C to exit.")
	while True:
		time.sleep(100)
except KeyboardInterrupt:
	sys.exit(0)

