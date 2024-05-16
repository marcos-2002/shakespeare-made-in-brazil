import os
import requests
from bs4 import BeautifulSoup
from langdetect import detect
from sklearn.model_selection import train_test_split
import json

def get_soup(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def replace_bad_char(string) -> str:
    bad_char = ['\\','/','?','"']
    new_string = list(string)
    for i, c in enumerate(new_string):
        if c in bad_char:
            new_string[i] = ' '
    return ''.join(new_string)

#Dicionário com {musica: link}
def scrap_links_musicas(artista) -> dict:
    link = f'https://www.letras.mus.br/{artista}/mais_acessadas.html'
    soup = get_soup(link)
    song_table = soup.find(class_="songList-table").find_all('li')
    links_dict = {}
    for song in song_table:
        song_title = song.get('data-name')
        song_link = song.get('data-shareurl')
        links_dict [song_title] = song_link
    return (links_dict)

def scrap_letra_musica(link,paragraph_bool) -> str:
    soup = get_soup(link)
    if paragraph_bool == True:#espaço entre parágrafos
        song_paragraphs = soup.find(class_="lyric-original").find_all('p')
        paragraphs = []
        for paragraph in song_paragraphs:
            paragraphs.append(paragraph.get_text(separator="\n"))
        song_lyric = '\n\n'.join(paragraphs)
        return song_lyric
    else:
        song_lyric = soup.find(class_="lyric-original").get_text(separator="\n")
        return song_lyric[2:-2]#índice para ignorar o primeiro e ultimo espaço em branco ' \n'

def download_musicas(artist, paragraph_bool):
    links_dict = scrap_links_musicas(artist)
    downloaded = 0
    folder_path = f'{os.getcwd()}\\musicas\\{artist}'
    #cria pasta caso ainda não exista
    os.makedirs(folder_path, exist_ok=True)
    for song_title in links_dict:
        file_name = replace_bad_char(song_title)
        file_path = f'{folder_path}\\{file_name}.json'
        if os.path.exists(file_path):
            print (f'"{file_name}" não salva. Arquivo já existe')
            continue
        song_lyric = scrap_letra_musica(links_dict[song_title], paragraph_bool)
        if not (song_lyric):
            print (f'"{file_name}" não salva. Música sem letra.')
            continue
        if detect(song_lyric) != 'pt':
            print (f'"{file_name}" não salva. Música não está em português.')
            continue
        with open(file_path, "w", encoding="utf-8") as file:
            print (f'Salvando "{file_name}"')
            file.write(song_lyric)
        downloaded += 1
    print (f'{downloaded} músicas salvas.')

def download_musicas_concat(artist, paragraph_bool):
    links_dict = scrap_links_musicas(artist)
    downloaded = 0
    folder_path = f'{os.getcwd()}\\musicas'
    os.makedirs(folder_path, exist_ok=True)
    file_path = f'{folder_path}\\{artist}.txt'
    if os.path.exists(file_path):
        print (f'"{artist}.txt" não salvo. Arquivo já existe')
        return
    for song_title in links_dict:
        file_name = replace_bad_char(song_title)
        song_lyric = scrap_letra_musica(links_dict[song_title], paragraph_bool)
        if not (song_lyric):
            print (f'"{file_name}" não salva. Música sem letra.')
            continue
        if detect(song_lyric) != 'pt':
            print (f'"{file_name}" não salva. Música não está em português.')
            continue
        with open(file_path, 'a', encoding='utf-8') as file:
            print (f'Salvando "{file_name}"')
            file.write(f'{song_lyric}\n')
            if paragraph_bool == True:
                file.write(f'\n')
        downloaded += 1
    print (f'{downloaded} músicas salvas.')

def download_musicas_concat_json(artist, paragraph_bool):
    links_dict = scrap_links_musicas(artist)
    downloaded = 0
    folder_path = f'{os.getcwd()}\\musicas'
    os.makedirs(folder_path, exist_ok=True)
    file_path_train = f'{folder_path}\\{artist}-train.json'
    file_path_test = f'{folder_path}\\{artist}-test.json'
    if os.path.exists(file_path_train):
        print (f'"{artist}.txt" não salvo. Arquivo já existe')
        return
    list_data = []
    cont = 0
    for song_title in links_dict:
        file_name = replace_bad_char(song_title)
        song_lyric = scrap_letra_musica(links_dict[song_title], paragraph_bool)
        if not (song_lyric):
            print (f'"{file_name}" não salva. Música sem letra.')
            continue
        if detect(song_lyric) != 'pt':
            print (f'"{artist} - {file_name}" não salva. Música não está em português.')
            continue
        list_data.append({"Poema": song_title, "Letra": song_lyric})
        downloaded += 1
        print (f'{artist} - Salvando "{file_name}"')
    list_data_train, list_data_test = train_test_split(list_data, test_size=0.2) #separa os dados de treino e teste
    
    json_data_train = json.dumps(list_data_train)
    json_data_test = json.dumps(list_data_test)
    with open(file_path_train, 'a', encoding='utf-8') as file:
        file.write(f'{json_data_train}\n')
        if paragraph_bool == True:
            file.write(f'\n')
    with open(file_path_test, 'a', encoding='utf-8') as file:
        file.write(f'{json_data_test}\n')
        if paragraph_bool == True:
            file.write(f'\n')     
    print (f'{artist} - {downloaded} músicas salvas.')

if __name__ == '__main__':
    # artist = input('Artista: ')
    artists = ['5-seco', 'alceu-valenca', 'ana-frango-eletrico', 'anavitoria', 'belchior', 'caetano-veloso', 'cartola', 'cassia-eller', 'cassiano', 'cazuza', 'chico-buarque', 'cicero', 'djavan', 'elis-regina', 'elza-soares', 'gal-costa', 'geraldo-vandre', 'gilberto-gil', 'gilsons', 'gonzaguinha', 'joao-gilberto', 'jorge-ben-jor', 'kid-abelha', 'maria-bethania', 'marisa-monte', 'milton-nascimento', 'nando-reis', 'novos-baianos', 'peninha', 'raul-seixas', 'rubel', 'secos-&-molhados', 'tie', 'tim-maia', 'tom-jobim', 'toquinho', 'tribalistas', 'vinicius-de-moraes']
    paragraph_bool = input('Parágrafos? (0 ou 1): ')
    paragraph_bool = False if (paragraph_bool=='0') else True
    concat_bool = input('Concatenar em 1 arquivo? (0 ou 1): ')
    concat_bool = False if (concat_bool=='0') else True
    for artist in artists:
        if concat_bool == True:
            download_musicas_concat_json(artist, paragraph_bool)
        else:
            download_musicas(artist, paragraph_bool)