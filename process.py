import os
import io
from rembg import remove
from PIL import Image

input_folder = "images"
output_folder = "outputs"
os.makedirs(output_folder, exist_ok=True)

valid_exts = (".jpg", ".jpeg", ".png", ".webp", ".avif")

canvas_size = (2048, 2048)
bg_color = "#F6F6F6"
fill_ratio = 0.75  # image will take up 75% of canvas

for filename in os.listdir(input_folder):
    if filename.lower().endswith(valid_exts):
        input_path = os.path.join(input_folder, filename)
        output_name = os.path.splitext(filename)[0] + ".png"
        output_path = os.path.join(output_folder, output_name)

        print(f"Processing {filename} → {output_name}")

        # Remove background
        with open(input_path, "rb") as f:
            raw_img = f.read()
        result = remove(raw_img)

        # Load processed image
        img = Image.open(io.BytesIO(result)).convert("RGBA")

        # Create canvas
        bg = Image.new("RGBA", canvas_size, bg_color)

        # Target box size (75% of canvas)
        max_w = int(canvas_size[0] * fill_ratio)
        max_h = int(canvas_size[1] * fill_ratio)

        # Scale proportionally (always upscale or downscale)
        scale = min(max_w / img.width, max_h / img.height)
        new_w = int(img.width * scale)
        new_h = int(img.height * scale)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # Center position
        x = (canvas_size[0] - new_w) // 2
        y = (canvas_size[1] - new_h) // 2
        bg.paste(img, (x, y), img)

        bg.save(output_path, "PNG")

print("✅ All done! Check the 'outputs' folder.")

