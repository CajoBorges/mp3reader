import tkinter
from guizero import App, Text, PushButton, Slider, MenuBar, Window, ListBox
from pygame import mixer
import audio_metadata
import datetime
import os

musica = "song.mp3"
caminhosdemusicas = []
app = App(title="mp3reader - FREE VERSION UPGRADE TO PREMIUM FOR 399€", width="380", height="160", layout="grid")
metadata = audio_metadata.load(musica)
songsliderbefore = 0
playingt = 0
update = True

def updatesongslider():
    global songsliderbefore, playingt, update
    if update and mixer.music.get_busy():
        songsliderbefore = songslider.value
        playingt += 1
        songslider.value = playingt
    update = True


def songsliderjump(): # ora bolas
    global songsliderbefore, playingt
    if songslider.value != (songsliderbefore + 1):
        timetoset = songslider.value-mixer.music.get_pos()
        print(timetoset)
        mixer.music.play(timetoset)
        update = False


def volume():
    mixer.music.set_volume(volume.value / 100)

def importarmusicas():
    global listademusicas, caminhosdemusicas
    tkinter.Tk().withdraw()
    diretorioselecionado = tkinter.filedialog.askdirectory()
    ficheiros = os.listdir(diretorioselecionado)
    ficheirosmp3 = []
    i = ''
    for ficheiro in ficheiros:
        if ficheiro.endswith(".mp3"):
            ficheirosmp3.append(diretorioselecionado + '/' + ficheiro)
    for i in ficheirosmp3:
        metadata = audio_metadata.load(i)
        try:
            listademusicas.append(metadata["tags"]["title"][0])
        except KeyError:
            listademusicas.append(i.strip(diretorioselecionado))
        caminhosdemusicas.append(i)

def selecionarmusicas():
    global listademusicas, caminhosdemusicas, musica, songsliderbefore, songslider, playingt, songend, metadata
    l = 0
    for i in listademusicas.items:
        if i == listademusicas.value:
            musica = caminhosdemusicas[l]
            break
        l += 1
    mixer.music.stop()
    mixer.music.unload()
    mixer.music.load(musica)
    playingt = 0
    metadata = audio_metadata.load(musica)
    refresh_metadata()
    songslider.value = 0
    songsliderbefore = 0
    songslider.end = metadata["streaminfo"]["duration"]
    songend.value = datetime.timedelta(seconds=int(metadata["streaminfo"]["duration"]))
    mixer.music.play()


def play():
    if mixer.music.get_busy():
        mixer.music.pause()
        return
    mixer.music.unpause()

def abrir_biblioteca():
    selmusica.visible = True

def refresh_metadata():
    metadata = audio_metadata.load(musica)
    try:
        nome_da_musica.value = metadata["tags"]["title"][0]
        album.value = metadata["tags"]["album"][0]
        compositor.value = metadata["tags"]["artist"][0]
    except KeyError:
        nome_da_musica.value = musica.split("/")[-1].rstrip(".mp3")
        album.value = musica.split("/")[-2]
        compositor.value = "indefinido"

menubar = MenuBar(app,
                  toplevel=["Opções"],
                  options=[
                      [["Biblioteca de músicas", abrir_biblioteca], ["Recarregar metadados", refresh_metadata]]
                  ])

nome_da_musica = Text(app, metadata["tags"]["title"][0], grid=[1, 1])
album = Text(app, metadata["tags"]["album"][0], grid=[1, 2])
compositor = Text(app, metadata["tags"]["artist"][0], grid=[1, 3])
songstart = Text(app, text="0:00", grid=[0, 4])
selmusica = Window(app, title="Selecionar música", width=500, height=250, visible=False)
listademusicas = ListBox(selmusica, width=500, height=210)
bimportarmusicas = PushButton(selmusica, text="Importar músicas", align="left", command=importarmusicas)
bselecionar = PushButton(selmusica, text="Selecionar", align="right", command=selecionarmusicas)
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
librarybutton = PushButton(app, text="Abrir biblioteca", grid=[1, 5], command=abrir_biblioteca)
volumetext = Text(app, "Volume", grid=[2, 5])
volume = Slider(app, command=volume, grid=[3, 5])
mixer.init()
mixer.music.load(musica)
mixer.music.play()
mixer.music.set_volume(volume.value)

app.repeat(1000, updatesongslider)
app.display()
