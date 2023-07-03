from guizero import App, Text, PushButton, Slider

app = App(width="500", height="45")
playbutton = PushButton(app, text="Play/Pause", align="left")
librarybutton = PushButton(app, text="Abrir biblioteca", align="left")
volume = Slider(app, align="right")
volumetext = Text(app, "Volume", align="right")

app.display()