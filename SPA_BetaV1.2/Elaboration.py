import datetime
import numpy as np
import cv2 as cv
import os
import _tifffile as tiff
from matplotlib import path

import utilities
import Panel
import settings

class Elaboration:

    def __init__(self, id, sourceImg):
        self.__id = int(id)
        self.__sourceImg = sourceImg #Image
        self.__status = int(0)
        self.__exeTime = 0 #Time
        self.__stepsDir = None #String
        self.__panelsDetected = list() #list of Panels
        self.__resizeValue = 10
        self.__resizedImg = False
        self.__croppingError = 10

        print('Elaboration id: ' + str(self.__id) + '\nSTATUS: ' + str(self.__status) + ' - INITIALIZATION')

    # get
    def getId(self):
        return self.__id

    def getSourceImg(self):
        return self.__sourceImg

    def getStatus(self):
        return self.__status

    def getExeTime(self):
        return self.__exeTime

    def getStepsDir(self):
        return str(self.__stepsDir)

    def getPanelsDetected(self):
        return self.__panelsDetected

    def getResized(self):
        return self.__resizedImg

    def getResizeValue(self):
        return self.__resizeValue

    def getCroppingError(self):
        return self.__croppingError

    def printInfo(self):
        print('Elaboration ID: ' + str(self.__id))
        print('Source image: ' + str(self.__sourceImg.getFullPath()))
        print('Status: ' + str(self.__status))
        print('Execution time: ' + str(self.__exeTime))
        print('Panels detected: ' + str(len(self.__panelsDetected)))

    # set
    def setId(self, inp):
        self.__id = inp
        return

    def setSourceImg(self, inp):
        self.__sourceImg = inp
        return

    def setStatus(self, inp):
        self.__status = inp
        return

    def setExeTime(self, inp):
        self.__exeTime = inp
        return

    def setStepsDir(self, inp):

        # dir of steps (folder with additional infos)
        self.__stepsDir = inp

        # create folder if it does not exist
        if not os.path.exists(inp):
            os.makedirs(inp)

        return

    def setPanelsDetected(self, inp):
        self.__panelsDetected = inp
        return

    def setResized(self):
        self.__resizedImg = True
        return

    # others
    def launchProcedure(self):

        inputImage = self.getSourceImg()
        SPA = settings.SPA

        params = SPA.getParams()
        debugMode = params[settings.DEBUG_PARAM]

        if debugMode is True:
            SPA.setDebugMode()

        panelDim = params[settings.DIM_PARAM]
        autoThresh = params[settings.AUTOTHRESH_PARAM]
        lowThresh = params[settings.LOWTHRESH_PARAM]
        highThresh = params[settings.HIGHTHRESH_PARAM]
        blur = params[settings.BLUR_PARAM]
        nIters = params[settings.DILATE_PARAM]
        minArea = params[settings.MINAREA_PARAM]

        # CMD ############################################################
        if settings.byCmd:
            # input parameters
            lowThresh = settings.arg[settings.LOW]
            highThresh = settings.arg[settings.HIGH]
            blur = settings.arg[settings.BLUR]
            nIters = settings.arg[settings.NITERS]
            minArea = settings.arg[settings.AREA]
            e = 10

            if settings.arg[settings.DEBUG_POS] == '1':
                SPA.setDebugMode()
        #####################################################################

        # dir of results
        saveDir = SPA.getSaveDir() + '/' + str(datetime.datetime.now().strftime("%d-%m-%Y_%H.%M") + '_' + inputImage.getFilename())
        print('SaveDir: ' + str(saveDir))

        # create folder if it does not exist
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)

        if SPA.checkDebugMode():
            self.setStepsDir(str(saveDir) + '/others')

        # t0
        tStart = datetime.datetime.now()

        print('\n>> Script begins... ' + utilities.time())
        print()
        print('>> Load image... ' + utilities.time())

        # read, check and eventually convert input image
        srcImg = self.checkImage()

        if srcImg is None:
            print('ERROR: Insert TIFF or JPG file')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\n')
            return

        print()
        print('   CONSTRAINTS:')
        print('   low threshold:  ' + str(lowThresh))
        print('   high threshold:  ' + str(highThresh))
        print('   blur:  ' + str(blur))
        print('   dilate iters:  ' + str(nIters))
        print('   min area:  ' + str(minArea))
        print('   cropping error in px:  ' + str((self.getCroppingError())))
        print()

        # IMG PROCESSING
        self.setStatus(1)
        print('>> STATUS ' + str(self.getStatus()) + ' - IMAGE PROCESSING BEGINS... ' + utilities.time())
        self.processImg(srcImg, int(lowThresh), int(highThresh), int(blur), int(nIters))
        print('<< ... IMAGE PROCESSING COMPLETE ' + utilities.time())
        print()

        # counter
        inputImage.incrementPanels()
        if self.getResized():
            srcImg = tiff.imread(inputImage.getFullPath())
            srcImg = cv.cvtColor(srcImg, cv.COLOR_RGB2BGR)

        # START ELABORATION ON IMG #########################################################################################
        self.setStatus(2)
        print('>> STATUS ' + str(self.getStatus()) + ' - PANELS DETECTION... ' + utilities.time())

        for contour in self.getSourceImg().getContours():

            # get bounding rect
            [x, y, w, h] = cv.boundingRect(contour)
            # areaE = cv.contourArea(contour)
            # perimeter = cv.arcLength(contour, True)

            # get panel rect
            rect = cv.minAreaRect(contour)
            [centerRect, [wRect, hRect], angle] = rect
            box = np.int0(cv.boxPoints(rect))
            area = wRect * hRect
            perim = wRect * 2 + hRect * 2

            # if found rect is reverse oriented
            if hRect < wRect:
                aux = hRect
                hRect = wRect
                wRect = aux
                angle = 90 + angle
                del aux

            # START LIMITATIONS #########################################

            # area lim with resize case
            if self.getResized():
                if area < int(int(minArea)/(self.getResizeValue()**2)):
                    continue
            else:
                if area < int(minArea):
                    continue

            # proportional lim
            if panelDim[0] is None and panelDim[1] is None:
                rate = settings.RATE_DEFAULT #rate = 1.8
                downRate = rate - 0.4
                upRate = rate + 0.4
            else:
                short = min(panelDim)
                long = max(panelDim)
                rate = int(long) / int(short)
                downRate = rate - 0.6
                upRate = rate + 0.6

            if hRect / wRect < downRate or hRect / wRect > upRate:
                continue

            # END LIMITATIONS ############################################

            # take coordinates of vertices
            xCoords = box[:, 0]
            yCoords = box[:, 1]

            # compute values of panel both resized or not
            vertices, centroid, x, y, w, h, hRect, wRect, area, rect = self.computePanelInfo(xCoords, yCoords, centerRect, area, wRect, hRect, angle, x, y, w, h)

            # create new Panel
            newPanel = Panel.Panel(id=inputImage.getPanels(), centroid=centroid, vertices=vertices, area=area, angle=angle,
                             minBox=[rect, [centerRect, [wRect, hRect], angle]], extRect=[x, y, w, h], rate=hRect / wRect)

            # check Rect in Rect and update rList
            updated = self.RectInRect(newPanel)

            if updated is True:
                print('   $ NEW Panel is found ' + utilities.time())
                print('      area = ' + str(area))
                print('      h = ' + str(hRect))
                print('      w = ' + str(wRect))
                print('      rate = ' + str(hRect / wRect))
                print('      angle = ' + str(angle))
                
                self.cropping(srcImg, newPanel, saveDir)
                print()

                # increase Panels counter
                inputImage.incrementPanels()

            # END FOR #####################################################################################################

        if self.getPanelsDetected():
            self.draw(srcImg)

        print('<< ...ELABORATION COMPLETED ' + utilities.time())
        print()

        self.setStatus(3)
        print('>> STATUS ' + str(self.getStatus()) + ' - COMPLETING... ' + utilities.time())

        # save result image with contours
        print('>> SAVE PROCESSED IMAGE... ' + utilities.time())
        cv.imwrite(saveDir + '/' + inputImage.getFilename() + '_processed.jpg', srcImg)
        print('<< ...SAVED!!! ' + utilities.time())

        # write CSV
        print('>> CSV WRITING ' + utilities.time())
        self.writeCSV(saveDir)
        print()

        # write DP xml
        print('>> CSV WRITING ' + utilities.time())
        self.writeDP(saveDir)
        print()

        # write metadata file
        metadataFile = open(saveDir + '/metadata.txt', "w+")
        metadataFile.write(str(self.getSourceImg().getMetadata()))

        # T
        tEnd = datetime.datetime.now()
        tDiff = tEnd - tStart
        self.setExeTime(tDiff)
        self.setStatus(4)
        print('>> STATUS ' + str(self.getStatus()) + ' - COMPLETED... ' + utilities.time())
        inputImage.setPanels(int(inputImage.getPanels()) - 1)

        self.printInfo()

        return self.getStatus()


    def convertToJPG(self, img):
        # convert to jpg
        print('>> Converting to .jpg ' + utilities.time())

        if self.getSourceImg().getFileweight() > 50000000:
            img = self.resizeImg(img)

        if settings.SPA.checkDebugMode():
            cv.imwrite(self.getStepsDir() + '/convertedImg.jpg', img)

        print('<< ... Conversion COMPLETED ' + utilities.time())

        return img


    def resizeImg(self, image):
        # resize
        print('>> Resizing image... ' + utilities.time())
        height, width = image.shape[:2]
        print('   height: ' + str(height) + ', width: ' + str(width))
        resizedImg = cv.resize(image, (int(width / self.getResizeValue()), int(height / self.getResizeValue())),
                               interpolation=cv.INTER_CUBIC)
        self.setResized()  # resized is True
        print('<< ... Image resized! ' + utilities.time())

        if settings.SPA.checkDebugMode() and not(self.getSourceImg().getFiletype() == '.tif' or self.getSourceImg().getFiletype() == '.tiff' or self.getSourceImg().getFiletype() == '.TIF' or self.getSourceImg().getFiletype() == '.TIFF'):
            cv.imwrite(self.getStepsDir() + '/resizedImg.jpg', resizedImg)

        return resizedImg


    def checkImage(self):
        # typefile cases
        if self.getSourceImg().getFiletype() == '.tif' or self.getSourceImg().getFiletype() == '.tiff' or self.getSourceImg().getFiletype() == '.TIF' or self.getSourceImg().getFiletype() == '.TIFF':
            # procedura tiff
            # load image
            tiffImg = tiff.imread(self.getSourceImg().getFullPath())
            tiffImg = cv.cvtColor(tiffImg, cv.COLOR_RGB2BGR)
            print('>> TIFF image reading')
            srcImg = self.convertToJPG(tiffImg)
            del tiffImg

        elif self.getSourceImg().getFiletype() == '.jpg' or self.getSourceImg().getFiletype() == '.jpeg' or self.getSourceImg().getFiletype() == '.JPG' or self.getSourceImg().getFiletype() == '.JPEG':
            # procedura
            srcImg = cv.imread(self.getSourceImg().getFullPath())

            if self.getSourceImg().getFileweight() > 50000000:
                srcImg = self.resizeImg(srcImg)

        else:
            # formato non adottato dal SW
            print('ERROR: Insert TIFF or JPG file')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\n')
            srcImg = None

        return srcImg


    def processImg(self, srcImg, lowThresh, highThresh, blur, nIters):
        # STEP 1 - grayscale
        grayImg = cv.cvtColor(srcImg, cv.COLOR_RGB2GRAY)
        if settings.SPA.checkDebugMode():
            cv.imwrite(self.getStepsDir() + '/01_grayImg.jpg', grayImg)
        print('   STEP 1 - RGB to GRAYSCALE')

        # STEP 2 - blur
        blurImg = cv.bilateralFilter(grayImg, int(blur), 150, 150)
        del grayImg
        if settings.SPA.checkDebugMode():
            cv.imwrite(self.getStepsDir() + '/02_blurredImg.jpg', blurImg)
        print('   STEP 2 - Blurring')

        # STEP 3 - canny edge detection
        #autothresh
        if settings.SPA.getParams()[settings.AUTOTHRESH_PARAM] or (settings.byCmd is True and lowThresh == 0 and highThresh == 0):
            # OTSU method
            lowThresh,th = cv.threshold(blurImg,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
            settings.autoThreshValue = lowThresh
            highThresh = settings.HIGHTHRESH_DEFAULT

        edges = cv.Canny(blurImg, int(lowThresh), int(highThresh))
        del blurImg
        if settings.SPA.checkDebugMode():
            cv.imwrite(self.getStepsDir() + '/03_edges.jpg', edges)
        print('   STEP 3 - Edges detection')

        # STEP 4 - dilate image
        dilatedImg = cv.dilate(edges, np.ones((5, 5), np.uint8), iterations=int(nIters))
        del edges
        if settings.SPA.checkDebugMode():
            cv.imwrite(self.getStepsDir() + '/04_dilatedImg.jpg', dilatedImg)
        print('   STEP 4 - Edges dilatation')

        # STEP 5 - find contours
        contoursImg, contours, hierarchy = cv.findContours(dilatedImg, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        del dilatedImg
        del contoursImg
        print('   STEP 5 - Contours detection')

        self.getSourceImg().setContours(contours)

        return


    def computePanelInfo(self, xCoords, yCoords, centerRect, area, wRect, hRect, angle, x, y, w, h):
        if not self.getResized():
            # no resized img values update
            vEl0 = (int(xCoords[0]), int(yCoords[0]))
            vEl1 = (int(xCoords[1]), int(yCoords[1]))
            vEl2 = (int(xCoords[2]), int(yCoords[2]))
            vEl3 = (int(xCoords[3]), int(yCoords[3]))
            centerX = int(centerRect[0])
            centerY = int(centerRect[1])

        else:
            # resized img values update
            vEl0 = (int(xCoords[0] * self.getResizeValue()), int(yCoords[0] * self.getResizeValue()))
            vEl1 = (int(xCoords[1] * self.getResizeValue()), int(yCoords[1] * self.getResizeValue()))
            vEl2 = (int(xCoords[2] * self.getResizeValue()), int(yCoords[2] * self.getResizeValue()))
            vEl3 = (int(xCoords[3] * self.getResizeValue()), int(yCoords[3] * self.getResizeValue()))
            centerX = int(centerRect[0] * self.getResizeValue())
            centerY = int(centerRect[1] * self.getResizeValue())
            centerRect = (centerX, centerY)
            wRect = wRect * self.getResizeValue()
            hRect = hRect * self.getResizeValue()
            x = x * self.getResizeValue()
            y = y * self.getResizeValue()
            w = w * self.getResizeValue()
            h = h * self.getResizeValue()
            area = area * (self.getResizeValue()**2)

        centroid = tuple([centerX, centerY])
        rect = (centerRect, (wRect, hRect), angle)

        # collecting vertices and sorting
        vertices = [vEl0, vEl1, vEl2, vEl3]
        vertices = self.sortVertices(vertices)

        return vertices, centroid, x, y, w, h, hRect, wRect, area, rect


    def sortVertices(self, a):
        sorted_y = sorted(a, key=lambda tup: tup[1])
        a1 = [sorted_y[0], sorted_y[1]]
        a2 = [sorted_y[2], sorted_y[3]]

        sorted_x1 = sorted(a1, key=lambda tup: tup[0])
        sorted_x2 = sorted(a2, key=lambda tup: tup[0], reverse=True)

        return sorted_x1 + sorted_x2


    def RectInRect(self, newPanel):
        # indexes
        redundantItem = False
        index = -1  # of rList
        updated = False

        if not self.getPanelsDetected():
            self.getPanelsDetected().append(newPanel)
            updated = True
        else:
            for item in self.getPanelsDetected():

                index += 1
                polygon = path.Path(newPanel.getVertices())

                if polygon.contains_points(points=[item.getCentroid()]):
                    redundantItem = True

                    if item.getArea() > newPanel.getArea():
                        self.getPanelsDetected()[index] = newPanel  # update rList
                    else:
                        # discard newRect
                        pass

            if not redundantItem:
                self.getPanelsDetected().append(newPanel)
                updated = True

        return updated


    def cropping(self, srcImg, Panel, saveDir):
        e = self.getCroppingError()

        # rotation of image
        M = cv.getRotationMatrix2D(Panel.getCentroid(), Panel.getAngle(), 1)
        rotatedImg = cv.warpAffine(srcImg, M, srcImg.shape[1::-1], flags=cv.INTER_LINEAR)

        # shift image and increase cropping area (error of cropping)
        h = Panel.getExtRect()[3]
        w = Panel.getExtRect()[2]
        y = Panel.getExtRect()[1]
        x = Panel.getExtRect()[0]

        [centerRect, [wRect, hRect], angle] = Panel.getMinBox()[1]
        # hRect = Panel.getMinBox()[1][1]
        # wRect = Panel.getMinBox()[1][0]
        shiftY = (int((h - hRect) / 2))
        shiftX = (int((w - wRect) / 2))

        # cropping and save
        print('      Panel CROPPING and SAVE ' + utilities.time())

        croppedImg = rotatedImg[y + shiftY - e: y + int(hRect) + shiftY + e * 2,
                     x + shiftX - e: x + int(wRect) + shiftX + e * 2]


        cv.imwrite(saveDir + '/' + str(Panel.getId()) + '.jpg', croppedImg)

        Panel.setCropImgPath(saveDir + '/' + str(Panel.getId()) + '.jpg')

        del rotatedImg
        del croppedImg

        return 0


    # write CSV
    def writeCSV(self, dir):
        import csv
        with open(dir + '/report.csv', 'w+') as report:
            filewriter = csv.writer(report, delimiter=';', quoting=csv.QUOTE_ALL)
            filewriter.writerow(['ID', 'VERTEX-1', 'VERTEX-2', 'VERTEX-3', 'VERTEX-4', 'CENTROID', 'AREA'])
            for item in self.getPanelsDetected():
                filewriter.writerow([item.getId(), item.getVertices()[0], item.getVertices()[1], item.getVertices()[2],
                                     item.getVertices()[3], item.getCentroid(), item.getArea()])


    # write DP
    def writeDP(self, dir):
        # elaboration info
        id = self.getId()
        sourceImg = self.getSourceImg()
        panels = self.getPanelsDetected()
        params = settings.SPA.getParams()

        import xml.etree.cElementTree as ET
        root = ET.Element("root")
        elaboration = ET.SubElement(root, "elaboration", id=str(id))

        # params
        parameters = ET.SubElement(elaboration, "params")
        if params[settings.AUTOTHRESH_PARAM] is not True:
            ET.SubElement(parameters, "threshold", low=str(params[settings.LOWTHRESH_PARAM]), high=str(params[settings.HIGHTHRESH_PARAM])).text = "manual"
        else:
            ET.SubElement(parameters, "threshold", value=str(settings.autoThreshValue)).text = "automatic"
        ET.SubElement(parameters, "blur").text = str(params[settings.BLUR_PARAM])
        ET.SubElement(parameters, "dilate").text = str(params[settings.DILATE_PARAM])
        ET.SubElement(parameters, "area").text = str(params[settings.MINAREA_PARAM])

        dim = params[settings.DIM_PARAM]
        if dim[0] is not None and dim[1] is not None:
            ratio = int(int(dim[0])/int(dim[1]))
            ET.SubElement(parameters, "ratio").text = str(ratio)

        # image
        image = ET.SubElement(elaboration, "source_image", id=str(sourceImg.getId()), path=str(sourceImg.getFullPath()))
        ET.SubElement(image, "extension").text = str(sourceImg.getFiletype())
        ET.SubElement(image, "weight", measure="bytes").text = str(sourceImg.getFileweight())
        if sourceImg.getFiletype() != ".tif" and sourceImg.getFiletype() != ".tiff" and sourceImg.getFiletype() != ".TIF" and sourceImg.getFiletype() != ".TIFF":
            ET.SubElement(image, "gps").text = str(sourceImg.getGPSCoord())

        # panels
        for item in panels:
            panel =  ET.SubElement(elaboration, "panel", id=str(item.getId()), path=str(item.getCropImgPath()))
            for v in item.getVertices():
                ET.SubElement(panel, "vertex").text = str(v)
            ET.SubElement(panel, "centroid").text = str(item.getCentroid())
            ET.SubElement(panel, "area").text = str(item.getArea())
            ET.SubElement(panel, "angle").text = str(item.getAngle())
            ET.SubElement(panel, "ratio").text = str(item.getRate())

        # write
        tree = ET.ElementTree(root)
        tree.write(dir + "/particular_data.xml")


    # drawing
    def draw(self, srcImg):

        print('>> Drawing on source image... ' + utilities.time())
        print()

        [centerRect, [w, h], angle] = self.getPanelsDetected()[0].getMinBox()[1]

        dim = int(max(w, h) * 0.02)

        if self.getSourceImg().getFiletype() == '.tif' or self.getSourceImg().getFiletype() == '.tiff' or self.getSourceImg().getFiletype() == '.TIF' or self.getSourceImg().getFiletype() == '.TIFF':
            dim = int(dim/2) #resize

        for panel in self.getPanelsDetected():

            box = np.int0(cv.boxPoints(panel.getMinBox()[0]))
            cv.drawContours(srcImg, [box], 0, (0, 255, 255), dim)

            # # draw bounding rect
            # cv.rectangle(srcImg, (x, y), (x + w, y + h), (0, 255, 255), 20)

            # draw centroid
            cv.circle(srcImg, panel.getCentroid(), dim * 2, (0, 255, 0), -1)

            # draw vertices
            cv.circle(srcImg, panel.getVertices()[0], dim * 2, (0, 255, 0), -1)
            cv.circle(srcImg, panel.getVertices()[1], dim * 2, (0, 255, 0), -1)
            cv.circle(srcImg, panel.getVertices()[2], dim * 2, (0, 255, 0), -1)
            cv.circle(srcImg, panel.getVertices()[3], dim * 2, (0, 255, 0), -1)

            # show sorted vertices
            for i in range(len(panel.getVertices())):
                cv.putText(srcImg, str(i + 1), panel.getVertices()[i], cv.FONT_HERSHEY_SIMPLEX, int(dim/3), (255, 255, 255), int(dim/3))

            # write name of panel
            cv.putText(srcImg, str(panel.getId()), panel.getCentroid(), cv.FONT_HERSHEY_SIMPLEX, int(dim / 2),
                       (255, 255, 255), int(dim / 2))

        return 0
