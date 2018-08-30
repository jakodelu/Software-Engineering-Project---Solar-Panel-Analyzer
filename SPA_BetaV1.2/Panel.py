class Panel:

    def __init__(self, id, vertices, centroid, area, angle, minBox, extRect, rate):
        self.__id = int(id)
        self.__vertices = list(vertices)
        self.__centroid = tuple(centroid)
        self.__area = int(area)
        self.__angle = int(angle)
        self.__minBox = minBox #Rect
        self.__extRect = extRect #Rect
        self.__rate = rate
        self.__cropImgPath = None #String
        return

    # get
    def getId(self):
        return self.__id

    def getVertices(self):
        return self.__vertices

    def getCentroid(self):
        return self.__centroid

    def getArea(self):
        return self.__area

    def getAngle(self):
        return self.__angle

    def getMinBox(self):
        return self.__minBox

    def getExtRect(self):
        return self.__extRect

    def getCropImgPath(self):
        return self.__cropImgPath

    def getRate(self):
        return self.__rate

    # set
    def setId(self, inp):
        self.__id = inp
        return

    def setVertices(self, inp):
        self.__vertices = inp
        return

    def setCentroid(self, inp):
        self.__centroid = inp
        return

    def setArea(self, inp):
        self.__area = int(inp)
        return

    def setAngle(self, inp):
        self.__angle = inp
        return

    def setMinBox(self, inp):
        self.__minBox = inp
        return

    def setExtRect(self, inp):
        self.__extRect = inp
        return

    def setCropImgPath(self, inp):
        self.__cropImgPath = inp
        return

    def setRate(self, inp):
        self.__rate = inp
        return


