import os

def main():
    
    current_dir = os.getcwd()
    encoding = 'utf-8'
    file_name = 'musicas_concat'
    file_destination = f'{current_dir}/musicas/{file_name}'
    artists_path = f'{current_dir}/musicas/artistas/'

    if os.path.exists(f'{file_destination}.txt'):
        print ('Arquivo já criado')
        return
    file_concat = open(f'{file_destination}.txt','a+',encoding = encoding)
    file_concat_no_double_newline = open(f'{file_destination}_no_double_newline.txt','a+',encoding = encoding)
    file_concat_no_newline = open(f'{file_destination}_no_newline.txt','a+',encoding = encoding)

    for artist in os.listdir(artists_path):
        for song in os.listdir(f'{artists_path}/{artist}'):
            with open (f'{artists_path}/{artist}/{song}','r',encoding = encoding) as song_file:
                #print (f'Adicionando {song}.')
                #song[:-4] = musica menos o .txt
                header = f'Poema: MPB {song[:-4]}\n'
                footer = '<|endoftext|>\n'
                lyric = song_file.read()
                no_double_newline = lyric.replace('\n\n','\n')
                no_newline = no_double_newline.replace('\n',' ')
                
                file_concat.write(f'{header}{lyric}{footer}')
                file_concat_no_double_newline.write(f'{header}{no_double_newline}{footer}')
                file_concat_no_newline.write(f'{header}{no_newline}{footer}')

    file_concat.close()
    file_concat_no_double_newline.close()
    file_concat_no_newline.close()
    print ('Sucesso')

if __name__ == '__main__':
    main()