from PyQt5 import QtCore
from PyQt5 import QtWidgets
import asyncio



# İş parçacığı sınıfını oluşturun
class WorkerThread(QtCore.QThread):
    def __init__(self,app_instance, task_name):
        super().__init__()
        # Görev tamamlandığında bir sinyal göndermek için

        self.app_instance = app_instance
        self.task_name = task_name

    def run(self):
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        if self.task_name == 'Connect':
            self.app_instance.operationName = "Connecting"
            # loop.run_until_complete(self.parent().startLoadingScreen()) # Loading işlemini başlat
            # loop.run_until_complete(self.parent().connectPort())
            asyncio.run(self.app_instance.start_loading_screen("Connecting"))
            asyncio.run(self.app_instance.connectPort())

        elif self.task_name == 'Disconnect':
            asyncio.run(self.app_instance.disconnectCart())
            print("bitti artık")


        elif self.task_name == 'read':
            self.app_instance.operationName = "Reading Records"
            asyncio.run(self.app_instance.start_loading_screen("Reading"))
            asyncio.run(self.app_instance.readRecords())

