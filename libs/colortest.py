# test


import time, os
from painting import Painting
from drawLine import *
import cv2
import matplotlib.pyplot as plt
def imageSave(image, directory = "./result-image/", name = "", id=""):
    path = os.path.join(directory, name+"-"+id)
    print(path)
    cv2.imwrite(path+".jpg", image)
    return
    
# import time
# start = time.time()
# print("비교 시간 :", round((time.time() - start), 3) ,"초.." )

dir = "./test-image/"
file = "senss"
base = ".png"
id = "a"

start = time.time()

painting = Painting( dir+file+base )
'''
# org
blurImage = painting.blurring(div = 32, radius = 10, sigmaColor = 30, medianValue=5)
imageSave(blurImage, name = file+"-blur", id=id)

similarMap = painting.getSimilarColorMap(blurImage, value = 10, direction = "h" )
imageSave(similarMap, name = file+"-similar", id=id)
'''
# plt.imshow(painting.image)
# plt.show()
# test
similarMap = painting.getSimilarColorMap( value = 5, direction = "h" )
imageSave(similarMap, name = file+"-similar", id=id)
# plt.imshow(similarMap)
# plt.show()
print("========  Similar Map End  =======")
print("time :", round((time.time() - start), 3) ,"초 정도.." )
start = time.time()
blurImage = painting.blurring(similarMap, div = 20, radius = 15, sigmaColor = 40, medianValue= 5)
imageSave(blurImage, name = file+"-blur", id=id)
print("========  Blur Map End  =======")
print("time :", round((time.time() - start), 3) ,"초 정도.." )
# test finish
start = time.time()

print("========  Merge Color Map End  =======")
paintingMap = painting.getPaintingColorMap(blurImage)
# paintingMap = painting.getPaintingColorMap(blurImage)
print("time :", round((time.time() - start), 3) ,"초 정도.." )

imageSave(paintingMap, name = file+"-painting", id=id)
# plt.imshow(paintingMap)
# plt.show()

# colorDict = painting.getColorDict(paintingMap)
print("=="*20)
# print("COLOR NUMBER : ", len(colorDict))
print("=="*20)

drawLine = DrawLine(paintingMap)

start = time.time()
print("========  draw Line End  =======")
lineMap = drawLine.getDrawLine()
imageSave(lineMap, name = file+"-line", id=id)
# plt.imshow(lineMap)
# plt.show()
print("time :", round((time.time() - start), 3) ,"초 정도.." )

print("========= Expand Process ========")
start = time.time()
expandImage = imageExpand(lineMap, guessSize = True)
imageSave(expandImage, name = file+"-expand", id=id)
print("time :", round((time.time() - start), 3) ,"초 정도.." )
# expandImage = eraseOutline(expandImage)
# imageSave(expandImage, name = file+"-erase", id=id)

skImage = leaveOnePixel(expandImage)
imageSave(skImage, name = file+"-skeleton", id=id)

lineImage = drawLine.getLineOnImage()
imageSave(lineImage, name = file+"-line+image", id=id)






