import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from datetime import datetime
import random

def draw_colored_text_box(canvas, x, y, width, height, text,color):
    # Kutucuk içine metni ve renkli arka planı çizen fonksiyon
    canvas.saveState()

    if color == "white":
        canvas.setFillColorRGB(1, 1, 1)  # Beyaz arka plan rengi (RGB formatında)
    elif color == "gray":
        canvas.setFillColorRGB(0.8, 0.8, 0.8)  # Açık gri arka plan rengi (RGB formatında)

    canvas.rect(x, y, width, height, fill=True)
    canvas.setStrokeColorRGB(198, 226, 255) ## siyah kenarlar
    canvas.setLineWidth(1)
    canvas.rect(x, y, width, height)
    canvas.setFont("Helvetica", 10)
    canvas.setFillColorRGB(0, 0, 0)  # Siyah metin rengi (RGB formatında
    canvas.drawString(x + 5, y + height - 11.7, text)
    canvas.restoreState()

def create_pdf_with_data(data_dict, veriDict,file_path, image_path, report_num):
    location_file = str(os.getcwd())
    replace = location_file.replace("\\", "/")
    c = canvas.Canvas(f"{file_path}", pagesize=letter)

    # Üst kısımdaki resim ve tarih, rapor numarasını eklemek
    c.drawImage(image_path, 35, 705, width=550, height=57)
    c.setFont("Helvetica", 14)
    now = datetime.now().date()
    year = now.year
    month = now.month
    day = now.day

    rand = random.randint(100,1000)
    c.drawString(400, 670, f"Tarih : {day}.{month}.{year}")
    c.drawString(100, 670, f"Rapor No : {year}{month}{day}{rand}")

    # Verileri düzenli bir şekilde yazdırma
    c.setFont("Helvetica-Bold", 16)
    y_position = 585  # Verilerin başlangıç yüksekliği
    say = 0
    sayac = 1

    for key, value in data_dict.items():
        color = "white" if say == 0 else "gray"

        ## veri alma
        data = veriDict[f'16 {sayac}']

        sayac += 1
        ## veri alma


        draw_colored_text_box(c, 70, y_position, 460, 15, f"{value}: {data}", color)
        say = 1 - say  # Sıradaki rengi değiştirmek için

        y_position -= 15.4  # Sonraki kutucuğa geçmek için

    c.save()