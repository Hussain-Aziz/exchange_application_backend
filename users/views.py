from django.http import JsonResponse
from rest_framework.views import APIView
import os
import platform
from tempfile import TemporaryDirectory
from pathlib import Path
 
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import requests
from openai import OpenAI, OpenAIError
import json
from concurrent.futures import ThreadPoolExecutor
import time
from users.models import CourseApplication

class Comparison(APIView):
    def get(self, request):
        try:
            # get the course syllabi from the query parameters
            pdf1 = request.query_params.get('course_1', None)
            pdf2 = request.query_params.get('course_2', None)

            if not pdf1 or not pdf2:
                return JsonResponse({"error": "Please provide the path or URL of the two course syllabi."}, status=400)
            
            # compare the two course syllabi
            comparison_result = compare(pdf1, pdf2)
            return JsonResponse(comparison_result, safe=False)
        
        except Exception as e:
            return JsonResponse({"error": f"An error occurred while processing the request: {e}" }, status=500)

class ComparisonOnApplication(APIView):
    def get(self, request):

        id = request.query_params.get('id', None)
        if not id:
            return JsonResponse({"error": "Please provide the course application ID."}, status=400)

        course = CourseApplication.objects.filter(course_application_id=id).first()

        if not course:
            return JsonResponse({"error": "Course application not found."}, status=404)

        success, result = do_comparison_on_application(course)
        if success:
            return JsonResponse(result, safe=False)
        else:
            return JsonResponse({"error": f"An error occurred while processing the request: {result}" }, status=500)

def read_pdf(file, pdf_num):
    if platform.system() == "Windows":
        local = os.getenv('LOCALAPPDATA')
        tesseract_path = os.path.join(local, "Tesseract-OCR") # type: ignore
        tesseract_exe = os.path.join(tesseract_path, "tesseract.exe") # type: ignore
        pytesseract.pytesseract.tesseract_cmd = tesseract_exe

    if file.startswith("http"):
        PDF_file = Path(f"temp{pdf_num}.pdf")
        if PDF_file.exists():
            PDF_file.unlink()
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

def pdf_read_with_retry(file, pdf_num):
    for _ in range(3):
        try:
            return read_pdf(file, pdf_num)
        except Exception as e:
            print(f"Error reading PDF: {str(e)}")
            time.sleep(2)
    raise Exception(f"Failed to read the PDF file from {file}.")
    
def compare(pdf1, pdf2):
    # read the text content from the PDF files in parallel
    with ThreadPoolExecutor() as executor:
        future1 = executor.submit(pdf_read_with_retry, pdf1, 1)
        future2 = executor.submit(pdf_read_with_retry, pdf2, 2)

        pdf1_text = future1.result()
        pdf2_text = future2.result()

    # compare the two course syllabi using OpenAI's GPT model
    try:
        client = OpenAI() # requires defining the OPENAI_API_KEY environment variable
        response = client.chat.completions.create(
            #model="gpt-4-turbo-2024-04-09",
            model="gpt-3.5-turbo-0125",
            messages=[ 
                # provide the instructions using system role
                {"role": "system", "content": 'Act like you are a college professor who needs to compare the learning outcomes of two course\
                                                syllabi and decide whether or not they are equivalent. To compare their similarity, you have to\
                                                write bullet points for each of the learning outcomes in course 1 and explain in only 1-2 sentences\
                                                whether or not they are achieved in course 2. The output must be in JSON format where the key is the\
                                                course learning objective from course 1 and the value is the explanation. At the end, add a key to the\
                                                json called "match percentage" and have its value be the percentage of learning outcomes from course 1\
                                                that matched. Remember the response must be a valid JSON object with no nested objects and must have a match percentage.'},
                # provide the course syllabi as the user input                                                
                {"role": "user", "content": f"Course 1: {pdf1_text}"},
                {"role": "user", "content": f"Course 2: {pdf2_text}"},
            ]
            )
    except OpenAIError as e:
        raise Exception(f"OpenAI Error: {str(e)}")   

    # get the response from the model
    primary_answer = response.choices[0].message.content

    if primary_answer is None:
        raise Exception("The model did not return a response.")
    
    # extract the JSON response from the model's output
    primary_answer = primary_answer[primary_answer.find("{"):primary_answer.rfind("}")+1]
    primary_answer = json.loads(primary_answer)

    return primary_answer

def disallow_multiple_comparisons(course_application):
    print("Comparison is already running. Waiting for the result...")
    time_slept = 0
    while course_application.running_comparison and time_slept < 300: # max 5 minutes
        time.sleep(10)
        time_slept += 10
        course_application.refresh_from_db()
    course_application.refresh_from_db()
    if course_application.comparison_result:
        return (True, course_application.comparison_result)
    else:
        # force it to stop
        if course_application.running_comparison:
            course_application.running_comparison = False
            course_application.save()
        return (False, "Comparison is still running. Please try again later.")

def do_comparison_on_application(course_application):
    if course_application.running_comparison:
        return disallow_multiple_comparisons(course_application)
    
    if course_application.comparison_result is not None:
        return (True, course_application.comparison_result)
        
    course_application.running_comparison = True
    course_application.save()
    try:
        course1_syllabus = course_application.aus_syllabus
        course2_syllabus = course_application.syllabus

        compare_result = compare(course1_syllabus, course2_syllabus)
        course_application.comparison_result = compare_result
        course_application.running_comparison = False
        course_application.save()
        return (True, compare_result)
    except Exception as e:
        course_application.running_comparison = False
        course_application.save()
        return (False, str(e))