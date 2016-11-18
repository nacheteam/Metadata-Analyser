from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from PIL.ExifTags import TAGS, GPSTAGS
from PIL import Image
import gmplot
import os

'''
This function printfs the metadata from a pdf file given the name of the file. It requires the file to be in the data folder
made in the project folder. It prints normal metadata, numer of pages and XMP Adobe metadata  if found.
pdf_file is a string type object containing the pdf file name.
'''
def print_metadata_pdf(pdf_file):
    pdfFile = PdfFileReader(open("./data/"+pdf_file, 'rb'))
    docInfo = pdfFile.getDocumentInfo()

    for metaItem in docInfo:
        print("[X] " + metaItem + ": " + str(docInfo[metaItem]))
    print("[X] El número de páginas es: " + str(pdfFile.getNumPages()))

    xmpMetadata = pdfFile.getXmpMetadata()
    print("\nXMP metadata:\n")
    if not xmpMetadata is None:
        for key in xmpMetadata.custom_properties:
            print("[X] " + key + ": " + str(xmpMetadata.custom_properties[key]))
        key_words = xmpMetadata.pdf_keywords
        if not key_words is None:
            print("Keywords found: " + str(key_words))
    else:
        print("No XMP metadata was found.")

'''
This function writes new metadata to a pdf, the actual setting is just to erase the metadata from a file, so that the given metadata dictionary is empty by default.
The result is going to be in the result folder of the project with the same name as the input.
pdf_file is a string type object containing the pdf file name.
The metadata object is a dictionary containing the new metadata of the file.
'''
def write_metadata_pdf(pdf_file, metadata):
    if metadata is None:
        metadata = {}

    pdfFile = PdfFileReader(open("./data/"+pdf_file, 'rb'))
    pdfFile_writer = PdfFileWriter()

    for i in range(pdfFile.getNumPages()):
        pdfFile_writer.addPage(pdfFile.getPage(i))

    pdfFile_writer.addMetadata(metadata)
    outputStream = open("./result/"+pdf_file, 'wb')
    pdfFile_writer.write(outputStream)
    outputStream.close()
    print("\nNew metadata added!\n")

def getImageMetadata(image_file):
    try:
        webpage = ""
        exifData = {}
        imgFile = Image.open("./data/"+image_file)
        info = imgFile._getexif()
        if info:
            for (tag, value) in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t,t)
                        gps_data[sub_decoded] = value[t]

                    exifData[decoded] = gps_data
                else:
                    exifData[decoded] = value
            for key in exifData:
                print("[X] " + str(key) + ": " + str(exifData[key]))
            (lat, lon) = get_lat_lon(exifData)
            print("\n\n[X] Latitude and longitude of image: " + str(lat) + ", " + str(lon))
            if lat and lon:
                print("\n\nCreating map\n")
                gmap = gmplot.GoogleMapPlotter(lat, lon, 16)
                gmap.marker(lat, lon)
                gmap.draw("./result/" + image_file + ".html")
                webpage = "./result/" + image_file + ".html"
        else:
            print("No metadata found!")
    except:
        pass
    return webpage

def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
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

def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None

def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon

def main(fileType):
    if fileType=="PDF":
        pdf_name = input("Insert PDF file to extract metadata: ")
        print("\n")
        print_metadata_pdf(pdf_name)

        erase_metadata = input("Do you want to erase metadata from the file?(S/N)")
        if erase_metadata is 'S':
            write_metadata_pdf(pdf_name, None)

        image = input("Insert image: ")
        getImageMetadata(image)

    elif fileType=="Image":
        image_name = input("Insert Image file to extract metadata: ")
        webpage = getImageMetadata(image_name)
        open_map = input("Would you like to see the map?(S/N): ")
        if open_map=='S':
            os.system("firefox " + webpage)

    print("\nAllright, be careful with your data!\n")

fileType = input("Insert the type of file(Image/PDF):")
main(fileType)
