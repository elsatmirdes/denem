import math

from PyQt5.QtWidgets import QMessageBox, QFileDialog
from crcmod import crcmod

from LoadingThread import LoadingThread
from loadingScreen import LoadingTranslucentScreen
from form import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSlot
import sys
import time
import serial
from serial.tools import list_ports
import printerDetail
from crccheck.crc import Crc32Mpeg2
import os


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.veri_dict = {
            "16 1": "PART_REF",
            "16 2": "HW_VERSION",
            "16 3": "SW_VERSION",
            "16 4": "SRSID",
            "16 5": "UUIDMH",
            "16 6": "UUIDML",
            "16 7": "UUIDL",
            "16 8": "FRONT LEAF MOTOR THERMIC BREAK EVENTS",
            "16 9": "REAR LEAF MOTOR THERMIC BREAK EVENTS",
            "16 10": "FRONT LEAF MOTOR OVERCURRENT EVENTS (VEHICLE AT REST)",
            "16 11": "FRONT LEAF MOTOR OVERCURRENT EVENTS (VEHICLE MOBILE)",
            "16 12": "REAR LEAF MOTOR OVERCURRENT EVENTS (VEHICLE AT REST)",
            "16 13": "REAR LEAF MOTOR OVERCURRENT EVENTS (VEHICLE MOBILE)",
            "16 14": "DOOR OPENING EVENTS BY SENSITIVE EDGE (VEHICLE AT REST)",
            "16 15": "DOOR OPENING EVENTS BY SENSITIVE EDGE (VEHICLE MOBILE)",
            "16 16": "DOOR OPENING OPERATIONS BY BUTTON",
            "16 17": "DOOR CLOSING OPERATIONS BY BUTTON",
            "16 18": "DOOR OPENING OPERATIONS BY EXTERNAL BUTTON",
            "16 19": "DOOR CLOSING OPERATIONS BY EXTERNAL BUTTON",
            "16 20": "DOOR CLOSING OPERATIONS BY VEHICLE MOVE OFF",
            "16 21": "DOOR CLOSING OPERATIONS BY HANDBRAKE",
            "16 22": "DOOR CLOSING OPERATIONS BY IGNITION TURN OFF",
            "16 23": "DOOR CLOSING OPERATIONS BY REMOTE CONTROL",
            "16 24": "DOOR OPENING OPERATIONS BY REMOTE CONTROL",
            "16 25": "DOOR OPENING OPERATIONS IN SINGLE LEAF MODE",
            "16 26": "DOOR CLOSING OPERATIONS IN SINGLE LEAF MODE",
            "16 27": "DISABLED PASSENGER RAMP OPERATIONS",
            "16 28": "EMERGENCY RELEASE OPERATIONS",
            "16 29": "MAXIMUM VOLTAGE ON VEHICLE",
            "16 30": "MINIMUM VOLTAGE WHILE DOOR IS BEING OPERATED",
            "16 31": "FRONT LEAF CLOSED POSITION SWITCH OPERATIONS",
            "16 32": "REAR LEAF CLOSED POSITION SWITCH OPERATIONS",
            "16 33": "FRONT LEAF OPEN POSITION SWITCH OPERATIONS",
            "16 34": "REAR LEAF OPEN POSITION SWITCH OPERATIONS",
            "16 35": "DOOR DIRECTION REVERSAL BY BUTTON",
            "16 36": "VEHICLE MOVE OFF EVENTS WITH HANDBRAKE PULLED",
            "16 37": "MAXIMUM NUMBER OF DOOR OPERATIONS AT ONE REST TIME"
        }
        self.cskVersion = {
            "1":"CSK.737022.AA"
        }

        self.com = ""
        self.connInfo = False
        self.reciveData = {}


        self.ui.print.clicked.connect(self.printData)
        self.ui.readRecords.clicked.connect(self.readRecords)

        self.ui.connect.clicked.connect(self.connectPort)


        self.ui.readRecords.setEnabled(False)
        self.ui.print.setEnabled(False)

    def send_message(self,data_to_send):
        # try:
        #     # Veriyi sayılara dönüştürme
        #     sayilar = [int(x) for x in message.split()]
        #
        #     for sayi in sayilar:
        #         self.serial_port.write(sayi.to_bytes(1, byteorder='big'))
        #         print(sayi)
        # except:
        #     pass
        print(data_to_send)
        try:
            # Veriyi gönder
            self.serial_port.write(data_to_send)
            print("Veri gönderildi:", data_to_send)

        except Exception as e:
            print("Hata:", e)

    def receive_message(self):
        # start_time = time.time()  # Başlangıç zamanını kaydedin
        # try:
        #     while True:
        #         try:
        #             received_data = self.serial_port.read()
        #             print(received_data)
        #             if received_data == b'':
        #                 break
        #             else:
        #                 return received_data
        #         except serial.SerialTimeoutException:
        #             pass
        # except:
        #     pass

        try:
            # # Karttan cevap al
            # response = ser.read()  # Beklenen cevap boyutu
            # print("Alınan cevap:", response)

            # Karttan cevap al
            response = b""
            while True:
                byte = self.serial_port.read(1)
                if byte:
                    response += byte
                else:
                    break

            # print("Alınan cevap:", response.decode(encoding="utf-32"))
            hex_string = " ".join("{:02X}".format(byte) for byte in response)

            return hex_string

        except Exception as e:
            print("Hata:", e)

    def dataToAscii(self, input_data):
        values = input_data.split()  # Boşluklarla ayır

        byte_array = bytearray()
        for value in values:
            byte_array.append(int(value))  # Değeri bayt olarak ekle

        byte_string = bytes(byte_array)
        return byte_string

    def getAndControlCRC(self,veri):
        dataNumber = veri.split(" ")[4]
        parameter = int(veri.split(" ")[5])

        ## veri alma
        dataSayac = 1
        reciveData = ""
        for j in range(parameter):
            reciveData += veri.split(" ")[parameter + 1 + dataSayac]
            dataSayac += 1

        ## crc alma
        crcInfo = 5 + parameter + 1
        finishCrc = crcInfo + 4
        crcData = ""
        for i in range(crcInfo, finishCrc):
            crcData += veri.split(" ")[i]


        ## 4 ün katı kontrolü
        ## 10
        ## 17 / 4 = 4,25
        ## önce toplam parametre sayısında kaç tane 4 var buluyoruz sonra bulduğumuz sayıyı ceil ile ondalık kısmı varsa yukarısındaki sayıya atıyoruz
        ## ceil ile dönüştürdüğümüz sayıyı 4 ile çarpıp toplam parametere sayısından çıkarınca eklenmesi gerek 0 sayısını buluyoruz
        veriToplamParametre = parameter + dataSayac + 1
        olmasiGereken = math.ceil((veriToplamParametre) / 4)
        olmasiGereken = 4 * olmasiGereken
        eklenecekVeriSayisi = olmasiGereken - (veriToplamParametre)
        ## for crc new data 4^
        newData = ""
        for k in range(veriToplamParametre):
            newData += veri.split(" ")[k] + " "

        for ekle in range(eklenecekVeriSayisi):
            if ekle == eklenecekVeriSayisi - 1:
                newData += "00"
            else:
                newData += "00 "

        hex_liste = newData.split()
        decimal_degerler = [int(deger, 16) for deger in hex_liste]
        # Decimal değerleri string olarak birleştirin
        decimal_metin = ' '.join(map(str, decimal_degerler))



        ## 16 lık veriyi decimal değere çeviriyoruz crc hesaplaması için
        mpeg2_data = self.dataToAscii(decimal_metin)
        crc32_calculator = Crc32Mpeg2()
        crc32_value = crc32_calculator.calc(mpeg2_data)
        crcHex = format(crc32_value, '08X')

        if crcData == crcHex:
            return True
        else:
            return False

    ## karşıdan gelen verinin crc nin bulur
    def createCRCandData(self,input_data,sayac):
        custom_polynomial = 0x04C11DB7  # Replace this with your desired polynomial
        mpeg2_data = self.dataToAscii(input_data)
        crc32_calculator = Crc32Mpeg2()

        crc32_value = self.calculate_custom_crc32(mpeg2_data, custom_polynomial)
        crc32_hex = format(crc32_value, '08X')  # Convert to hex with leading zeros
        # crc32_bytes = [(crc32_value >> (24 - 8 * i)) & 0xFF for i in range(4)]
        say = 1
        liste = []
        for i in crc32_hex:
            if say % 2 == 0:
                a = f"{crc32_hex[say - 2:say]}"
                liste.append(a)
            say += 1
        decimal_list = []

        for hex_value in liste:
            decimal_value = int(hex_value, 16)
            decimal_list.append(decimal_value)
        decimal_list.append(59)
        listToByte = [58, 0, 1, 16, sayac, 0] + decimal_list

        dataSend = bytes(listToByte)
        return dataSend

    def find_serial_port(self):
        try:
            # Veri gönderme
            # data_to_send = bytes([58, 0, 1, 16, 1, 0, 0xBC, 0xF4, 0xB3, 0xDA, 59])
            data_to_send = bytes([58, 0, 1, 16, 0, 0, 96, 153, 41, 109, 59])
            ## crc hesaplama
            # crc_hex = self.convert_to_modbus_format(dataList)

            # Example MPEG-2 data stream (replace this with your actual data)
            mpeg2_data = b'\x3A\x00\x01\x10\x00\x00\x00\x00'
            custom_polynomial = 0x04C11DB7  # Replace this with your desired polynomial

            crc32_value = self.calculate_custom_crc32(mpeg2_data, custom_polynomial)
            crc32_hex = format(crc32_value, '08X')  # Convert to hex with leading zeros

            self.send_message(data_to_send)
            # self.send_message(crc32_hex)
            # Geri mesajın kabul edilmesini bekleyin
            result = self.receive_message()

            #################################################33
            ## get data
            conData = []
            if self.getAndControlCRC(result):
                sayac = 0
                for i in range(8):
                    # crc hesaplat
                    input_data = f"58 0 1 16 {sayac} 0 0 0"
                    dataSend = self.createCRCandData(input_data,sayac)
                    sayac += 1
                    self.send_message(dataSend)
                    res = self.receive_message()

                    if self.getAndControlCRC(res):
                        print("gelen cevap: "+res)
                        dataName1 = self.hexToDecimal(res.split(" ")[3])
                        dataName2 = self.hexToDecimal(res.split(" ")[4])

                        ## veri alma
                        parameter = int(self.hexToDecimal(res.split(" ")[5]))
                        #
                        ## veri alma
                        dataSayac = 1
                        reciveData = ""
                        for j in range(parameter):
                            reciveData += res.split(" ")[parameter + 1 + dataSayac]
                            dataSayac += 1
                        self.reciveData[f'{dataName1} {dataName2}'] = f'{reciveData}'

                    else:
                        print("\n Veri yanlış geldi!!")

                print(self.reciveData)
                self.connInfo = True
                return True

            else:
                self.connInfo = False
                return False
        except:
            return False

    def connectPort(self):
        conStatus = self.ui.connect.text()
        print(conStatus)

        if conStatus == "Disconnect":
            self.disconnectCart()
            self.connInfo = False
        else:

            self.ui.connInfo.setText("Connecting...")

            ports = list_ports.comports()
            available_ports = [port.device for port in ports]

            baudrate = 115200
            try:
                start_time = time.time()
                for i in available_ports:
                    try:
                        try:
                            succesCom = i
                            try:
                                self.serial_port = serial.Serial(i, baudrate, timeout=0.1,writeTimeout=0.1)
                                # self.com = succesCom
                                print(succesCom)
                            except:
                                pass
                            result = True

                            self.portConnControl(result,succesCom)

                            if self.connInfo == True:
                                self.com = succesCom
                                break
                        except Exception as e:
                            print(e)
                    except Exception as e:
                        print(e)

                total = time.time() - start_time
                print(total)


                if self.connInfo == False:
                    print("falsee")


                    self.ui.connInfo.setText("Connect Info : Failed")
                    self.ui.portUsed.setText(f"Used Port : ")
                    self.ui.connInfo.setStyleSheet(
                        "background-color: crimson;color: white;border: 1px solid black;")

                    print("Belirli port bulunamadı veya uygun geri mesaj alınamadı.")
                else:

                    self.ui.portUsed.setText(f"Used Port : {self.com}")
                    ## 10 01 : csk version , 10 02 : cart name,


                    cartName = self.reciveData['16 2']
                    cskVersion = self.reciveData['16 1']
                    softwareVer = self.reciveData['16 3']

                    cskName = self.cskVersion["1"]

                    cartNumber = cartName[:4]
                    version = " R"+cartName[4:6]


                    ## 03 software version
                    softwareVer1 = f"{softwareVer[1]}.{softwareVer[2:4]}.{softwareVer[4:6]}.{softwareVer[6:8]}"

                    self.productId = ""
                    ## ürün id 05 06 07
                    self.productId += self.hexToDecimal(self.reciveData['16 5'])
                    productId2 = self.reciveData['16 6']
                    productId3 = self.reciveData['16 7']


                    self.productId += self.hexToDecimal(productId2[2:4])
                    self.productId += self.hexToDecimal(productId2[4:6])
                    self.productId += self.hexToDecimal(productId2[6:8])

                    self.productId += self.hexToDecimal(productId3[2:4])
                    self.productId += self.hexToDecimal(productId3[4:6])
                    self.productId += self.hexToDecimal(productId3[6:8])


                    self.ui.productID.setText(f"Product ID : {self.productId}")
                    self.ui.cartName.setText(f"Hardware version: {cartNumber}{version}")
                    self.ui.karsanPartRef.setText(f"KARSAN part reference : {cskName}")
                    self.ui.sfVersion.setText(f"Software version: {softwareVer1}")
                    self.ui.connInfo.setText("Connect info : Success")

                    self.ui.readRecords.setEnabled(True)
                    self.ui.print.setEnabled(True)

                    self.updateLabel()

            except Exception as e:
                print(e)

    def portConnControl(self,result,succesCom):
        if result:
            if self.find_serial_port():

                self.ui.connect.setText("Disconnect")

                self.connInfo = True
            else:
                self.connInfo = False

    def calculate_custom_crc32(self,data, polynomial):
        crc = 0xFFFFFFFF
        for byte in data:
            crc ^= byte << 24
            for _ in range(8):
                crc = (crc << 1) ^ polynomial if crc & 0x80000000 else crc << 1
            crc &= 0xFFFFFFFF
        return crc

    def hexToDecimal(self, newData):

        hex_liste = newData.split()
        decimal_degerler = [int(deger, 16) for deger in hex_liste]
        print(decimal_degerler)
        # Decimal değerleri string olarak birleştirin
        decimal_metin = ' '.join(map(str, decimal_degerler))
        return decimal_metin

    def disconnectCart(self):
        try:
            self.serial_port.close()
            self.ui.readRecords.setEnabled(False)
            self.ui.print.setEnabled(False)

        except:
            pass

        self.ui.connect.setText("Connect")
        self.ui.connInfo.setText("Connect info : ")
        self.ui.productID.setText("Product ID : ")
        self.ui.portUsed.setText(f"Port : ")

        self.ui.cartName.setText(f"Hardware version: ")
        self.ui.karsanPartRef.setText(f"KARSAN part reference :")
        self.ui.sfVersion.setText(f"Software version : ")

        self.ui.connInfo.setStyleSheet("background-color:white; : ")

        self.ui.recordDetail.clear()

    def updateLabel(self):
        self.ui.portUsed.repaint()
        self.ui.productID.repaint()
        self.ui.cartName.repaint()
        self.ui.sfVersion.repaint()
        self.ui.karsanPartRef.repaint()
        self.ui.connInfo.repaint()

    ## data düzenlenecek
    def readRecords(self):
        sayac = 8
        self.ui.recordDetail.clear()

        ## data düzenlenecek
        for i in range(8,38):
            # crc hesaplat
            input_data = f"58 0 1 16 {sayac} 0 0 0"
            print(sayac)
            dataSend = self.createCRCandData(input_data, sayac)
            sayac += 1
            self.send_message(dataSend)
            res = self.receive_message()

            if self.getAndControlCRC(res):
                print("gelen cevap: " + res)
                dataName1 = self.hexToDecimal(res.split(" ")[3])
                dataName2 = self.hexToDecimal(res.split(" ")[4])

                ## veri alma
                parameter = int(self.hexToDecimal(res.split(" ")[5]))
                #
                ## veri alma
                dataSayac = 1
                reciveData = ""
                for j in range(parameter):
                    try:
                        reciveData += self.hexToDecimal(res.split(" ")[parameter + 1 + dataSayac])

                        dataSayac += 1

                    except Exception as e:
                        print(e)

                self.reciveData[f'{dataName1} {dataName2}'] = f'{reciveData}'

            else:
                print("\n Veri yanlış geldi!!")


        say = 8

        for write in range(8,38):
            dataName = self.veri_dict[f'16 {say}']
            data = self.reciveData[f'16 {say}']

            say += 1

            print(say)
            self.ui.recordDetail.append(f"{dataName} : {data}")


        print(self.reciveData)

    def printData(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save PDF File", f"{self.productId}.pdf", "PDF Files (*.pdf);;All Files (*)",
                                                  options=options)
        if fileName:
            # Örnek resim yolu ve rapor numarası
            try:
                location_file = str(os.getcwd())
                self.replace = location_file.replace("\\", "/")

                image_path = f"{self.replace}/System Data/header.png"
                report_num = "2023-001"

                printerDetail.create_pdf_with_data(self.veri_dict,self.reciveData,fileName, image_path, report_num)

                QMessageBox.information(self,"SUCCESS",f" Rapor dosyanız {fileName} dizinine kaydedildi")
            except Exception as e:
                QMessageBox.critical(self,"ERROR",f"Veriler Düzgün yüklenemedi \nError Info : {e}")

# for second result

def run():
    ap = QtWidgets.QApplication(sys.argv)
    win = App()
    win.setFixedSize(990, 800)  # pencere boyutlandırma işlemi kapatıldı
    win.show()
    sys.exit(ap.exec_())

if __name__ == "__main__":
    run()
##