from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import platform
from tempfile import TemporaryDirectory
from pathlib import Path
 
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import requests
from openai import OpenAI
import json
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import time


class Comparison(APIView):
    def get(self, request, *args, **kwargs):
        """
        The GET request to compare two course syllabi and decide whether or not they are equivalent.

        Accepts:
            course_1 (str): The path or URL of the first course syllabus.
            course_2 (str): The path or URL of the second course syllabus.
        
        Returns:
            JSONResponse: The comparison of the two course syllabi in JSON format.
        """
        try:
            # get the course syllabi from the query parameters
            pdf1 = request.query_params.get('course_1', None)
            pdf2 = request.query_params.get('course_2', None)

            if not pdf1 or not pdf2:
                return JsonResponse({"error": "Please provide the path or URL of the two course syllabi."}, status=400)
            
            # read the text content from the PDF files in parallel
            with ThreadPoolExecutor() as executor:
                future1 = executor.submit(read_pdf, pdf1)
                future2 = executor.submit(read_pdf, pdf2)

                pdf1_text = future1.result()
                pdf2_text = future2.result()

            # compare the two course syllabi using OpenAI's GPT-3.5 model
            client = OpenAI() # requires defining the OPENAI_API_KEY environment variable
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[ 
                    # provide the instructions using system role
                    {"role": "system", "content": 'Act like you are a college professor who needs to compare the learning outcomes of two course\
                                                    syllabi and decide whether or not they are equivalent. To compare their similarity, you have to\
                                                    write bullet points for each of the learning outcomes in course 1 and explain in only 1-2 sentences\
                                                    whether or not they are achieved in course 2. The output must be in JSON format where the key is the\
                                                    course learning objective from course 1 and the value is the explanation. At the end, add a key to the\
                                                    json called "match percentage" and have its value be the percentage of learning outcomes from course 1\
                                                    that matched. Remember the response must be a valid JSON object with no nested objects.'},
                    # provide the course syllabi as the user input                                                
                    {"role": "user", "content": f"Course 1: {pdf1_text}"},
                    {"role": "user", "content": f"Course 2: {pdf2_text}"},
                ]
            )

            # get the response from the model
            primary_answer = response.choices[0].message.content

            if primary_answer is None:
                return JsonResponse({"error": "the model did not return a response"}, status=500)
            
            # extract the JSON response from the model's output
            primary_answer = primary_answer[primary_answer.find("{"):primary_answer.rfind("}")+1]
            primary_answer = json.loads(primary_answer)
        
            return JsonResponse(primary_answer, safe=False)
        except:
            return JsonResponse({"error": "An error occurred while processing the request."}, status=500)


def read_pdf(file):
    """
    Reads the text content from a PDF file.

    Args:
        file (str): The path or URL of the PDF file.

    Returns:
        str: The extracted text content from the PDF file.
    """
    # requires tesseract to be installed
    # windows: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-setup-3.05.00dev-205-ge205c59.exe
    # linux: sudo apt-get install -y tesseract-ocr && sudo apt-get install -y poppler-utils
    if platform.system() == "Windows":
        local = os.getenv('LOCALAPPDATA')
        tesseract_path = os.path.join(local, "Tesseract-OCR") # type: ignore
        tesseract_exe = os.path.join(tesseract_path, "tesseract.exe") # type: ignore
        pytesseract.pytesseract.tesseract_cmd = tesseract_exe

    if file.startswith("http"):
        PDF_file = Path("temp.pdf")
        with open(PDF_file, "wb") as f:
            f.write(requests.get(file).content)
    else:
        PDF_file = Path(file)

    image_file_list = []
    pdf_text = ""

    with TemporaryDirectory() as tempdir:

        pdf_pages = convert_from_path(PDF_file, 500)
        
        for page_enumeration, page in enumerate(pdf_pages, start=1):
            filename = f"{tempdir}\\page_{page_enumeration:03}.jpg"
            page.save(filename, "JPEG")
            image_file_list.append(filename)

        for image_file in image_file_list:
            text = str(((pytesseract.image_to_string(Image.open(image_file)))))
            text = text.replace("-\n", "")
            pdf_text += text
        
    return pdf_text