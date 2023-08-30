from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


def generate_image_file(name="image.png"):
    file = BytesIO()
    image = Image.new("RGB", (100, 100))
    image.save(fp=file, format="PNG")
    image = SimpleUploadedFile(name, file.getvalue(), content_type="image/png")

    return image
