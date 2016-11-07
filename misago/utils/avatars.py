from django.conf import settings
import os
from django.core.files.storage import default_storage as storage

try:
    from PIL import Image
    has_pil = True
except ImportError:
    has_pil = False

avatar_sizes = {}
def avatar_size(size):
    if not has_pil:
        return None
    try:
        return avatar_sizes[size]
    except KeyError:
        avatar_sizes[size] = None
        for i in settings.AVATAR_SIZES[1:]:
            if size <= i:
                avatar_sizes[size] = i
    return avatar_sizes[size]


def resizeimage(image, size, target, info=None, format=None):
    if isinstance(image, basestring):
        image = Image.open(image)
    if not info:
        info = image.info
    if not format:
        format = image.format
    if format == "GIF":
        if 'transparency' in info:
            image = image.resize((size, size), Image.ANTIALIAS)
            image.save(target, image.format, transparency=info['transparency'])

            # save to s3
            save_avatar_s3(target)

        else:
            image = image.convert("RGB")
            image = image.resize((size, size), Image.ANTIALIAS)
            image = image.convert('P', palette=Image.ADAPTIVE)
            image.save(target, image.format)

            # save to s3
            save_avatar_s3(target)

    if format == "PNG":
        image = image.resize((size, size), Image.ANTIALIAS)
        image.save(target, quality=95)

        # save to s3
        save_avatar_s3(target)

    if format == "JPEG":
        image = image.convert("RGB")
        image = image.resize((size, size), Image.ANTIALIAS)
        image = image.convert('P', palette=Image.ADAPTIVE)
        image = image.convert("RGB", dither=None)
        image.save(target, image.format, quality=95)

        # save to s3
        save_avatar_s3(target)


def save_avatar_s3(file):
    filename = os.path.basename(file)
    image_path_s3 = settings.MEDIA_ROOT_S3 + 'avatars/' + filename
    with open(file, 'r') as source:
        with storage.open(image_path_s3, 'wb+') as destination:
            destination.write(source.read())


def delete_avatar_s3(file):
    filename = os.path.basename(file)
    image_path_s3 = settings.MEDIA_ROOT_S3 + 'avatars/' + filename
    storage.delete(image_path_s3)
