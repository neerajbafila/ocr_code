import os
import re
import sys
import cv2
import time
import logging
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfFileMerger, PdfFileReader
from pdf2image.exceptions import (PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError)

input_file = sys.argv[1]
dir_word = sys.argv[2]


root_path = os.path.dirname(os.path.realpath(__file__))
# print(root_path)

logging.basicConfig(filename=root_path + r'\ Local_Pdf_To_OCR.log', level=logging.INFO,
                    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s", filemode="a")


pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
TESSDATA_PREFIX = r'C:\\Program Files\\Tesseract-OCR'
tessdata_dir_config = 'tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'


input_pdf_path = root_path
pdf_to_image_output = root_path + '\\mainadminhtml\\' + dir_word + '\\pdf_to_image_output'
image_to_pdf_ocr_output = root_path + '\\mainadminhtml\\' + dir_word + '\\image_to_pdf_ocr_output'
combine_pdf_file = root_path + '\\mainadminhtml\\' + dir_word + '\\files'

start_time = time.time()

class OCR:
    try:
        logging.info(f"The OCR Exicution Is Started.....")

        def __init__(self) -> None:
            pass

        def pdf_to_image(self, input_pdf_path, pdf_to_image_output, filename):
            try:
                """
                The Given Function Can be used for the converting pdf Files Into Image
                """
                OUTPUT_FOLDER = None
                FIRST_PAGE = None
                LAST_PAGE = None
                FORMAT = 'jpg'
                USERPWD = None
                USE_CROPBOX = False
                STRICT = False

                # For Stamp Paper
                images = convert_from_path(pdf_path=input_pdf_path, dpi=70, output_folder=OUTPUT_FOLDER,
                                           first_page=FIRST_PAGE, last_page=LAST_PAGE, fmt=FORMAT,
                                           userpw=USERPWD, use_cropbox=USE_CROPBOX, strict=STRICT,
                                           poppler_path=r'C:\Program Files\poppler-22.04.0\Library\bin')

                for i, image in enumerate(images):
                    os.makedirs(pdf_to_image_output, exist_ok=True)
                    fname = pdf_to_image_output + \
                        "\\" + str(i) + filename + '.jpg'
                    image.save(fname, "JPEG")

            except Exception as e:
                logging.info(f"Their Is Error In pdf_to_image Function : {e}")
                # pass

        def image_to_pdf_ocr(self, pdf_to_image_output, image_to_pdf_ocr_output):
            try:
                """
                The Given Function Can be used for the converting Images Files Into PDF Using OCR
                """
                list_dir = os.listdir(pdf_to_image_output)
                list_dir.sort(key=lambda f: int(re.sub(r'\D', '', f)))

                for i in list_dir:
                    image_basename = os.path.splitext(i)[0]

                    img = cv2.imread(pdf_to_image_output + "\\" + i, 1)

                    result = pytesseract.image_to_pdf_or_hocr(
                        img, lang="eng", config=tessdata_dir_config)

                    os.makedirs(image_to_pdf_ocr_output, exist_ok=True)
                    f = open(image_to_pdf_ocr_output + "\\" +
                             image_basename + ".pdf", "w+b")

                    f.write(bytearray(result))
                    f.close()

            except Exception as e:
                logging.info(
                    f"Their Is Error In image_to_pdf_ocr Function : {e}")
                pass

        def merge_pdfs(self, image_to_pdf_ocr_output, filename):
            try:
                """
                The Given Function Can be used for the Combined All The PDF That We Take From Above Function
                """
                os.makedirs(combine_pdf_file, exist_ok=True)
                pdf_list = os.listdir(image_to_pdf_ocr_output)

                pdf_list = [pdf for pdf in pdf_list if '.pdf' in pdf]
                pdf_list.sort(key=lambda f: int(re.sub(r'\D', '', f)))

                mergedObject = PdfFileMerger()

                for file in pdf_list:
                    fullpath = os.path.join(image_to_pdf_ocr_output, file)
                    mergedObject.append(PdfFileReader(fullpath, 'rb'))

                output = os.path.join(combine_pdf_file, filename)
                mergedObject.write(output)

            except Exception as e:
                logging.info(f"Their Is Error In merge_pdfs Function : {e}")
                pass

        def delimages(self, pdf_to_image_output):
            try:
                """
                The Given Function Can Be Used For Deleting The Files Which Are Created By 1st Function
                """
                images_list = os.listdir(pdf_to_image_output)
                images_list = [jpg for jpg in images_list if '.jpg' in jpg]

                for file in images_list:
                    imagepath = os.path.join(pdf_to_image_output, file)
                    os.remove(imagepath)

            except Exception as e:
                logging.info(f"Their Is Error In delimages Function : {e}")
                pass

        def delpdfimages(self, image_to_pdf_ocr_output):
            try:
                """
                The Given Function Can Be Used For Deleting The Files Which Are Created By 2nd Function
                """
                pdflist = os.listdir(image_to_pdf_ocr_output)
                pdflist = [pdf for pdf in pdflist if '.pdf' in pdf]

                for file in pdflist:
                    pdffilepath = os.path.join(image_to_pdf_ocr_output, file)
                    os.remove(pdffilepath)

            except Exception as e:
                logging.info(f"Their Is Error In delpdfimages Function : {e}")
                pass

        def ocr(self, input_file_path):
            if not os.path.isfile(input_file_path):
                logging.error("Input file path is not valid.")
                return None

            logging.info("Started conversion")
            logging.info(f"The current file execution is started: {input_file_path}")

            filename = os.path.basename(input_file_path)
            file_name_without_extension = os.path.splitext(filename)[0]

            self.pdf_to_image(input_file_path, pdf_to_image_output, file_name_without_extension)
            logging.info("The pdf_to_image function is executed")

            self.image_to_pdf_ocr(pdf_to_image_output, image_to_pdf_ocr_output)
            logging.info("The image_to_pdf_ocr function is executed")

            self.merge_pdfs(image_to_pdf_ocr_output, file_name_without_extension + '.pdf')
            logging.info("The merge_pdfs function is executed")

            self.delimages(pdf_to_image_output)
            logging.info("The delimages function is executed")

            self.delpdfimages(image_to_pdf_ocr_output)
            logging.info("The delpdfimages function is executed")

            output_file_path = os.path.join(combine_pdf_file, file_name_without_extension + '.pdf')
            logging.info("Finished conversion")
            logging.info("*" * 50)

            return output_file_path

    except Exception as e:
        logging.info(f"Their Is Error In OCR Class : {e}")
        pass


vil_ocr = OCR()

ocr_conversion = vil_ocr.ocr(input_file)
print(ocr_conversion)