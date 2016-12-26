# -*- coding: utf-8 -*-
from PIL import Image, ImageEnhance
import qrcode
import PIL
import math
import base64
import cStringIO


class vn_qrcode():
    def generate_qrcode(self, text):
        # initialize settings for Output Qrcode
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=1, )
        # adds the data to the qr cursor
        qr.add_data(text)
        qr.make(fit=True)
        result = qr.make_image()
        return result

    def reduce_opacity(self, im, opacity):
        """Returns an image with reduced opacity."""
        assert opacity >= 0 and opacity <= 1
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        else:
            im = im.copy()
        alpha = im.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        im.putalpha(alpha)
        return im

    def watermark_image_with_qrcode(self, image, text, opacity=1):
        # open image background
        image = Image.open(image)
        width, height = image.size
        # generate qrcode from text
        background_size = int(math.sqrt((width * width) + (height * height)) * 0.2)
        image_qrcode = self.generate_qrcode(text).resize((background_size, background_size), PIL.Image.ANTIALIAS)
        qrc_width, qrc_height = image_qrcode.size
        position = ((width - qrc_width), (height - qrc_height))

        """Adds a watermark to an image."""
        if opacity < 1:
            image_qrcode = self.reduce_opacity(image_qrcode, opacity)
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        # create a transparent layer the size of the image and draw the
        # watermark in that layer.
        layer = Image.new('RGBA', image.size, (0, 0, 0, 0))

        layer.paste(image_qrcode, position)
        # composite the watermark with the layer
        watermark_image = Image.composite(layer, image, layer)

        #convert to base64
        buffer = cStringIO.StringIO()
        watermark_image.save(buffer, format="png")
        result = base64.b64encode(buffer.getvalue())

        return result
