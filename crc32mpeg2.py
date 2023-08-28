# def calculate_crc(data):
#     crc = 0xFFFFFFFF  # Başlangıç değeri
#     polynomial = 0x04C11DB7  # CRC polinomu
#
#     for byte in data:
#         crc ^= byte << 24
#         for _ in range(8):
#             if crc & 0x80000000:
#                 crc = (crc << 1) ^ polynomial
#             else:
#                 crc <<= 1
#
#     return crc & 0xFFFFFFFF  # Sonucun bit tersi alınıyor
#
# data = b'58 0 1 10 1 0 0 0' ## 0xBB08EC87
# data = hex(data)
# crc_result = calculate_crc(data)
#
# print(f"CRC-32/MPEG-2 formatında hesaplanan CRC: {crc_result:08X}")
#
# import binascii
#
# data = b'\x58\x00\x01\x10\x01\x00\x00\x00'
# hex_data = binascii.hexlify(data).decode()
#
# print(hex_data)

# import zlib
#
# data = b'\x58\x00\x01\x10\x01\x00\x00\x00'
#
# crc_result = zlib.crc32(data) & 0xFFFFFFFF
#
# print(f"CRC-32/MPEG-2 formatında hesaplanan CRC: {crc_result:08X}")

# import zlib
#
# def calculate_crc32(data, polynomial):
#     crc32_value = zlib.crc32(data, polynomial)
#     return crc32_value
#
# # data = b"58 0 1 10 1 0 0 0"
# ##0x3A 0x00 0x01 0x10 0x01 0x00 0x00 0x00
# data = "\x3A\x00\x01\x10\x01\x00\x00\x00"
# custom_polynomial = 0x04C11DB7  # Örnek olarak farklı bir polinom
# crc32_result = calculate_crc32(data, custom_polynomial)
# print(f"CRC-32 value: {crc32_result:08X}")

# import binascii
#
# def calculate_mpeg2_crc32(data):
#     crc32 = binascii.crc32(data) & 0xFFFFFFFF  # Calculate the CRC32 and mask to 32 bits
#
#     return crc32
#
# # Example MPEG-2 data stream (replace this with your actual data)
# mpeg2_data = b'\x3A\x00\x01\x10\x01\x00\x00\x00'
#
# crc32_value = calculate_mpeg2_crc32(mpeg2_data)
# crc32_hex = format(crc32_value, '08X')  # Convert to hex with leading zeros
#
# print("CRC32 Value:", crc32_hex)

def calculate_custom_crc32(data, polynomial):
    crc = 0xFFFFFFFF
    for byte in data:
        crc ^= byte << 24
        for _ in range(8):
            crc = (crc << 1) ^ polynomial if crc & 0x80000000 else crc << 1
        crc &= 0xFFFFFFFF
    return crc

# Example MPEG-2 data stream (replace this with your actual data)
# mpeg2_data = b'\x3a\x00\x01\x10\x00\x00\x00\x00'
# print(mpeg2_data)
# custom_polynomial = 0x04C11DB7  # Replace this with your desired polynomial
#
# crc32_value = calculate_custom_crc32(mpeg2_data, custom_polynomial)
# crc32_hex = format(crc32_value, '08X')  # Convert to hex with leading zeros
# crc32_bytes = [(crc32_value >> (24 - 8 * i)) & 0xFF for i in range(4)]
#
# dataSend = bytes([58, 0, 1, 16, 0, 0])
#
# combined_data = mpeg2_data + bytes(crc32_bytes)
#
# combined_bytes = bytes(combined_data)
# print("Combined data as bytes:", combined_bytes)
#
# say = 1
# liste = []
# for i in crc32_hex:
#     if say % 2 == 0:
#         a = f"{crc32_hex[say - 2:say]}"
#         liste.append(a)
#
#     say+=1
#
# decimal_list = []
#
# for hex_value in liste:
#     decimal_value = int(hex_value, 16)
#     decimal_list.append(decimal_value)
# decimal_list.append(59)
# print(decimal_list)

#
# newListe = []
# for i in liste:
#     new = i[0:]
#
# print(ornekByte)
# # input_data = "58 0 1 16 1 0"
# # values = input_data.split()  # Boşluklarla ayır
# #
# # hex_format_values = []
# # for value in values:
# #     hex_value = "\\x" + hex(int(value))[2:].zfill(2)  # Değeri hexadecimal formatına çevir
# #     hex_format_values.append(hex_value)
# #
# # hex_string = "".join(hex_format_values)
# # print(hex_string)
#
# input_data = "58 0 1 16 1 0"
# values = input_data.split()  # Boşluklarla ayır
#
# byte_array = []
# for value in values:
#     byte_array.append(int(value))  # Değeri bayt olarak ekle
#     byte_string = bytes(byte_array)
#     # print(byte_string)
#
#
#
from crccheck.crc import Crc32Mpeg2
import math
#
# mpeg2_data = b'\x3A\x01\x00\x10\x06\x04\x00\x3B\x26\x19\x00\x00'
# ## 9F DC AE A6 3B
# crc32_calculator = Crc32Mpeg2()
# crc32_value = crc32_calculator.calc(mpeg2_data)
#
# print("CRC-32/MPEG-2 value:", format(crc32_value, '08X'))
#
# crc32_value = str(crc32_value)

# veri = "3A 01 00 10 06 04 00 3B 26 19 9F DC AE A6 3B"
#
#
# def dataToAscii(input_data):
#     values = input_data.split()  # Boşluklarla ayır
#
#     byte_array = bytearray()
#     for value in values:
#         byte_array.append(int(value))  # Değeri bayt olarak ekle
#
#     byte_string = bytes(byte_array)
#     return byte_string
#
#
# def getAndControlCRC(veri):
#     dataNumber = veri.split(" ")[4]
#     parameter = int(veri.split(" ")[5])
#
#     ## veri alma
#     dataSayac = 1
#     reciveData = ""
#     for j in range(parameter):
#         reciveData += veri.split(" ")[parameter + 1 + dataSayac]
#         dataSayac += 1
#
#     ## crc alma
#     crcInfo = 5 + parameter + 1
#     finishCrc = crcInfo + 4
#     print(reciveData)
#     crcData = ""
#     for i in range(crcInfo, finishCrc):
#         crcData += veri.split(" ")[i]
#
#
#     print(crcData)
#     ## 4 ün katı kontrolü
#     ## 10
#     ## 17 / 4 = 4,25
#     ## önce toplam parametre sayısında kaç tane 4 var buluyoruz sonra bulduğumuz sayıyı ceil ile ondalık kısmı varsa yukarısındaki sayıya atıyoruz
#     ## ceil ile dönüştürdüğümüz sayıyı 4 ile çarpıp toplam parametere sayısından çıkarınca eklenmesi gerek 0 sayısını buluyoruz
#     veriToplamParametre = parameter + dataSayac + 1
#     olmasiGereken = math.ceil((veriToplamParametre) / 4)
#     olmasiGereken = 4 * olmasiGereken
#     eklenecekVeriSayisi = olmasiGereken - (veriToplamParametre)
#     ## for crc new data 4^
#     newData = ""
#     for k in range(veriToplamParametre):
#         newData += veri.split(" ")[k] + " "
#
#     for ekle in range(eklenecekVeriSayisi):
#         if ekle == eklenecekVeriSayisi - 1:
#             newData += "00"
#         else:
#             newData += "00 "
#
#     print(newData)
#
#     hex_liste = newData.split()
#     decimal_degerler = [int(deger, 16) for deger in hex_liste]
#     # Decimal değerleri string olarak birleştirin
#     decimal_metin = ' '.join(map(str, decimal_degerler))
#
#     print(decimal_metin)
#
#     mpeg2_data = dataToAscii(decimal_metin)
#     print("mpeg2 data : ",mpeg2_data)
#     crc32_calculator = Crc32Mpeg2()
#     crc32_value = crc32_calculator.calc(mpeg2_data)
#     crcHex = format(crc32_value, '08X')
#
#     print("Gelen crc: ", crcData)
#     print("Hesaplanan Crc: ", crcHex)
#
#
# getAndControlCRC(veri)




# dataNumber = veri.split(" ")[4]
# parameter = int(veri.split(" ")[5])
# #
# ## veri alma
# dataSayac = 1
# reciveData = ""
# for j in range(parameter):
#     reciveData += veri.split(" ")[parameter+1 + dataSayac]
#     dataSayac += 1
#
# ## 4 ün katı kontrolü
# ## 10
# ## 17 / 4 = 4,25
# ## önce toplam parametre sayısında kaç tane 4 var buluyoruz sonra bulduğumuz sayıyı ceil ile ondalık kısmı varsa yukarısındaki sayıya atıyoruz
# ## ceil ile dönüştürdüğümüz sayıyı 4 ile çarpıp toplam parametere sayısından çıkarınca eklenmesi gerek 0 sayısını buluyoruz
# veriToplamParametre = parameter+dataSayac+1
# olmasiGereken = math.ceil((veriToplamParametre)/4)
# olmasiGereken = 4*olmasiGereken
# eklenecekVeriSayisi = olmasiGereken - (veriToplamParametre)
# ## for crc new data 4^
# newData = ""
# for k in range(veriToplamParametre):
#     newData += veri.split(" ")[k]+" "
#
# for ekle in range(eklenecekVeriSayisi):
#     if ekle == eklenecekVeriSayisi-1:
#         newData += "00"
#     else:
#         newData += "00 "
#
# print(newData)
#
#
# ## crc alma
# crcInfo = 5+parameter+1
# finishCrc = crcInfo+4
# print(reciveData)
# crcData = ""
# for i in range(crcInfo,finishCrc):
#     crcData += veri.split(" ")[i]
#
# print(crcData)
# Boş bir sözlük oluşturun

# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
# from PyQt5.QtGui import QPdfWriter
# from PyQt5.QtCore import Qt
#
# class PDFExportApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle("PDF Export")
#         self.setGeometry(100, 100, 400, 200)
#
#         self.exportButton = QPushButton("Export to PDF", self)
#         self.exportButton.setGeometry(150, 80, 150, 40)
#         self.exportButton.clicked.connect(self.exportToPDF)
#
#     def exportToPDF(self):
#         options = QFileDialog.Options()
#         options |= QFileDialog.ReadOnly
#         options |= QFileDialog.DontUseNativeDialog
#         fileName, _ = QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options)
#
#
#
#         if fileName:
#             # PDF dosyasını oluşturun
#             pdf = QPdfWriter(fileName)
#
#             pdf.setCreator("Your Application Name")
#             pdf.setTitle("Exported PDF")
#
#             # PDF içeriğini burada ekleyin, örneğin:
#             # painter = QPainter()
#             # painter.begin(pdf)
#             # painter.drawText(100, 100, "Hello, PDF!")
#             # painter.end()
#
#             print(f"PDF dosyası başarıyla oluşturuldu ve {fileName} adıyla kaydedildi.")
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = PDFExportApp()
#     window.show()
#     sys.exit(app.exec_())