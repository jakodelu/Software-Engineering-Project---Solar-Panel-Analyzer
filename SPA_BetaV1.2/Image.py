import os

class Image:

    def __init__(self, id, filepath):
        self.__id = int(id)
        self.__fullPath = str(filepath)
        dir, filename, filetype = self.extractFile(filepath)
        self.__filedir = str(dir)
        self.__filename = str(filename)
        self.__filetype = str(filetype)
        self.__fileweight = os.path.getsize(filepath) #byte
        self.__gpscoord = None
        self.__metadata = None
        self.__contours = list() #contours
        self.__panelsCounter = int(0)
        self.__elaborationId = None

        # metadata reading is not supported for TIF files
        if self.__filetype != ".tif" and self.__filetype != ".tiff" and self.__filetype != ".TIF" and self.__filetype != ".TIFF":
            self.readMetadata()

        print('About IMAGE:')
        print('id: ' + str(self.__id))
        print('dir: ' + str(self.__filedir))
        print('name: ' + str(self.__filename))
        print('type: ' + str(self.__filetype))
        print('weight: ' + str(self.__fileweight) + ' bytes')
        print('gps coord: ' + str(self.__gpscoord))
        print()

    # get
    def getId(self):
        return self.__id

    def getFullPath(self):
        return self.__fullPath

    def getFiledir(self):
        return self.__filedir

    def getFilename(self):
        return self.__filename

    def getFiletype(self):
        return self.__filetype

    def getFileweight(self):
        return self.__fileweight

    def getMetadata(self):
        return self.__metadata

    def getGPSCoord(self):
        return self.__gpscoord

    def getContours(self):
        return self.__contours

    def getPanels(self):
        return self.__panelsCounter

    # set
    def setId(self, inp):
        self.__id = inp
        return

    def setFiledir(self, inp):
        self.__filedir= inp
        return

    def setFilename(self, inp):
        self.__filename = inp
        return

    def setFiletype(self, inp):
        self.__filetype = inp
        return

    def setMetadata(self, inp):
        self.__metadata = inp
        return

    def setGPSCoord(self, inp):
        self.__gpscoord = inp
        return

    def setContours(self, inp):
        self.__contours = inp
        return

    def setPanels(self, inp):
        self.__panelsCounter = inp
        return

    # others
    def extractFile(self, inputFilepath):
        filename_w_ext = os.path.basename(inputFilepath)
        filename, file_extension = os.path.splitext(filename_w_ext)
        path, filename = os.path.split(inputFilepath)
        filename = filename.replace(file_extension, '')

        return path, filename, file_extension

    def incrementPanels(self):
        self.__panelsCounter = self.__panelsCounter + 1
        return

    # metadata methods
    def readMetadata(self):
        from PIL import Image

        exif_data = None
        image = None

        path_name = self.getFullPath()
        image = Image.open(path_name)
        latlng = self.get_lat_lng(image)
        exif_data = self.get_exif_data(image)
        self.setMetadata(str(exif_data))
        self.setGPSCoord(str(latlng))

    def get_exif_data(self, image):
        from PIL.ExifTags import TAGS, GPSTAGS
        """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
        exif_data = {}
        info = image._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]

                    exif_data[decoded] = gps_data
                else:
                    exif_data[decoded] = value
        self.exif_data = exif_data
        return exif_data

    def get_if_exist(self, data, key):
        if key in data:
            return data[key]
        return None

    def convert_to_degress(self, value):

        """Helper function to convert the GPS coordinates
        stored in the EXIF to degress in float format"""
        d0 = value[0][0]
        d1 = value[0][1]
        d = float(d0) / float(d1)

        m0 = value[1][0]
        m1 = value[1][1]
        m = float(m0) / float(m1)

        s0 = value[2][0]
        s1 = value[2][1]
        s = float(s0) / float(s1)

        return d + (m / 60.0) + (s / 3600.0)

    def get_lat_lng(self, image):
        """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
        lat = None
        lng = None
        exif_data = self.get_exif_data(image)
        # print(exif_data)
        if "GPSInfo" in exif_data:
            gps_info = exif_data["GPSInfo"]
            gps_latitude = self.get_if_exist(gps_info, "GPSLatitude")
            gps_latitude_ref = self.get_if_exist(gps_info, 'GPSLatitudeRef')
            gps_longitude = self.get_if_exist(gps_info, 'GPSLongitude')
            gps_longitude_ref = self.get_if_exist(gps_info, 'GPSLongitudeRef')
            if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                lat = self.convert_to_degress(gps_latitude)
                if gps_latitude_ref != "N":
                    lat = 0 - lat
                lng = self.convert_to_degress(gps_longitude)
                if gps_longitude_ref != "E":
                    lng = 0 - lng
        return lat, lng