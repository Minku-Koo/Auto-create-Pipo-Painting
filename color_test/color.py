﻿#210401
#minku koo

import matplotlib.pyplot as plt
import cv2
import numpy as np
import random, datetime, os

'''
# -- 메모 --
# opencv에서 imread는 기본 BGR
'''

class Color:
    def __init__ (self, filepath, job_id = "job123"):
        self.__job_id = job_id
        self.colorDict = {}
        self.colorMap = np.array([])
        
        self.width, self.height = 800, 500
        
        self.__imageSetting( filepath )
        
    def __imageSetting(self, imagepath):
        self.filename = os.path.basename(imagepath)
        self.image = cv2.imread(imagepath) #, cv2.IMREAD_GRAYSCALE
        # self.rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        
        a = [30, 56, 87]
        hexColor = self.__bgr2hex(a)
        print(hexColor)
        return
    
    def colorProcess(self, image):
        print("color process start")
        print(" ======= File Name ======")
        print("file:", self.filename)
        render_file_name = self.filename.split(".")[0]
        # dict = self.__createColorDict(image) # make  self.colorDict
        # print("--------- dict count:", len(dict.keys()))
        images = image.copy()
        self.colorMap = self.__createColorMap(image)
        print(" ======= Convert Image Size ======")
        print("size:",self.colorMap.shape )
        self.imageSave(self.colorMap, name=render_file_name+"change"  )
        dict =  self.__createColorDict(self.colorMap)
        print(" ======= COLOR Numbers ======")
        print("color:", len(dict.keys()))
        
        changeMap = self.checkChange(images, self.colorMap)
        self.imageSave(changeMap, name=render_file_name+"change_area"  )
        
        return 
        
        
    def checkChange(self, image, map):
        maps = []
        for r1, r2 in zip(image, map):
            line = []
            for i, j in zip(r1, r2):
                i, j = list(i), list(j)
                if i == j:
                    line.append([255, 255, 255])
                else:
                    line.append( i )
            maps.append(line)
        return np.array(maps)
    
    def blurring(self, radius = 15, sigmaColor = 90, sigmaSpace = 60) :
        '''
        이미지 크기에 맞추어 블러 사이즈 조절하기
        '''
        
        blurring = cv2.bilateralFilter(self.image,  radius, sigmaColor, sigmaSpace)
        # cv2.imshow("bilateralFilter", dst)
        return blurring
    
    def __bgr2hex(self, bgr):
        hexColor = ""
        for color in bgr: hexColor+= hex(color).split('x')[-1]
        return hexColor
    
    def __createColorDict(self, image, value = 15):
        for y, row in enumerate(image):
            for x, bgr in enumerate(row):
                bgr = tuple(bgr)
                if self.colorDict == {}: self.colorDict[ bgr ] = [ (x, y) ]
                """
                for key in self.colorDict.keys():
                    b, g, r = key
                    blue, green, red = tuple(bgr)
                    if  b-value< blue <b+value and \
                        g-value< green <g+value and \
                        r-value< red <r+value:
                        
                        self.colorDict[key].append( (x, y) )
                        break
                self.colorDict[tuple(bgr)] = [ (x, y) ]
                    
                """
                # hexColor = self.__bgr2hex(bgr)
                if bgr in self.colorDict.keys():
                    self.colorDict[bgr].append( (x, y) )
                else:
                    self.colorDict[bgr] = [ (x, y) ]
                
        # print(self.colorDict)
        return self.colorDict
    
    def __createColorMap(self, blurImage, value = 15):
        map = []
        count = 0
        image_size_ = blurImage.shape[0]
        for y, row in enumerate(blurImage):
            line = []
            if y % 500 == 0: print("processing...", y, "/", image_size_)
            for x, bgr in enumerate(row):
                colorChange = False
                blue, green, red = bgr
                for c in [-1, 1]:
                    try: 
                        b, g, r = blurImage[y+c, x]
                        if b==blue and g==green and r==red: pass
                        elif  b-value< blue <b+value and \
                        g-value< green <g+value and \
                        r-value< red <r+value: # and \
                        #(r!=red or b!=blue or g!=green):
                            line.append( [b, g, r] )
                            blurImage[y][x] = [ b, g, r ]
                            colorChange = True
                            break
                    except IndexError as e: pass
                    
                    try: 
                        b, g, r = blurImage[y, x+c]
                        if b==blue and g==green and r==red: pass
                        elif  b-value< blue <b+value and \
                        g-value< green <g+value and \
                        r-value< red <r+value: # and \
                        #(r!=red or b!=blue or g!=green):
                            line.append( [b, g, r] )
                            blurImage[y][x] = [ b, g, r ]
                            colorChange = True
                            break
                    except IndexError as e: pass
                if not colorChange: line.append( [blue, green, red] )
                else: count += 1
            map.append( line )
        print("change count:", count)
        return np.array(map)
        
    
    def imageSave(self, image, directory = "./render/", name = ""):
        if name == "": path = os.path.join(directory, self.filename)
        else: path = os.path.join(directory, name+".jpg")
        
        cv2.imwrite(path, image)
        return
    
    def onChange(self, pos): pass
    
    def showBar(self):
        
        cv2.namedWindow("Trackbar Windows")

        cv2.createTrackbar("t", "Trackbar Windows", 0, 200, self.onChange)
        cv2.createTrackbar("j", "Trackbar Windows", 0, 200, self.onChange)

        cv2.setTrackbarPos("t", "Trackbar Windows", 40)
        cv2.setTrackbarPos("j", "Trackbar Windows", 60)

        while cv2.waitKey(1) != ord('q'):

            t = cv2.getTrackbarPos("t", "Trackbar Windows")
            j = cv2.getTrackbarPos("j", "Trackbar Windows")

            dst = self.blurring(t, j)
            print(t, j)
            # dst_ = cv2.resize(dst, dsize=(self.width, self.height))
            cv2.imshow("Trackbar Windows", dst)

        cv2.destroyAllWindows()
            
if __name__ == "__main__":
    import time
    start = time.time()
    dirpath = "./test/"
    filename = "tli"
    
    color_class = Color( dirpath + filename + ".jpg" )
    # color_class.showBar()
    value = 110
    blurImage = color_class.blurring(radius = 18, sigmaColor = 90, sigmaSpace = 110)
    color_class.imageSave(blurImage, name=filename+"org")
    color_class.colorProcess(blurImage)
    
    
    print("time :", time.time() - start)
    
    # color_class.imageSave(blurImage) #, name = filename+str(value)
    
    