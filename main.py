from guizero import App, Text, PushButton, Slider
from pygame import mixer
import audio_metadata
import datetime

musica = "song.mp3"

app = App(width="500", height="200", layout="grid")
metadata = audio_metadata.load(musica)


def updatesongslider():
    songslider.value = mixer.music.get_pos() / 1000


def songsliderjump():
    mixer.music.play()
    print(songslider.value)
    mixer.music.set_pos(songslider.value)


def volume():
    mixer.music.set_volume(volume.value / 100)


def play():
    if mixer.music.get_busy():
        mixer.music.pause()
        return
    mixer.music.unpause()


def refresh_metadata():
    metadata = audio_metadata.load(musica)
    nome_da_musica.text = metadata["tags"]["title"][0]
    album.text = metadata["tags"]["album"][0]
    compositor.text = metadata["tags"]["artist"][0]


nome_da_musica = Text(app, metadata["tags"]["title"][0], grid=[1, 1])
album = Text(app, metadata["tags"]["album"][0], grid=[1, 2])
compositor = Text(app, metadata["tags"]["artist"][0], grid=[1, 3])
songstart = Text(app, text="0:00", grid=[0, 4])
songslider = Slider(
    app,
    start=0,
    end=metadata["streaminfo"]["duration"],
    grid=[1, 4],
    command=songsliderjump,
)
songend = Text(
    app,
    text=datetime.timedelta(seconds=int(metadata["streaminfo"]["duration"] / 2)),
    grid=[2, 4],
)
playbutton = PushButton(app, text="Play/Pause", align="left", command=play, grid=[0, 5])
librarybutton = PushButton(app, text="Abrir biblioteca", grid=[1, 5])
volumetext = Text(app, "Volume", grid=[2, 5])
volume = Slider(app, command=volume, grid=[3, 5])
mixer.init()
mixer.music.load(musica)
mixer.music.play()
mixer.music.set_volume(volume.value)

app.repeat(1000, updatesongslider)
app.display()
