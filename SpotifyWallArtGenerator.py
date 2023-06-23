import os
import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from turtle import back, bgcolor
from PIL import Image, ImageTk, ImageFont, ImageDraw
import sys
import requests
from io import BytesIO
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def searchSongButtonClick():
    
    spotifyResults = callSpotifyAPI()

    spotifyResults[1] = trimTextToThirtyCharacters(spotifyResults[1])
    spotifyResults[2] = trimTextToThirtyCharacters(spotifyResults[2])

    songTitleModifyTextbox.delete(1.0,"end")
    songTitleModifyTextbox.insert(1.0, spotifyResults[1])

    artistModifyTextbox.delete(1.0,"end")
    artistModifyTextbox.insert(1.0, spotifyResults[2])

    colorHexCode = colorHexTextbox.get("1.0", "end-1c")

    albumArtImage = retrieveImageFromUrl(spotifyResults[0])
    songCodeImage = retrieveImageFromUrl("https://scannables.scdn.co/uri/plain/png/" + colorHexCode + "/white/640/spotify:playlist:0qtAGoh3i4qOdw0pKaFjMz")

    final_thumb = Image.new(mode='RGBA',size=[760,1140],color="black")
    final_thumb.paste(albumArtImage, [60,60])
    final_thumb.paste(songCodeImage, [60,700])


    drawInterface = ImageDraw.Draw(final_thumb)
    
    title_size = 90
    artist_size = 70

    title_font = ImageFont.truetype("Gotham-Medium.otf", title_size)
    artist_font = ImageFont.truetype("Gotham-Medium.otf", artist_size)

    w_title, h_title = drawInterface.textsize(spotifyResults[1], title_font)
    w_artist, h_artist = drawInterface.textsize(spotifyResults[2], artist_font)

    start_x_title = (760 - w_title) / 2
    start_x_artist = (760 - w_artist) / 2

    start_y_title = 900
    start_y_artist = 1020

    while(start_x_title < 62):
        title_size = title_size - 1
        title_font = ImageFont.truetype("Gotham-Medium.otf", title_size)
        w_title, h_title = drawInterface.multiline_textsize(spotifyResults[1], title_font)
        start_x_title = (760 - w_title) / 2
        start_y_title = start_y_title + 0.5
    
    while(start_x_artist < 62):
        artist_size = artist_size - 1
        artist_font = ImageFont.truetype("Gotham-Medium.otf", artist_size)
        w_artist, h_artist = drawInterface.textsize(spotifyResults[2], artist_font)
        start_x_artist = (760 - w_artist) / 2
        start_y_artist = start_y_artist + 0.5


    drawInterface.text((start_x_title, start_y_title), spotifyResults[1], font=title_font)
    drawInterface.text((start_x_artist, start_y_artist), spotifyResults[2], font=artist_font, fill=(118,118,118))

    logo = final_thumb
    logo = logo.resize((380,570))
    logo = ImageTk.PhotoImage(logo)
    logo_label.configure(image = logo)
    logo_label.image = logo

def modifyButtonClick():
    spotifyResults = callSpotifyAPI()

    spotifyResults[1] = songTitleModifyTextbox.get("1.0", "end-1c")
    spotifyResults[2] = artistModifyTextbox.get("1.0", "end-1c")
    colorHexCode = colorHexTextbox.get("1.0", "end-1c")

    albumArtImage = retrieveImageFromUrl(spotifyResults[0])
    songCodeImage = retrieveImageFromUrl("https://scannables.scdn.co/uri/plain/png/" + colorHexCode + "/white/640/spotify:playlist:0qtAGoh3i4qOdw0pKaFjMz")

    final_thumb = Image.new(mode='RGBA',size=[760,1140],color="black")
    final_thumb.paste(albumArtImage, [60,60])
    final_thumb.paste(songCodeImage, [60,700])

    drawInterface = ImageDraw.Draw(final_thumb)
    
    title_size = 90
    artist_size = 70

    title_font = ImageFont.truetype("Gotham-Medium.otf", title_size)
    artist_font = ImageFont.truetype("Gotham-Medium.otf", artist_size)

    w_title, h_title = drawInterface.textsize(spotifyResults[1], title_font)
    w_artist, h_artist = drawInterface.textsize(spotifyResults[2], artist_font)

    start_x_title = (760 - w_title) / 2
    start_x_artist = (760 - w_artist) / 2

    start_y_title = 900
    start_y_artist = 1020

    while(start_x_title < 62):
        title_size = title_size - 1
        title_font = ImageFont.truetype("Gotham-Medium.otf", title_size)
        w_title, h_title = drawInterface.textsize(spotifyResults[1], title_font)
        start_x_title = (760 - w_title) / 2
        start_y_title = start_y_title + 0.5
    
    while(start_x_artist < 62):
        artist_size = artist_size - 1
        artist_font = ImageFont.truetype("Gotham-Medium.otf", artist_size)
        w_artist, h_artist = drawInterface.textsize(spotifyResults[2], artist_font)
        start_x_artist = (760 - w_artist) / 2
        start_y_artist = start_y_artist + 0.5


    drawInterface.text((start_x_title, start_y_title), spotifyResults[1], font=title_font)
    drawInterface.text((start_x_artist, start_y_artist), spotifyResults[2], font=artist_font, fill=(118,118,118))

    logo = final_thumb
    logo = logo.resize((380,570))
    logo = ImageTk.PhotoImage(logo)

    logo_label.configure(image = logo)
    logo_label.image = logo

def modifyColor():
    fullColorCode = colorchooser.askcolor(title ="Choose color")
    hexColor = fullColorCode[1]
    hexColor = hexColor[1:]
    colorHexTextbox.delete(1.0,"end")
    colorHexTextbox.insert(1.0, hexColor)
    if (songTitleModifyTextbox.get("1.0", "end-1c") and artistModifyTextbox.get("1.0", "end-1c")):
        modifyButtonClick()
    elif (songSearchTextbox.get("1.0", "end-1c") or artistSearchTextbox.get("1.0", "end-1c")):
        searchSongButtonClick()

def saveImage():
    saveImageThing = ImageTk.getimage(logo_label.image)
    saveFile = filedialog.asksaveasfile(mode='w', initialdir="./", defaultextension=".png")
    if saveFile:
        saveImageThing.save(saveFile.name)
    saveImageThing.close()
    


def callSpotifyAPI():
    songInput = songSearchTextbox.get("1.0", "end-1c")
    artistInput = artistSearchTextbox.get("1.0", "end-1c")
    client_credentials_manager = SpotifyClientCredentials(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')
    spotify = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    songResults = spotify.search(q='track:' + songInput + ' ' + artistInput, type='track')
    albumArtUrl = songResults['tracks']['items'][0]['album']['images'][0]['url']
    songTitle = songResults['tracks']['items'][0]['name']
    songArtist = songResults['tracks']['items'][0]['artists'][0]['name']
    return [albumArtUrl, songTitle, songArtist]

def retrieveImageFromUrl(url):
    imageRequest = requests.get(url)
    return Image.open(BytesIO(imageRequest.content))

def trimTextToThirtyCharacters(text):
    if len(text) > 30:
        text = text[0:30]
    return text



root = tk.Tk()
root.title("Spotify Wall Art Generator")

canvas = tk.Canvas(root, width = 800, height = 600)
canvas.grid(columnspan=2, rowspan=25)
root.columnconfigure(1,weight=1)


labelSongName = tk.Label( root, text="Enter song name:")
labelSongName.grid(column=0, row = 0, sticky=tk.W,pady=0)

songSearchTextbox = tk.Text(root, background="light cyan", height = 1, width = 52, borderwidth=1, relief="solid")
songSearchTextbox.grid(column=0, row = 1, sticky=tk.E, padx=5, pady=0)

labelArtistName = tk.Label( root, text="Enter artist name:")
labelArtistName.grid(column=0, row = 2, sticky=tk.W,pady=0)

artistSearchTextbox = tk.Text(root, background="light cyan", height = 1, width = 52, borderwidth=1, relief="solid")
artistSearchTextbox.grid(column=0, row=3, sticky=tk.E, padx=5)

searchButton = tk.Button(root, height = 2,
                 width = 20,
                 text ="Search",
                 command = lambda:searchSongButtonClick())
searchButton.grid(column = 0, row = 4)

colorHexLabel = tk.Label( root, text="Song code color hexidecimal:")
colorHexLabel.grid(column=0, row = 8, sticky=tk.W,pady=0)

colorHexTextbox = tk.Text(root, background="light cyan", height = 1, width = 52, borderwidth=1, relief="solid")
colorHexTextbox.grid(column=0, row=9, sticky=tk.E, padx=5)
colorHexTextbox.insert(1.0, "6fa8dc")

colorButton = tk.Button(root, height = 2,
                 width = 20,
                 text ="Color Selector",
                 command = lambda:modifyColor())
colorButton.grid(column = 0, row = 10)

songTitleModifyLabel = tk.Label( root, text="Modify song title:")
songTitleModifyLabel.grid(column=0, row = 11, sticky=tk.W,pady=0)

songTitleModifyTextbox = tk.Text(root, background="light cyan", height = 1, width = 52, borderwidth=1, relief="solid")
songTitleModifyTextbox.grid(column=0, row=12, sticky=tk.E, padx=5)

artistModifyLabel = tk.Label( root, text="Modify artist name:")
artistModifyLabel.grid(column=0, row = 13, sticky=tk.W,pady=0)

artistModifyTextbox = tk.Text(root, background="light cyan", height = 1, width = 52, borderwidth=1, relief="solid")
artistModifyTextbox.grid(column=0, row=14, sticky=tk.E, padx=5)

updateButton = tk.Button(root, height = 2,
                 width = 20,
                 text ="Modify",
                 command = lambda:modifyButtonClick())
updateButton.grid(column = 0, row = 17)

saveButton = tk.Button(root, height = 2,
                 width = 20,
                 text ="Save Image",
                 command = lambda:saveImage())
saveButton.grid(column = 0, row = 24)

logo_label = tk.Label()
logo_label.grid(column=1, row = 0, rowspan=40)


root.mainloop()
