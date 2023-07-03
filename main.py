from guizero import App, Text, PushButton, Slider
from pygame import mixer
import audio_metadata

musica = "song.mp3"

app = App(width="500", height="200")
metadata = audio_metadata.load(musica)


def volume():
    print(volume.value)
    mixer.music.set_volume(volume.value / 100)


def play():
    if mixer.music.get_busy():
        mixer.music.pause()
        return
    mixer.music.unpause()


nome_da_musica = Text(app, "Nome da Musica", align="top")
album = Text(app, "Album", align="top")
compositor = Text(app, "Compositor", align="top")
playbutton = PushButton(app,
                        text="Play/Pause",
                        align="left",
                        command=play)
librarybutton = PushButton(app, text="Abrir biblioteca", align="left")
volume = Slider(app, align="right", command=volume)
mixer.init()
mixer.music.load(musica)
mixer.music.play()
mixer.music.set_volume(volume.value)
volumetext = Text(app, "Volume", align="right")

app.display()
