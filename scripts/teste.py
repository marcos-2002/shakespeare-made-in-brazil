import json
from datasets import load_dataset

with open("musicas\\zeca-baleiro-train.json", "r") as file:
    text = file.read()
    data_train = json.loads(text)
print(len(data_train))

with open("musicas\\zeca-baleiro-test.json", "r") as file:
    text = file.read()
    data_test = json.loads(text)
print(len(data_test))


data_files = {"train": "musicas\\zeca-baleiro-train.json", "test": "musicas\\zeca-baleiro-test.json"}
songs_it_dataset = load_dataset("json", data_files=data_files)
print(songs_it_dataset)

