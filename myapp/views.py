# Django import start
from django.shortcuts import render
from myapp.models import Contact, Image as C_Image 
from datetime import datetime
from django.contrib import messages
from .forms import ImageForm
# Django import end

# ML import start

import pytesseract
import os
from PIL import ImageEnhance, ImageFilter, Image
import cv2
import matplotlib.pyplot as plt
import googletrans
from googletrans import Translator
from langdetect import detect
# ML import Ends

# ML pytesseract path start
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# ML pytesseract path end

# ML Store array start
languages = ['hin', 'mar','ben', 'guj', 'pan', 'tam', 'tel', 'kan',
              'eng', 'spa', 'rus', 'por', 'ita', 'gre', 'fra', 'nep', 'lta']
lang_string = '+'.join(languages)
# ML Store array ends

pytess_dict = {
    'hindi': 'hin',
    'marathi': 'mar',
    'bengali' : 'ben',
    'gujarati' : 'guj',
    'punjabi': 'pan',


    'tamil': 'tam',
    'telugu': 'tel',
    'kannada': 'kan',
    'english' : 'eng',
    'spanish': 'spa',
    
    'russian': 'rus',
    'portuguese': 'por',
    'italian': 'ita',
    'greek' : 'gre',
    'french': 'fra',

    'Nepali': 'nep',
    'Latin': 'lta',
   
}

spt_img_extension = ['.png','.jpg','.jpeg','.jfif']

# Create your views here.


def home(request):
    langip = ''
    transip = ''
    if request.method == "POST":
        langip = request.POST.get('lang_ip')
        transip = request.POST.get('trans_ip')
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Image have been successfully submitted!")
    form = ImageForm()

    if langip and transip:
        Img = C_Image.objects.filter().last()

        img_path = 'media/' + str(Img.photo)
        split_tup = os.path.splitext(img_path)
        print(f"----------------> {split_tup}")
        print(f"image path---->{img_path} ---- {split_tup[1]}")
        extension = split_tup[1]
        if extension.lower() in spt_img_extension:
            if langip == "Auto Detect":
                lang_code_ip = lang_string
                print(f"If Auto Detect Pressed--> {lang_code_ip}")

                img = cv2.imread(img_path)
                imgH, imgW,_ = img.shape


                # here we have to provide "lang_code_ip" variable
                

                try:
                    imgbox = pytesseract.image_to_boxes((img_path), lang = lang_code_ip ,timeout = 90)
                    for boxes in imgbox.splitlines():
                        boxes = boxes.split(' ')
                        x,y,w,h = int(boxes[1]),int(boxes[2]),int(boxes[3]),int(boxes[4])
                        cv2.rectangle(img,(x,imgH-y),(w,imgH-h),(231, 76, 60),3)
                except:
                    imgbox = "Error Occured Unable Detect Text from provided image...!!!!"

                

                plt.imshow(img)
                plt.savefig('media/plotimage/plot.png')

                try:
                    img2char = pytesseract.image_to_string((img_path), lang = lang_code_ip,timeout = 90)
                    detectedLangCode = detect(img2char)
                    detectedLangName = googletrans.LANGUAGES.get(detectedLangCode)
                except:
                    img2char = "Error Occured Unable Extract Text from provided image...!!!!"
                    detectedLangCode = " "
                    detectedLangName = " "            

                translator = Translator()
                transip = transip.strip()
                if (transip.isalpha()):
                    key_list = list(googletrans.LANGUAGES.keys())
                    val_list = list(googletrans.LANGUAGES.values())

                    position1 = val_list.index(transip.lower())
                    src_from = detectedLangCode
                    translated_to = key_list[position1]
                else:
                    print("Please Enter Valid Input.")
                
                try:
                    # img2char = pytesseract.image_to_string(img_path, lang=lang_code_ip)
                    translated_text = translator.translate(text=img2char, dest=translated_to, src=src_from)
                except:
                    context = {
                    'form': form,
                    'img': Img,
                    'img2char': img2char,
                    'translated_text': "Blank Image Uploaded......!",
                    'plot_path' : "Blank Image Uploaded......!",
                    'From_lang' : " ",
                    'To_lang' : " "
                    }
                else:
                    context = {
                    'form': form,
                    'img': Img,
                    'img2char': img2char,
                    'translated_text': translated_text.text,
                    'plot_path' : "media/plotimage/plot.png",
                    'From_lang' : detectedLangName,
                    'To_lang' : transip
                    }
            else:
                lang_code_ip = pytess_dict.get(langip.lower())
                print(f"If Auto Detect Not Pressed--> {lang_code_ip}")
            
                translator = Translator()
                transip = transip.strip()
                if (transip.isalpha()):
                    key_list = list(googletrans.LANGUAGES.keys())
                    val_list = list(googletrans.LANGUAGES.values())

                    position1 = val_list.index(transip.lower())
                    position2 = val_list.index(langip.lower())
                    src_from = key_list[position2]
                    translated_to = key_list[position1]
                else:
                    print("Please Enter Valid Input.")
        

                img = cv2.imread(img_path)
                imgH, imgW,_ = img.shape


                # here we have to provide "lang_code_ip" variable
                imgbox = pytesseract.image_to_boxes((img_path), lang = lang_code_ip)

                for boxes in imgbox.splitlines():
                    boxes = boxes.split(' ')
                    x,y,w,h = int(boxes[1]),int(boxes[2]),int(boxes[3]),int(boxes[4])
                    cv2.rectangle(img,(x,imgH-y),(w,imgH-h),(231, 76, 60),3)

                plt.imshow(img)
                plt.savefig('media/plotimage/plot.png')
                
                # Plot Image Logic Ends


                try:
                    img2char = pytesseract.image_to_string(img_path, lang=lang_code_ip)
                    translated_text = translator.translate(text=img2char, dest=translated_to, src=src_from)
                except:
                    context = {
                    'form': form,
                    'img': Img,
                    'img2char': img2char,
                    'translated_text': "Blank Image Uploaded......!",
                    'plot_path' : "Blank Image Uploaded......!",
                    'From_lang' : " ",
                    'To_lang' : " "
                    }
                else:
                    context = {
                    'form': form,
                    'img': Img,
                    'img2char': img2char,
                    'translated_text': translated_text.text,
                    'plot_path' : "media/plotimage/plot.png",
                    'From_lang' : langip,
                    'To_lang' : transip
                    }
        else:
            context = {
                'form': form,
                'img': Img,
                'img2char': " ",
                'translated_text': "Image Extension does not supported. Please upload only .png , .jpeg , .jpg , .jfif",
                'plot_path' : "Image Extension does not supported. Please upload only .png , .jpeg , .jpg , .jfif",
                'From_lang' : " ",
                'To_lang' : " "
            }    
    else:
        context = {
        'form': form,
        'img': "Not yet uploaded",
        'img2char': "Not yet uploaded",
        'translated_text': "Not yet uploaded",
        'plot_path' : "Not yet uploaded",
        'From_lang' : "",
        'To_lang' : ""
        }    
    return render(request, 'home.html', context)

# ----------------------------------------------------------------------------------

def textupload(request):
    text_area = 'Please write something....'
    text_ip = 'english'
    text_trans = 'english'
    if request.method == "POST":
        text_area = request.POST.get('textarea_input')
        text_ip = request.POST.get('lang_ip')
        text_trans = request.POST.get('trans_ip')

    print(f"{text_area} \n  {text_ip} \n {text_trans}")

    translator = Translator()
    src_form =  'en'
    translated_to = 'mr'
    
    if(text_ip == "Auto Detect"):
        src_from = detect(text_area)
        print(f"-------------> {src_from}")
        detectedLangName = googletrans.LANGUAGES.get(src_from)
        translated_to = 'mr'

        if (text_trans.isalpha()):
            key_list = list(googletrans.LANGUAGES.keys())
            val_list = list(googletrans.LANGUAGES.values())
            position1 = val_list.index(text_trans.lower())
            translated_to = key_list[position1]
        else:
            print("Please Enter Valid Input.")
    else:
        detectedLangName = text_ip
        text_trans = text_trans.strip()
        if (text_trans.isalpha()):
            key_list = list(googletrans.LANGUAGES.keys())
            val_list = list(googletrans.LANGUAGES.values())

            position1 = val_list.index(text_trans.lower())
            position2 = val_list.index(text_ip.lower())
            src_from = key_list[position2]
            translated_to = key_list[position1]
        else:
            print("Please Enter Valid Input.")


    translated_text = translator.translate(
        text=text_area, dest=translated_to, src=src_from) 

    context = {
        'text_area_ip' : text_area,
        'translated_text' : translated_text.text,
        'detectedLangName' : detectedLangName.upper(),
        # 'From_lang' : text_ip,
        # 'To_lang' : text_trans
    }
        
    return render(request,'textupload.html',context)
# -------------------------------------------------------------------------------

def about(request):
    # return HttpResponse('Hello Sumit ....From about')
    return render(request, 'about.html')

# -------------------------------------------------------------------------------

def services(request):
    # return HttpResponse('Hello Sumit ....From services')
    return render(request, 'services.html')

# -------------------------------------------------------------------------------

def contact(request):
    # return HttpResponse('Hello Sumit ....From contact')
    if request.method == 'POST':
        mail = request.POST.get('mail')
        password = request.POST.get('password')
        Address = request.POST.get('address')
        Address2 = request.POST.get('address2')
        mob_num = request.POST.get('mobile')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        date = request.POST.get('')
        contact = Contact(mail=mail, password=password, Address=Address, Address2=Address2,
                          mob_num=mob_num, city=city, state=state, zip=zip, date=datetime.today())
        contact.save()
        messages.success(request, "Your Form has been successfully submitted!")

    return render(request, 'contact.html')

    # -------------------------------------------------------------------------------
