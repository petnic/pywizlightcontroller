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

class MediaPlayerController(QGroupBox):
    def __init__(self, title, parent=None):
        super(MediaPlayerController, self).__init__(parent)

        self.vBoxLayout = QVBoxLayout()

        self.titleLabel = QLabel(title, self)
        self.vBoxLayout.addWidget(self.titleLabel)

        self.progressBarSlider = QSlider(1, self) ## Qt::Horizontal
        self.progressBarSlider.setRange(0, 1)
        self.vBoxLayout.addWidget(self.progressBarSlider)

        self.hBoxLayout = QHBoxLayout()

        self.playPushButton = QPushButton("Play", self)
        self.hBoxLayout.addWidget(self.playPushButton)

        self.mutePushButton = QPushButton("Mute", self)
        self.hBoxLayout.addWidget(self.mutePushButton)

        self.volumeSlider = QSlider(1, self) ## Qt::Horizontal
        self.volumeSlider.setTickInterval(10)
        self.volumeSlider.setTickPosition(3) ## QSlider::TicksBothSides
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setToolTip(str(0))
        self.volumeSlider.setValue(0)
        self.hBoxLayout.addWidget(self.volumeSlider)

        self.vBoxLayout.addLayout(self.hBoxLayout)

        self.setLayout(self.vBoxLayout)

class AudioMediaPlayerController(MediaPlayerController):
    def __init__(self, title, parent=None):
        super(AudioMediaPlayerController, self).__init__(title, parent)

        self.setTitle("Audio")

class VideoMediaPlayerController(MediaPlayerController):
    def __init__(self, title, parent=None):
        super(VideoMediaPlayerController, self).__init__(title, parent)
        
        self.setTitle("Video")

        self.fullscreenPushButton = QPushButton("Fullscreen", self)
        self.hBoxLayout.addWidget(self.fullscreenPushButton)

        
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
    def __init__(self, loop: asyncio.AbstractEventLoop, _audioMediaPlayerController, _videoMediaPlayerController, parent=None):
        super(Worker, self).__init__(parent)
        self.dialog = None
        self.pushButton = None
        self.loop = loop
        self.counter = 0
        self.reset = False
        self.bDoStuff = False
        self.openMedia = False
        self.mediaPlayerDialog = None
        self.mediaPlayer = None
        self.videoWidget = None
        self.mediaPlayerOpen = False
        self.playbackMousePress = False
        self.audioMediaPlayerController = _audioMediaPlayerController
        self.videoMediaPlayerController = _videoMediaPlayerController

    @pyqtSlot(QPushButton)
    def set_index_slot(self, _pushButton):
        self.dialog = _pushButton.parent()
        self.pushButton = _pushButton
        self.reset = True
        self.bDoStuff = True
        self.openMedia = True

    def progressBarSliderPressed(self):
        self.playbackMousePress = True

    def progressBarSliderReleased(self):
        self.playbackMousePress = False
        self.mediaPlayer.setPosition(self.videoMediaPlayerController.progressBarSlider.value())

    def playPushButtonClicked(self):
        if self.mediaPlayer != None:
            if self.mediaPlayer.state() == 1:
                self.videoMediaPlayerController.playPushButton.setText("Play")
                self.mediaPlayer.pause()
            else:
                self.videoMediaPlayerController.playPushButton.setText("Pause")
                self.mediaPlayer.play()

    def mutePushButtonClicked(self):
        if self.mediaPlayer != None:
            if self.mediaPlayer.isMuted():
                self.videoMediaPlayerController.mutePushButton.setText("Mute")
                self.mediaPlayer.setMuted(False)
            else:
                self.videoMediaPlayerController.mutePushButton.setText("Unmute")
                self.mediaPlayer.setMuted(True)

    def volumeSliderValueChanged(self):
        self.mediaPlayer.setVolume(volume)
        self.videoMediaPlayerController.volumeSlider.setToolTip(str(volume))

    def fullscreenPushButtonClicked(self):
        self.videoWidget.setFullScreen(True)
        
    def playbackMediaPlayer(self, position):
        if self.videoMediaPlayerController.progressBarSlider != None:
            if self.playbackMousePress == False:
                self.videoMediaPlayerController.progressBarSlider.setRange(0, self.mediaPlayer.duration())
                self.videoMediaPlayerController.progressBarSlider.setValue(position)
            
    def closeMediaPlayer(self): 
        if self.mediaPlayer != None:
            self.mediaPlayer.stop()
        self.mediaPlayerOpen = False
            
    def openMediaPlayer(self, name, value, fullScreen, mute, volume):
        if self.mediaPlayerDialog == None:
            self.mediaPlayerDialog = QDialog(self.dialog)
            self.mediaPlayerDialog.resize(1920, 1080)
            self.mediaPlayerDialog.setWindowTitle(name)

        if self.mediaPlayer == None:
            self.mediaPlayer = QMediaPlayer(self.dialog)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(value)))
        if mute == True:
            self.mediaPlayer.setMuted(True)
        else:
            self.mediaPlayer.setMuted(False)
        self.mediaPlayer.setVolume(volume)
        if self.videoWidget == None:
            self.videoWidget = Video_Widget_Class(self.mediaPlayerDialog)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
##        if fullScreen is True:
##            self.fullScreenMediaPlayer()
        self.videoWidget.show()
        self.mediaPlayer.play()

        if self.mediaPlayerOpen == False:
            if self.videoMediaPlayerController.titleLabel != None:
                self.videoMediaPlayerController.titleLabel.setText(value)
            
            if self.videoMediaPlayerController.progressBarSlider != None:
                self.videoMediaPlayerController.progressBarSlider.setRange(0, self.mediaPlayer.duration())
                self.videoMediaPlayerController.progressBarSlider.sliderPressed.connect(self.progressBarSliderPressed)
                self.videoMediaPlayerController.progressBarSlider.sliderReleased.connect(self.progressBarSliderReleased)
                self.mediaPlayer.positionChanged.connect(self.playbackMediaPlayer)

            if self.videoMediaPlayerController.playPushButton != None:
                self.videoMediaPlayerController.playPushButton.setText("Pause")
                self.videoMediaPlayerController.playPushButton.clicked.connect(self.playPushButtonClicked)

            if self.videoMediaPlayerController.mutePushButton != None:
                if (mute):
                    self.videoMediaPlayerController.mutePushButton.setText("Unmute")
                else:
                    self.videoMediaPlayerController.mutePushButton.setText("Mute")
                self.videoMediaPlayerController.mutePushButton.clicked.connect(self.mutePushButtonClicked)

            if self.videoMediaPlayerController.volumeSlider != None:
                self.videoMediaPlayerController.volumeSlider.setValue(volume)
                self.videoMediaPlayerController.volumeSlider.valueChanged.connect(self.volumeSliderValueChanged)
                
            if self.videoMediaPlayerController.fullscreenPushButton != None:
                self.videoMediaPlayerController.fullscreenPushButton.clicked.connect(self.fullscreenPushButtonClicked)

            mediaPlayerDialogLayout = QVBoxLayout()
            mediaPlayerDialogLayout.addWidget(self.videoWidget)
            self.mediaPlayerDialog.setLayout(mediaPlayerDialogLayout)
            self.mediaPlayerDialog.show()
            self.mediaPlayerDialog.finished.connect(self.closeMediaPlayer)

        if self.videoMediaPlayerController.titleLabel != None:
                self.videoMediaPlayerController.titleLabel.setText(value)
                
        if self.videoMediaPlayerController.progressBarSlider != None:
            self.videoMediaPlayerController.progressBarSlider.setRange(0, self.mediaPlayer.duration())
            
        if self.videoMediaPlayerController.volumeSlider != None:
            self.videoMediaPlayerController.volumeSlider.setValue(volume)
            self.videoMediaPlayerController.volumeSlider.setToolTip(str(volume))
                
        self.mediaPlayerOpen = True
        
    async def do_stuff(self):
        while True:
            sleep = 1
            if self.bDoStuff:
                if self.pushButton != None:
                    if self.openMedia == True:
                        if self.pushButton.property("media") != None:
                            i = json.loads(self.pushButton.property("media"))
                            media_name = "Media"
                            media_url = i["url"]
                            media_fullScreen = False
                            fullScreen = i["fullScreen"]
                            if fullScreen == "on":
                                media_fullScreen = True
                            media_mute = False
                            mute = i["mute"]
                            if mute == "on":
                                media_mute = True
                            media_volume = i["volume"]
                            self.openMediaPlayer(media_name, media_url, media_fullScreen, media_mute, media_volume)
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
                            lighting_ids = i["ids"]
                            for j in lighting_ids:
                                lighting_id = j
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
                                lighting_ids = i["ids"]
                                for j in lighting_ids:
                                    lighting_id = j
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
                groupBox = QGroupBox(groupBox_name, self)
                groupBoxLayout = QVBoxLayout()
                if "items" in j:
                    for k in j["items"]:
                        pushButton_name = k["name"]
                        # Create push button
                        pushButton = QPushButton(pushButton_name, self)
                        if "media" in k:
                            pushButton.setProperty(media, json.dumps(k["media"]))
                        if "lighting" in k:
                            pushButton.setProperty(lighting, json.dumps(k["lighting"]))
                            items = k["lighting"]["items"]
                            for l in items:
                                lighting_ids = l["ids"]
                                for m in lighting_ids:
                                    lighting_id = m
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

        self.audioMediaPlayerController = AudioMediaPlayerController("", self)
        verticalLayout.addWidget(self.audioMediaPlayerController)

        self.videoMediaPlayerController = VideoMediaPlayerController("", self)
        verticalLayout.addWidget(self.videoMediaPlayerController)
        
        self.setLayout(verticalLayout)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint)
        self.setWindowTitle("pywizlightcontroller")
        self.resize(1920, 1080)

    def start_task(self):
        loop = asyncio.get_event_loop()
        self.worker = Worker(loop, self.audioMediaPlayerController, self.videoMediaPlayerController)
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
