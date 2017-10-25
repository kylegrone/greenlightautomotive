import base64
import cStringIO
from email.mime import image
import os
import uuid

from PIL import Image
from django.core.files.base import ContentFile
from django.http import request
import pytesseract

from BMW import settings


class CameraService():
    
    
    def get_zbar_from(self,image):
        try:
            import zbarlight
            codes = zbarlight.scan_codes('barcode', image)
            print codes
            if codes:
                return codes[0]
            else:
                print "code not found"
                return None
        except Exception,e:
            print "error"
            print e
            return None
        
    def get_image_from_base64(self,image):
        try:
            bassplit = image.split(',')
            b64data = bassplit[0] if len(bassplit)==1 else bassplit[1]
            # _, b64data = image.split(',')
            # pic = cStringIO.StringIO()
            image_string = cStringIO.StringIO(self.decode_base64(b64data))
            image = Image.open(image_string)
            uid = str(uuid.uuid4())
            image.save(settings.MEDIA_ROOT+'/newtest'+uid[0:4]+'.png', 'png')
            return image
        except Exception,e:
            print "getting here"
            print e
            return None
        
        
    def get_ocr_base64(self,image):
        try:
            _, b64data = image.split(',')
            pic = cStringIO.StringIO()
            image_string = cStringIO.StringIO(self.decode_base64(b64data))
            image = Image.open(image_string)
#             image.save(settings.MEDIA_ROOT+"/test.jpeg", image.format, quality = 100)
            pic.seek(0)
            abc = pytesseract.image_to_string(image)
            return abc
        except Exception,e:
            print str(e)
            return False
    
    def get_qr_base64(self,image):
        try:
            _, b64data = image.split(',')
            pic = cStringIO.StringIO()
            image_string = cStringIO.StringIO(self.decode_base64(b64data))
            image = Image.open(image_string)
#             image.save(settings.MEDIA_ROOT+"/test.jpeg", image.format, quality = 100)
            pic.seek(0)
#             qr = qrtools.QR()
#             text = qr.decode(image)
#             abc = pytesseract.image_to_string(image)
            return None
        except Exception,e:
            print str(e)
            return False    
        
         
    def decode_base64(self,data):
        """Decode base64, padding being optional.
    
        :param data: Base64 data as an ASCII byte string
        :returns: The decoded byte string.
    
        """
        missing_padding = 4 - len(data) % 4
        if missing_padding:
            data += b'='* missing_padding
        return base64.decodestring(data)