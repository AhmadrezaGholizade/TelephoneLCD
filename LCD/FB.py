from PIL import Image
import numpy as np

class FrameBuffer:
    def __init__(self, device="/dev/fb0", width=128, height=48):
        self.device = device
        self.width = width
        self.height = height
    
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