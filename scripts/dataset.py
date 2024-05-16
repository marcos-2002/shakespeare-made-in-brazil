import json
from datasets import load_dataset

artists = ['5-seco', 'alceu-valenca', 'ana-frango-eletrico', 'anavitoria', 'belchior', 'caetano-veloso', 'cartola', 'cassia-eller', 'cassiano', 'cazuza', 'chico-buarque', 'cicero', 'djavan', 'elis-regina', 'elza-soares', 'gal-costa', 'geraldo-vandre', 'gilberto-gil', 'gilsons', 'gonzaguinha', 'joao-gilberto', 'jorge-ben-jor', 'kid-abelha', 'maria-bethania', 'marisa-monte', 'milton-nascimento', 'nando-reis', 'novos-baianos', 'peninha', 'raul-seixas', 'rubel', 'secos-&-molhados', 'tie', 'tim-maia', 'tom-jobim', 'toquinho', 'tribalistas', 'vinicius-de-moraes']

file_path_train = f'musicas\\musicas-train.json'
file_path_test = f'musicas\\musicas-test.json'
with open(file_path_train, 'a', encoding='utf-8') as file_train:
    data = []
    for artist in artists:
        with open(f"musicas\\{artist}-train.json", "r", encoding="utf-8") as file:
            text_train = file.read()
            data_train = json.loads(text_train)
        data.extend(data_train)
        print(f'train - {artist} salvo')
    json_data_train = json.dumps(data)
    file_train.write(f'{json_data_train}\n')
with open(file_path_test, 'a', encoding='utf-8') as file_test:
    data = []
    for artist in artists:
        with open(f"musicas\\{artist}-test.json", "r", encoding="utf-8") as file:
            text_test = file.read()
            data_test = json.loads(text_test)
        data.extend(data_test)
        print(f'test - {artist} salvo')
    json_data_test = json.dumps(data)
    file_test.write(f'{json_data_test}\n')

data_files = {"train": "musicas\\musicas-train.json", "test": "musicas\\musicas-test.json"}
songs_it_dataset = load_dataset("json", data_files=data_files)
print(songs_it_dataset)
print(songs_it_dataset['train'][100])
print(songs_it_dataset['test'][100])
