import os
import requests
from bs4 import BeautifulSoup
from langdetect import detect

def get_soup(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def replace_bad_char(string) -> str:
    bad_char = ['\\','/','?']
    new_string = list(string)
    for i, c in enumerate(new_string):
        if c in bad_char:
            new_string[i] = ' '
    return ''.join(new_string)

#Dicionário com {musica: link}
def scrap_links_musicas(artista) -> dict:
    link = f'https://www.letras.mus.br/{artista}/mais_acessadas.html'
    soup = get_soup(link)
    #Talvez dê pra usar só uma função de find
    song_table = soup.find(class_="songList-table").find_all('li')
    links_dict = {}
    for song in song_table:
        song_title = song.get('data-name')
        song_link = song.get('data-shareurl')
        links_dict [song_title] = song_link
    return (links_dict)

def scrap_letra_musica(link) -> str:
    soup = get_soup(link)
    song_lyric = soup.find(class_="lyric-original").get_text(separator="\n")
    return song_lyric

def create_text_file(folder_name,file_name,file_content):
    folder_path = os.path.join(os.getcwd(), folder_name)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f'{file_name}.txt')
    with open(file_path, "w") as file:
        file.write(file_content)

def download_musicas(artist):
    links_dict = scrap_links_musicas(artist)
    downloaded = 0
    for song_title in links_dict:
        folder_name = f'musicas\\{artist}'
        file_name = replace_bad_char(song_title)
        song_lyric = scrap_letra_musica(links_dict[song_title])
        #só salvar se a música estiver em portugês
        if detect(song_lyric) == 'pt':
            create_text_file(folder_name, file_name, song_lyric)
            downloaded += 1
        else:
            print (f'"{song_title}" não foi salva pois não está em português.')
    print (f'{downloaded} músicas foram salvas')

if __name__ == '__main__':
    artist = input('Artista: ')
    download_musicas(artist)