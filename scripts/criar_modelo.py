# importando as bibliotecas
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow import keras
import numpy as np

with open(f"..\\musicas\\chico-buarque.txt", "r", encoding="utf8") as arquivo:
    dados_treino = arquivo.read()

corpo_do_texto = dados_treino.lower().split("\n")
tokenizer = Tokenizer()
tokenizer.fit_on_texts(corpo_do_texto)
total_palavras = len(tokenizer.word_index) + 1

# vamos tentar treinar o modelo para ele entender que dado uma lista de palavras a próxima é "essa" e assim por diante

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

# criando o modelo
model = Sequential()
model.add(Embedding(total_palavras, 240, input_length=frase_de_tamanho_maximo-1))
model.add(Bidirectional(LSTM(150)))
model.add(Dense(total_palavras, activation='softmax'))
adam = Adam(learning_rate=0.01)
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
history = model.fit(xs, ys, epochs=100, verbose=1)

# salvar modelo
model.save('modelo_chico_buarque.keras')
