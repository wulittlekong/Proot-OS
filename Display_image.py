import time
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

if len(sys.argv) < 2:
		sys.exit("Require an image argument")
else:
		image_file = sys.argv[1]

#Matrix Configuration
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.gpio_slowdown = 2
options.brightness=100
options.led_rgb_sequence = 'rbg'

matrix = RGBMatrix(options = options)

# automatically resizing images
def preprocess_frame(frame, width, height):
    """Resize frame to fit while centering it on a black canvas."""
    frame_rgb = frame.convert("RGB")
    frame_rgb.thumbnail((width, height), Image.LANCZOS)
    
    # Create black canvas and center frame
    canvas = Image.new("RGB", (width, height), (0, 0, 0))
    x_offset = (width - frame_rgb.width) // 2
    y_offset = (height - frame_rgb.height) // 2
    canvas.paste(frame_rgb, (x_offset, y_offset))
    return canvas

# Process input file
try:
    img = Image.open(image_file)
except Exception as e:
    sys.exit(f"Failed to open image file: {e}")

# Pre-process all frames and store durations
frames = []
is_animated = getattr(img, "is_animated", False)

if is_animated:
    for frame in ImageSequence.Iterator(img):
        processed_frame = preprocess_frame(frame, matrix.width, matrix.height)
        # Fallback to 100ms delay if 'duration' metadata is missing or zero
        duration = frame.info.get("duration", 100) / 1000.0
        if duration <= 0:
            duration = 0.1
        frames.append((processed_frame, duration))
else:
    processed_frame = preprocess_frame(img, matrix.width, matrix.height)
    frames.append((processed_frame, 1.0))

try:
    print("Matrix active. Press Ctrl+C to exit.")
    
    # Pre-create double buffer canvas for smoother playback
    double_buffer = matrix.CreateFrameCanvas()

    if is_animated:
        while True:
            for frame_canvas, duration in frames:
                start_time = time.time()
                
                double_buffer.SetImage(frame_canvas)
                double_buffer = matrix.SwapOnVSync(double_buffer)
                
                # Sleep for the remaining frame duration to keep proper timing
                elapsed = time.time() - start_time
                sleep_time = duration - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)
    else:
        # Static image: render once and hold
        matrix.SetImage(frames[0][0])
        while True:
            time.sleep(100)

except KeyboardInterrupt:
    matrix.Clear()
    sys.exit(0)