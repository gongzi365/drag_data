from service.ImportService import ImportService

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

img = 'https://extraimage.net/images/2018/11/14/91ec07adb6ac17d8d485f5ed2641293a.jpg'
image = ImportService.upload_image(img, iscut=True)
