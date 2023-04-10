import pickle
import nltk
import json
import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import SGD
from nltk.stem import SnowballStemmer
import matplotlib.pyplot as plt
lematizador = SnowballStemmer('spanish')

palabras_ignoradas = ["?", "¿", "!", "¡", ",", ".", "|", "°", "*"]



def tokenizer():
    palabras = []
    categorias = []
    documentos = []
    
    archivo_json = open("file_models/intenciones.json").read()
    intenciones = json.loads(archivo_json)
    
    for intencion in intenciones["intenciones"]:
        for patron in intencion["patrones"]:
            w_token = nltk.word_tokenize(patron)
            palabras.extend(w_token)
            
            
            documentos.append((w_token, intencion["etiqueta"]))
            
            if intencion["etiqueta"] not in categorias:
                categorias.append(intencion["etiqueta"])
            
    return palabras, categorias, documentos



def lematizer(palabras, categorias, documentos):
    palabras = [lematizador.stem(pal.lower()) for pal in palabras if pal not in palabras_ignoradas]
    palabras2= palabras
    

    pickle.dump(palabras, open("file_models/palabras.pkl", "wb"))
    pickle.dump(categorias, open("file_models/categorias.pkl", "wb"))

    return palabras2
    
    

def training(palabras, categorias, documentos):
    entrenamiento=[]
    output_empty=[0]*len(categorias)

    for doc in documentos:
        contenedor=[]
        patrones_pal=doc[0]
        patrones_pal=[lematizador.stem(palabra.lower()) for palabra in patrones_pal if palabra not in palabras_ignoradas ]
    
        for word in palabras:
            contenedor.append(1) if word in patrones_pal else contenedor.append(0)
        
        output_row=list(output_empty)
        output_row[categorias.index(doc[1])] = 1

        entrenamiento.append([contenedor, output_row])
    
    entrenamiento=np.array(entrenamiento)
    x_train = list(entrenamiento[:,0])
    y_train = list(entrenamiento[:,1])
    
    return x_train, y_train



def model_builder(x_train, y_train):
    modelo = Sequential()

    modelo.add(Dense(128, input_shape=(len(x_train[0]),), activation='relu')) 
    modelo.add(Dropout(0.5))
    modelo.add(Dense(64,activation='relu')) 
    modelo.add(Dropout(0.5))
    modelo.add(Dense(len(y_train[0]),activation='softmax'))

    sgd=SGD(learning_rate=0.01, weight_decay=1e-6, momentum=0.9, nesterov=True)

    modelo.compile(loss="categorical_crossentropy",optimizer=sgd,metrics=["accuracy"])

    hist=modelo.fit(np.array(x_train),np.array(y_train),epochs=300,batch_size=5,verbose=1)
    modelo.save("file_models/modelo_chatbot_pugs.h5",hist)
    print("modelo creado")

    

    # Entrenar el modelo y guardar el historial
    history = modelo.fit(np.array(x_train), np.array(y_train), epochs=300, batch_size=5, verbose=1)

    # Crear la gráfica
    plt.plot(history.history['accuracy'])
    #plt.plot(history.history['val_accuracy'])
    plt.title('Precisión del modelo')
    plt.ylabel('Precisión')
    plt.xlabel('Epoch')
    plt.legend(['Entrenamiento', 'Validación'], loc='upper left')
    plt.show()

    
    
    
def start_model():
    
    palabras, categorias, documentos = tokenizer()
    palabras2 = lematizer(palabras, categorias, documentos)
    x_train, y_train = training(palabras2, categorias, documentos)
    model_builder(x_train, y_train)
    
    
    

from intents_reference import start_intents

if __name__ == '__main__':
    start_intents()
    start_model()
    
            
            
