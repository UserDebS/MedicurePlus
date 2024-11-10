import os
from .base64Man import base64imageSplit, getImageType
import base64 as bsf

def createImage(b64str : str):
    parentDir : str = os.path.dirname(os.path.dirname(__file__))
    targetDir = os.path.join(parentDir, 'modeluploader')
    if(os.path.exists(targetDir)):
        with open(os.path.join(targetDir, f'upload.{getImageType(b64str)}'), 'wb') as img:
            img.write(bsf.b64decode(base64imageSplit(b64str)))
    
if __name__ == '__main__':
    createImage('sfs')