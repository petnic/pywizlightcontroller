from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import asyncio
from asyncqt import *
import random
import sys

from pywizlight import wizlight, PilotBuilder

light0 = wizlight("192.168.1.32") # Light 0

class Worker(QObject):
    def __init__(self, loop: asyncio.AbstractEventLoop, parent=None):
        super(Worker, self).__init__(parent)
        self.index = 0
        self.loop = loop
        self.counter = 0
        self.reset = False
        self.bDoStuff = False

    @pyqtSlot(int)
    def set_index_slot(self, _index):
        self.index = _index
        self.reset = True
        self.bDoStuff = True

    async def do_stuff(self):       
        while True:
            sleep = 1
            if self.bDoStuff:
                if self.index == 0 and self.reset == True:
                    await asyncio.gather(
                        light0.turn_off(),
                        loop = loop
                    )
                    self.reset = False
                    await asyncio.sleep(sleep)
                elif self.index == 1 and self.reset == True:
                    _rgb = (255, 0, 0)
                    await asyncio.gather(
                        light0.turn_on(PilotBuilder(rgb = _rgb)),
                        loop = loop
                    )
                    self.reset = False
                    await asyncio.sleep(sleep)
                elif self.index == 2 and self.reset == True:
                    _rgb = (0, 255, 0)
                    await asyncio.gather(
                        light0.turn_on(PilotBuilder(rgb = _rgb)),
                        loop = loop
                    )
                    self.reset = False
                    await asyncio.sleep(sleep)
                elif self.index == 3 and self.reset == True:
                    _rgb = (0, 0, 255)
                    await asyncio.gather(
                        light0.turn_on(PilotBuilder(rgb = _rgb)),
                        loop = loop
                    )
                    self.reset = False
                    await asyncio.sleep(sleep)
                elif self.index == 4 and self.reset == True:
                    _colortemp = 2700
                    await asyncio.gather(
                        light0.turn_on(PilotBuilder(colortemp = _colortemp)),
                        loop = loop
                    )
                    self.reset = False
                    await asyncio.sleep(sleep)
                elif self.index == 5 and self.reset == True:
                    _colortemp = 2700
                    await asyncio.gather(
                        light0.turn_on(PilotBuilder(colortemp = _colortemp)),
                        loop = loop
                    )
                    self.reset = False
                    await asyncio.sleep(sleep)
                elif self.index == 6 and self.reset == True:
                    _rgb = (255, 0, 0)
                    await asyncio.gather(
                        light0.turn_on(PilotBuilder(rgb = _rgb)),
                        loop = loop
                    )
                    self.reset = False
                    await asyncio.sleep(sleep)
                elif self.index == 7 and self.reset == True:
                    _rgb = (255, 0, 0)
                    await asyncio.gather(
                        light0.turn_on(PilotBuilder(rgb = _rgb)),
                        loop = loop
                    )
                    self.reset = False
                    await asyncio.sleep(sleep)
                elif self.index == 8:
                    _rgb = (255, 128, 0)
                    await asyncio.gather(
                        light0.turn_on(PilotBuilder(rgb = _rgb)),
                        loop = loop
                    )
                    print("On")
                    await asyncio.sleep(sleep)
                    await asyncio.gather(
                        light0.turn_off(),
                        loop = loop
                        )
                    print("Off")
                    await asyncio.sleep(sleep)
                elif self.index == 9 and self.reset == True:
                    _scene = 5 # Fireplace
                    await asyncio.gather(
                        light0.turn_on(PilotBuilder(scene = _scene)),
                        loop = loop
                    )
                    self.reset = False
                    await asyncio.sleep(sleep)
                elif self.index == 10 and self.reset == True:
                    _rgb = (255, 0, 255)
                    await asyncio.gather(
                        light0.turn_on(PilotBuilder(rgb = _rgb)),
                        loop = loop
                    )
                    self.reset = False
                    await asyncio.sleep(sleep)
                elif self.index == 11:
                    _colortemp = 6000
                    await asyncio.gather(
                        light0.turn_on(PilotBuilder(colortemp = _colortemp)),
                        loop = loop
                    )
                    print("On")
                    await asyncio.sleep(random.uniform(0.5, 1.0))
                    await asyncio.gather(
                        light0.turn_off(),
                        loop = loop
                        )
                    print("Off")
                    await asyncio.sleep(random.uniform(0.5, 1.0))
                    await asyncio.gather(
                        light0.turn_on(PilotBuilder(colortemp = _colortemp)),
                        loop = loop
                    )
                    print("On")
                    await asyncio.sleep(random.uniform(0.5, 2.0))
                    await asyncio.gather(
                        light0.turn_off(),
                        loop = loop
                        )
                    print("Off")
                    await asyncio.sleep(random.uniform(8.0, 16.0))
                else:
                    await asyncio.sleep(sleep)
            else:
                await asyncio.sleep(sleep)

    def work(self):
        asyncio.ensure_future(self.do_stuff(), loop=self.loop)

class Window(QWidget):
    set_index_signal = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super(Window, self).__init__()
        self.initUi()
        self.start_task()

    def addPushButton(self, layout, pushButtonName):
        pushButton = QPushButton(pushButtonName)
        pushButton.setProperty(self.name, self.value)
        pushButton.clicked.connect(self.sendtotask)
        layout.addWidget(pushButton)
        self.value += 1        
        
    def addPushButtons(self, layout, pushButtonNames):
        for pushButtonName in pushButtonNames:
            self.addPushButton(layout, pushButtonName)
        
    def initUi(self):
        self.name = "index"
        self.value = 0
        
        layout = QVBoxLayout()

        pushButtonNames0 = ["Off"]
        self.addPushButtons(layout, pushButtonNames0)
        
        groupBox1 = QGroupBox("General")
        layout1 = QVBoxLayout()
        pushButtonNames1 = ["Red", "Green", "Blue", "Warm White"]
        self.addPushButtons(layout1, pushButtonNames1)
        groupBox1.setLayout(layout1)
        layout.addWidget(groupBox1)

        groupBox2 = QGroupBox("Alien: Fate of the Nostromo")
        layout2 = QVBoxLayout()
        pushButtonNames2 = ["Default", "Alien", "Ash", "Emergency Destruction System", "Self-Destruct"]
        self.addPushButtons(layout2, pushButtonNames2)
        groupBox2.setLayout(layout2)
        layout.addWidget(groupBox2)
        
        groupBox3 = QGroupBox("Betrayal at House on the Hill")
        layout3 = QVBoxLayout()
        pushButtonNames3 = ["Default", "Haunt"]
        self.addPushButtons(layout3, pushButtonNames3)        
        groupBox3.setLayout(layout3)
        layout.addWidget(groupBox3)
        
        layout.addStretch(1)
        
        self.setLayout(layout)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint)
        self.setWindowTitle("Window")
        self.resize(1920, 1080)

    def start_task(self):
        loop = asyncio.get_event_loop()
        self.worker = Worker(loop)
        self.set_index_signal.connect(self.worker.set_index_slot)
        self.worker.work()

    def sendtotask(self):
        self.set_index_signal.emit(self.sender().property(self.name))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    ui = Window()
    ui.show()
    with loop:
        loop.run_forever()
