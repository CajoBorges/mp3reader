from guizero import App, Text, PushButton, Slider
from pygame import mixer

app = App(width="500", height="45")


def volume():
    print(volume.value)
    mixer.music.set_volume(volume.value / 100)


def play():
    if mixer.music.get_busy():
        mixer.music.pause()
        return
    mixer.music.unpause()


playbutton = PushButton(app,
                        text="Play/Pause",
                        align="left",
                        command=play)
librarybutton = PushButton(app, text="Abrir biblioteca", align="left")
volume = Slider(app, align="right", command=volume)
mixer.init()
mixer.music.load("song.mp3")
mixer.music.play()
mixer.music.set_volume(volume.value)
volumetext = Text(app, "Volume", align="right")

app.display()
