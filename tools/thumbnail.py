# usr/bin/env python
# -*- coding: utf-8 -*-
import os
from PIL import Image
from django.conf import settings


def get_thumb_size(image, thumb_width=None, thumb_height=None):
    width, height = image.size
    if thumb_width and thumb_height is None:
        thumb_height = int((thumb_width/width) * height)
    elif thumb_width is None and thumb_height:
        thumb_width = int((thumb_height/height) * width)
    elif thumb_width is None and thumb_height is None:
        if width < 320:
            return width, height
        else:
            thumb_width = int(width/2)
            thumb_height = int((thumb_width/width) * height)
    return thumb_width, thumb_height


def generate_thumbnail(image, thumb_width=None, thumb_height=None, store_dir=None):
    image_name, image_ext = os.path.splitext(os.path.basename(image.name))
    image = Image.open(image)
    thumb_size = get_thumb_size(image, thumb_width, thumb_height)
    if image.mode not in ('L', 'RGB'):
        if image.mode == 'RGBA':
            # 透明图片需要加白色底
            image.load()
            alpha = image.split()[3]
            bg = alpha.point(lambda x: 255 - x)
            image = image.convert('RGB')
            image.paste((255, 255, 255), None, bg)
        else:
            image = image.convert('RGB')

    thumb = image.resize(thumb_size, Image.ANTIALIAS)
    if store_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        store_dir = os.path.join(base_dir, 'thumbs').replace('\\', '/')
    filename = os.path.join(store_dir, image_name + '_thumb' + image_ext).replace('\\', '/')
    thumb.save(filename, quality=95)
