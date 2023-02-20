from celery import shared_task
import numpy 
from PIL import Image
import io
import blurhash
import binascii


@shared_task
def generate_image_hash(image_data):
    print('geneate method called')
    imagedata = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(imagedata)).convert(('RGB'))
    image_array = numpy.array(image)
    hash_bytes = blurhash.encode(image_array, 4, 3)
    hash_hex = binascii.hexlify(hash_bytes).decode('utf-8')
    return hash_hex

