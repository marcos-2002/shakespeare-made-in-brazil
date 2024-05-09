from tensorflow.keras.models import load_model
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np

# carregar dados
with open(f"..\\musicas\\chico-buarque.txt", "r", encoding="utf8") as arquivo:
    dados_treino = arquivo.read()


corpo_do_texto = dados_treino.lower().split("\n")
tokenizer = Tokenizer()
tokenizer.fit_on_texts(corpo_do_texto)
total_palavras = len(tokenizer.word_index) + 1

frases_imputadas = []
for linha in corpo_do_texto:
  lista_de_tokens = tokenizer.texts_to_sequences([linha])[0]
  for i in range(1,len(lista_de_tokens)):
    frase_comeco_ao_fim = lista_de_tokens[:i+1]
    frases_imputadas.append(frase_comeco_ao_fim)

frase_de_tamanho_maximo = max([len(x) for x in frases_imputadas])
frases_imputadas = np.array(pad_sequences(frases_imputadas, maxlen=frase_de_tamanho_maximo, padding='pre'))
xs = frases_imputadas[:,:-1]
labels = frases_imputadas[:,-1]
ys = tf.keras.utils.to_categorical(labels, num_classes=total_palavras)


# usar o modelo já criado
model = load_model('.\modelo_chico_buarque.keras')

frase_inicial = input('Digite a frase inicial do poema: ')
proximas_palavras = 30

# prever as palavras
for _ in range(proximas_palavras):
  lista_de_tokens = tokenizer.texts_to_sequences([frase_inicial])[0]
  lista_de_tokens = pad_sequences([lista_de_tokens], maxlen = frase_de_tamanho_maximo-1)
  indice_proxima_palavra = np.argmax(model.predict(lista_de_tokens), axis=-1)
  palavra_de_saida = ""
  for palavra, indice in tokenizer.word_index.items():
    if indice == indice_proxima_palavra:
      palavra_de_saida = palavra
      break
  frase_inicial += " " + palavra_de_saida

print(frase_inicial)