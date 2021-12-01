from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import *

import asyncio
from asyncqt import *
import json
import random
import sys

from pywizlight import wizlight, PilotBuilder

light0 = wizlight("192.168.1.32") # Light 0

media = "media"
lighting = "lighting"

class Video_Widget_Class(QVideoWidget):
    def Video_Widget(self):
        self.Video_Player = QtMultimediaWidgets.QVideoWidget(self.centralWidget)
        self.Video_Player.setObjectName("videoPlayer")
        self.Video_Player.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.isFullScreen():
            self.setFullScreen(False)
            event.accept()
        elif event.key() == Qt.Key_Enter and event.modifiers() & Qt.Key_Alt:
            self.setFullScreen(not self.isFullScreen())
            event.accept()

    def mouseDoubleClickEvent(self, event):
        self.setFullScreen(not self.isFullScreen())
        event.accept()
            
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
                elif self.index == 6 and self.reset == True:
                    _colortemp = 2700
                    await asyncio.gather(
                        light0.turn_on(PilotBuilder(colortemp = _colortemp)),
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
                elif self.index == 8 and self.reset == True:
                    _rgb = (255, 0, 0)
                    await asyncio.gather(
                        light0.turn_on(PilotBuilder(rgb = _rgb)),
                        loop = loop
                    )
                    self.reset = False
                    await asyncio.sleep(sleep)
                elif self.index == 9:
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
                elif self.index == 11 and self.reset == True:
                    _scene = 5 # Fireplace
                    await asyncio.gather(
                        light0.turn_on(PilotBuilder(scene = _scene)),
                        loop = loop
                    )
                    self.reset = False
                    await asyncio.sleep(sleep)
                elif self.index == 12 and self.reset == True:
                    _rgb = (255, 0, 255)
                    await asyncio.gather(
                        light0.turn_on(PilotBuilder(rgb = _rgb)),
                        loop = loop
                    )
                    self.reset = False
                    await asyncio.sleep(sleep)
                elif self.index == 13:
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
## This should be replaced by the url property in the media object of an item
##        self.name = "index"
##        self.value = 0

        # json start
        f = open("pywizlightcontroller.json", "r")
        x = f.read()
        f.close()
        y = json.loads(x)

        verticalLayout = QVBoxLayout()
        for i in y["rows"]:
            # Create horizontal layout
            horizontalLayout = QHBoxLayout()
            for j in i["columns"]:
                groupBox_name = j["name"]
                # Create group box
                groupBox = QGroupBox(groupBox_name)
                groupBoxLayout = QVBoxLayout()
                for k in j["items"]:
                    pushButton_name = k["name"]
                    # Create push button
                    pushButton = QPushButton(pushButton_name)
                    if "media" in k:
## Move to dostuff for interpretation of media                        
##                        l = k["media"]
##                        media_url = l["url"]
                        pushButton.setProperty(media, json.dumps(k["media"]))
                    if "lighting" in k:
                        pushButton.setProperty(lighting, json.dumps(k["lighting"]))
## Move to dostuff for interpretation of lighting
##                        for l in k["lighting"]:                           
##                            if "colortemp" in l:
##                                lighting_colortemp = l["colortemp"]
##                            elif "rgb" in l:
##                                m = l["rgb"]
##                                lighting_rgb_r = m["r"]
##                                lighting_rgb_g = m["g"]
##                                lighting_rgb_b = m["b"]
##                            elif "scene" in l:
##                                m = l["scene"]
##                                lighting_scene_id = m["id"]
##                            lighting_id = l["id"]
##                            if "pulse" in l:
##                                m = l["pulse"]
##                                lighting_pulse_type = m["type"]
##                                if lighting_pulse_type is "default":
##                                    lighting_pulse_on = m["on"]
##                                    lighting_pulse_off = m["off"]
                    pushButton.clicked.connect(self.sendtotask)
                    groupBoxLayout.addWidget(pushButton)
                # Add group box layout to group box
                groupBox.setLayout(groupBoxLayout)
                # Add group box to horizontal layout
                horizontalLayout.addWidget(groupBox)
            # Add horizontal layout to vertical layout
            verticalLayout.addLayout(horizontalLayout)
        # json end

## The following code will be replaced by json        
##        pushButtonNames0 = ["Off"]
##        self.addPushButtons(verticalLayout, pushButtonNames0)
##
##        # General
##        layout1 = QHBoxLayout()
##        
##        groupBox1Lighting = QGroupBox("General - Lighting")
##        layout1Lighting = QVBoxLayout()
##        pushButtonNames1Lighting = ["Red", "Green", "Blue", "Warm White"]
##        self.addPushButtons(layout1Lighting, pushButtonNames1Lighting)
##        groupBox1Lighting.setLayout(layout1Lighting)
##        layout1.addWidget(groupBox1Lighting)
##
##        #groupBox1Media = QGroupBox("General - Media")
##        #layout1Media = QVBoxLayout()
##        #pushButtonNames1Media = ["Video"]
##        #self.addPushButtons(layout1Media, pushButtonNames1Media)
##        #groupBox1Media.setLayout(layout1Media)
##        #layout1.addWidget(groupBox1Media)
##        
##        pushButton = QPushButton("Video")
##        pushButton.setProperty(self.name, "C:\Git\pywizlightcontroller\media\ASMR - Alien - Isolation - Nap Time near a Computer Console - Ambient Sounds - NO Aliens Aboard!.mp4")
##        pushButton.clicked.connect(self.openMediaPlayer)
##        layout1.addWidget(pushButton)
##        self.value += 1   
##        
##        verticalLayout.addLayout(layout1)
##
##        # Alien: Fate of the Nostromo
##        layout2 = QHBoxLayout()
##        
##        groupBox2Lighting = QGroupBox("Alien: Fate of the Nostromo")
##        layout2Lighting = QVBoxLayout()
##        pushButtonNames2Lighting = ["Default", "Alien", "Ash", "Emergency Destruction System", "Self-Destruct"]
##        self.addPushButtons(layout2Lighting, pushButtonNames2Lighting)
##        groupBox2Lighting.setLayout(layout2Lighting)
##        layout2.addWidget(groupBox2Lighting)
##
##        groupBox2Media = QGroupBox("Alien: Fate of the Nostromo - Media")
##        layout2Media = QVBoxLayout()
##        pushButtonNames2Media = ["Video"]
##        self.addPushButtons(layout2Media, pushButtonNames2Media)
##        groupBox2Media.setLayout(layout2Media)
##        layout2.addWidget(groupBox2Media)
##
##        verticalLayout.addLayout(layout2)
##
##        # Betrayal at House on the Hill
##        layout3 = QHBoxLayout()
##        
##        groupBox3Lighting = QGroupBox("Betrayal at House on the Hill")
##        layout3Lighting = QVBoxLayout()
##        pushButtonNames3Lighting = ["Default", "Haunt"]
##        self.addPushButtons(layout3Lighting, pushButtonNames3Lighting)        
##        groupBox3Lighting.setLayout(layout3Lighting)
##        layout3.addWidget(groupBox3Lighting)
##
##        groupBox3Media = QGroupBox("Betrayal at House on the Hill - Media")
##        layout3Media = QVBoxLayout()
##        pushButtonNames3Media = ["Video"]
##        self.addPushButtons(layout3Media, pushButtonNames3Media)
##        groupBox3Media.setLayout(layout3Media)
##        layout3.addWidget(groupBox3Media)
##
##        verticalLayout.addLayout(layout3)
        
        verticalLayout.addStretch(1)
        
        self.setLayout(verticalLayout)
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

## This should be moved to dostuff (remember: media and lighting should be able to run in parallel)
    def openMediaPlayer(self):
        value = self.sender().property(self.name)

        self.dialog = QDialog(self)
        self.dialog.resize(1920, 1080)
        
        self.player = QMediaPlayer(self.dialog)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(value)))
        self.videoWidget = Video_Widget_Class(self.dialog)
        self.player.setVideoOutput(self.videoWidget)
        self.videoWidget.show()
        self.player.play()

        self.fullScreenPushButton = QPushButton("FullScreen")
        self.fullScreenPushButton.clicked.connect(self.fullScreenMediaPlayer)

        dialogLayout = QVBoxLayout()
        dialogLayout.addWidget(self.videoWidget)
        dialogLayout.addWidget(self.fullScreenPushButton)
        self.dialog.setLayout(dialogLayout)
        self.dialog.show()
        self.dialog.finished.connect(self.closeMediaPlayer)

    def closeMediaPlayer(self):
        self.player.stop()

    def fullScreenMediaPlayer(self):
        self.videoWidget.setFullScreen(True)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    ui = Window()
    ui.show()
    with loop:
        loop.run_forever()
