from service.ImportService import ImportService

import sys
import requests
import time
import random

reload(sys)
sys.setdefaultencoding('utf-8')

img = 'http://www.imageto.org/images/q96g.jpg'

image = ImportService.upload_image(img, iscut=True, w=480, h=320)
print '========================'
print image