"""Funções para tratamento de imagens."""
import io
import numpy as np
from bson.objectid import ObjectId
from gridfs import GridFS
from PIL import Image


def recorta_imagem(image, coords, pil=False):
    """Recebe uma imagem serializada em bytes, retorna Imagem cortada.

    Params:
        image: imagem em bytes (recebida via http ou via Banco de Dados)
        coords: (x0,y0,x1,y1)
        pil: flag, retorna objeto PIL se True

    Returns:
        Um recorte da imagem em bytes ou formato PIL.Image se PIL=true

    """
    if coords:
        PILimage = Image.open(io.BytesIO(image))
        im = np.asarray(PILimage)
        im = im[coords[0]:coords[2], coords[1]:coords[3]]
        PILimage = Image.fromarray(im)
        if pil:
            return PILimage
        image_bytes = io.BytesIO()
        PILimage.save(image_bytes, 'JPEG')
        image_bytes.seek(0)
    return image_bytes


def mongo_image(db, image_id):
    """Lê imagem do Banco MongoDB. Retorna None se ID não encontrado."""
    fs = GridFS(db)
    _id = ObjectId(image_id)
    if fs.exists(_id):
        grid_out = fs.get(_id)
        image = grid_out.read()
        return image
    return None


def get_imagens_recortadas(db, _id):
    images = []
    image = mongo_image(db, _id)
    if image:
        preds = db['fs.files'].find_one({'_id': _id}).get(
            'metadata').get('predictions')
        if preds:
            for pred in preds:
                bbox = pred.get('bbox')
                if bbox:
                    try:
                        image = recorta_imagem(image, bbox, True)
                        images.append(image)
                    except:
                        pass
    return images
