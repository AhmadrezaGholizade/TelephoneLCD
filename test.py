from PIL import Image
from LCD.FB import FrameBuffer

fb = FrameBuffer()

# Load and resize image manually
img = Image.open("test.png")
img = img.resize((fb.width, fb.height), Image.LANCZOS)
fb.write(img)

# Or let write() handle resizing automatically
img = Image.open("test.png")
fb.write(img)