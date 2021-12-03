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

wizlightDictionary = {}

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
        self.dialog = None
        self.pushButton = None
        self.loop = loop
        self.counter = 0
        self.reset = False
        self.bDoStuff = False
        self.openMedia = False

    @pyqtSlot(QPushButton)
    def set_index_slot(self, _pushButton):
        self.dialog = _pushButton.parent()
        self.pushButton = _pushButton
        self.reset = True
        self.bDoStuff = True
        self.openMedia = True

    def openMediaPlayer(self, value):
        self.dialog = QDialog(self.dialog)
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
        
    async def do_stuff(self):
        while True:
            sleep = 1
            if self.bDoStuff:
                if self.pushButton != None:
                    if self.openMedia == True:
                        if self.pushButton.property("media") != None:
                            i = json.loads(self.pushButton.property("media"))
                            media_url = i["url"]
                            self.openMediaPlayer(media_url)
                            self.openMedia = False
                    if self.pushButton.property("lighting") != None:
                        tasks_on = []
                        tasks_off = []
                        lighting = json.loads(self.pushButton.property("lighting"))

                        _pulseType = 0
                        _pulseOn = 0
                        _pulseOff = 0
                        if "pulse" in lighting:
                            j = lighting["pulse"]
                            lighting_pulse_type = j["type"]
                            if lighting_pulse_type == "default":
                                lighting_pulse_on = j["on"]
                                lighting_pulse_off = j["off"]
                                _pulseType = 1
                                _pulseOn = lighting_pulse_on
                                _pulseOff = lighting_pulse_off
                        
                        items = lighting["items"]
                        for i in items:
                            _type = 0
                            _turn = 0
                            _colortemp = 0
                            _rgb = (0, 0, 0)
                            _scene = 0
                            _pulse = 0
                            if "turn" in i:
                                lighting_turn = i["turn"]
                                if lighting_turn == "on":
                                    _turn = 1
                            if _turn == 1:
                                if "colortemp" in i:
                                    lighting_colortemp = i["colortemp"]
                                    _type = 1
                                    _colortemp = lighting_colortemp
                                elif "rgb" in i:
                                    j = i["rgb"]
                                    lighting_rgb_r = j["r"]
                                    lighting_rgb_g = j["g"]
                                    lighting_rgb_b = j["b"]
                                    _type = 2
                                    _rgb = (lighting_rgb_r, lighting_rgb_g, lighting_rgb_b)
                                elif "scene" in i:
                                    lighting_scene_id = i["scene"]
                                    _type = 3
                                    _scene = lighting_scene_id
                                if "pulse" in i:
                                    j = i["pulse"]
                                    if j == "on":
                                        _pulse = 1
                            lighting_id = i["id"]
                            wizlight = wizlightDictionary[lighting_id]
                            if _turn == 0:
                                tasks_on.append(asyncio.create_task(wizlight.turn_off()))
                            else:
                                if _type == 1:
                                    tasks_on.append(asyncio.create_task(wizlight.turn_on(PilotBuilder(colortemp = _colortemp))))
                                elif _type == 2:
                                    tasks_on.append(asyncio.create_task(wizlight.turn_on(PilotBuilder(rgb = _rgb))))
                                elif _type == 3:
                                    tasks_on.append(asyncio.create_task(wizlight.turn_on(PilotBuilder(scene = _scene))))
                        await asyncio.gather(
                            *tasks_on
                        )
                        if _pulseType == 1:
                            await asyncio.sleep(_pulseOn)
                            for i in items:
                                _type = 0
                                _turn = 0
                                _colortemp = 0
                                _rgb = (0, 0, 0)
                                _scene = 0
                                _pulse = 0
                                if "turn" in i:
                                    lighting_turn = i["turn"]
                                    if lighting_turn == "on":
                                        _turn = 1
                                if _turn == 1:
                                    if "colortemp" in i:
                                        lighting_colortemp = i["colortemp"]
                                        _type = 1
                                        _colortemp = lighting_colortemp
                                    elif "rgb" in i:
                                        j = i["rgb"]
                                        lighting_rgb_r = j["r"]
                                        lighting_rgb_g = j["g"]
                                        lighting_rgb_b = j["b"]
                                        _type = 2
                                        _rgb = (lighting_rgb_r, lighting_rgb_g, lighting_rgb_b)
                                    elif "scene" in i:
                                        lighting_scene_id = i["scene"]
                                        _type = 3
                                        _scene = lighting_scene_id
                                    if "pulse" in i:
                                        j = i["pulse"]
                                        if j == "on":
                                            _pulse = 1
                                lighting_id = i["id"]
                                wizlight = wizlightDictionary[lighting_id]
                                if _pulse == 1:
                                    tasks_off.append(asyncio.create_task(wizlight.turn_off()))
                            await asyncio.gather(
                                *tasks_off
                            )
                            await asyncio.sleep(_pulseOff)
                        else:
                            await asyncio.sleep(sleep)
                    else:
                        await asyncio.sleep(sleep)
            else:
                await asyncio.sleep(sleep)

    def work(self):
        asyncio.ensure_future(self.do_stuff(), loop=self.loop)       

class Window(QWidget):
    set_index_signal = pyqtSignal(QPushButton)
    
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
                if "items" in j:
                    for k in j["items"]:
                        pushButton_name = k["name"]
                        # Create push button
                        pushButton = QPushButton(pushButton_name)
                        if "media" in k:
                            pushButton.setProperty(media, json.dumps(k["media"]))
                        if "lighting" in k:
                            pushButton.setProperty(lighting, json.dumps(k["lighting"]))
                            items = k["lighting"]["items"]
                            for l in items:
                                lighting_id = l["id"]
                                wizlightDictionary[lighting_id] = wizlight(lighting_id)
                        pushButton.clicked.connect(self.sendtotask)
                        groupBoxLayout.addWidget(pushButton)
                # Add group box layout to group box
                groupBox.setLayout(groupBoxLayout)
                # Add group box to horizontal layout
                horizontalLayout.addWidget(groupBox)
            # Add horizontal layout to vertical layout
            verticalLayout.addLayout(horizontalLayout)
        
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
        self.set_index_signal.emit(self.sender())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    ui = Window()
    ui.show()
    with loop:
        loop.run_forever()
