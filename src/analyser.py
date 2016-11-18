from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

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


pdf_name = input("Insert PDF file to extract metadata: ")
print("\n")
print_metadata_pdf(pdf_name)

erase_metadata = input("Do you want to erase metadata from the file?(S/N)")
if erase_metadata is 'S':
    write_metadata_pdf(pdf_name, None)

print("\nAllright, be careful with your data!\n")
