from PIL import Image
import numpy as np

class LCDFrameBuffer:
    BACKLIGHT_PATH = "/sys/class/backlight/backlight/brightness"
    
    def __init__(self, device="/dev/fb0", width=128, height=48):
        self.device = device
        self.width = width
        self.height = height

    def screen_off(self):
        """
        Turn LCD backlight OFF
        """
        try:
            with open(self.BACKLIGHT_PATH, "w") as f:
                f.write("0")
        except Exception as e:
            print(f"Failed to turn screen off: {e}")

    def screen_on(self):
        """
        Turn LCD backlight ON
        """
        try:
            with open(self.BACKLIGHT_PATH, "w") as f:
                f.write("1")
        except Exception as e:
            print(f"Failed to turn screen on: {e}")
    
    def image_to_frame(self, image):
        """
        Convert PIL Image or pygame Surface to binary framebuffer data.
        Use threshold: grayscale < 128 -> 0x0000, else 0xFFFF.
        
        Args:
            image: PIL Image or pygame Surface
        
        Returns:
            bytes: Binary data ready to write to framebuffer
        """

        # Handle pygame Surface
        if hasattr(image, 'get_buffer'):
            import pygame
            img_str = pygame.image.tostring(image, 'RGB')
            pil_image = Image.frombytes('RGB', image.get_size(), img_str)
        else:
            pil_image = image

        # Resize to framebuffer dimensions
        pil_image = pil_image.resize((self.width, self.height), Image.LANCZOS)

        # Convert to grayscale
        pil_image = pil_image.convert('L')

        # Convert to numpy array
        img_array = np.array(pil_image, dtype=np.uint8)

        # Apply threshold: <128 -> 0x0000, >=128 -> 0xFFFF
        frame_data = bytearray()
        for y in range(self.height):
            for x in range(self.width):
                pixel = 0xFFFF if img_array[y, x] <= 128 else 0x0000
                frame_data.extend(pixel.to_bytes(2, byteorder='little'))

        return bytes(frame_data)

    
    def write(self, image):
        """
        Convert image and write directly to framebuffer.
        
        Args:
            image: PIL Image or pygame Surface
        """
        frame_data = self.image_to_frame(image)
        
        with open(self.device, "wb") as fb:
            fb.write(frame_data)
    
    def clear(self, color=0x0000):
        """
        Clear framebuffer to specified color.
        
        Args:
            color: 16-bit color value (default: black)
        """
        frame_data = bytearray()
        for _ in range(self.width * self.height):
            frame_data.extend(color.to_bytes(2, byteorder='little'))
        
        with open(self.device, "wb") as fb:
            fb.write(frame_data)

    def write_region(self, image, x, y, w, h):
        """
        Write only a specific region to framebuffer.
        
        Args:
            image: PIL Image (should be w x h size)
            x, y: Top-left position in framebuffer
            w, h: Width and height of region
        """
        # Ensure image is the right size
        if image.size != (w, h):
            image = image.resize((w, h), Image.LANCZOS)
        
        # Convert to grayscale and get pixel data
        image = image.convert('L')
        img_array = np.array(image, dtype=np.uint8)
        
        # Open framebuffer for reading and writing
        with open(self.device, "r+b") as fb:
            for row in range(h):
                # Calculate offset for this row
                offset = ((y + row) * self.width + x) * 2  # 2 bytes per pixel
                fb.seek(offset)
                
                # Convert row pixels
                row_data = bytearray()
                for col in range(w):
                    pixel = 0xFFFF if img_array[row, col] <= 128 else 0x0000
                    row_data.extend(pixel.to_bytes(2, byteorder='little'))
                
                fb.write(row_data)
    
    def toggle_region(self, x, y, w, h):
        """
        Toggle pixels in a region (invert black <-> white).
        
        Args:
            x, y: Top-left position in framebuffer
            w, h: Width and height of region to toggle
        """
        with open(self.device, "r+b") as fb:
            for row in range(h):
                # Calculate offset for this row
                offset = ((y + row) * self.width + x) * 2  # 2 bytes per pixel
                fb.seek(offset)
                
                # Read existing pixels
                existing = fb.read(w * 2)
                
                # Toggle each pixel (XOR with 0xFFFF)
                toggled = bytearray()
                for i in range(0, len(existing), 2):
                    pixel = int.from_bytes(existing[i:i+2], byteorder='little')
                    pixel ^= 0xFFFF  # XOR to invert
                    toggled.extend(pixel.to_bytes(2, byteorder='little'))
                
                # Write back
                fb.seek(offset)
                fb.write(toggled)