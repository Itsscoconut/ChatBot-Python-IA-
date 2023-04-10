import nltk, json, pickle
import numpy as np
import random
from nltk.stem import SnowballStemmer
from tensorflow.keras.models import load_model

lematizador = SnowballStemmer('spanish')

modelo = load_model("file_models/modelo_chatbot_pugs.h5")
intenciones = json.loads(open("file_models/intenciones.json").read())
palabras = pickle.load(open("file_models/palabras.pkl","rb"))
categorias = pickle.load(open("file_models/categorias.pkl","rb"))


def expresion_regular(data):
    import regex

    res_nom = regex.search(u'\w+[a-z]', data)
    res_cel = regex.search(u'\d\d\d\d\-\d\d\d\d', data)
    res_hor = regex.search(u'\w\d', data)
    if res_nom == None:
        r = "Uy, parece no ingresaste tu nombre :-( vuelve a intentarlo!"

    elif res_cel == None:
        r = "Uy, parece no ingresaste tu numero de celular :-( vuelve a intentarlo!\n Recuerda que debes colocar un guion para que sea un numero valido ;-)"

    elif res_hor == None:
        r = "Uy, parece no ingresaste el codigo del horario :-( vuelve a intentarlo!"
    
    else:
        s = "Perfecto! Su cita ha sido agendada con exito ", res_nom.group(),"\n","Estaremos llamando para recordarle su cita al numero de celular: ", res_cel.group(),"\n","GUAU, tienes alguna otra consulta?"
        r = ''.join(s)
    
    return(r)
       


def limpiar_conversacion(sentence):
    sentence_words=nltk.word_tokenize(sentence)
    sentence_words=sentence_words=[lematizador.stem(palabras.lower()) for palabras in sentence_words] 
    return sentence_words

def bow (sentence,palabras,show_details=True): 
    sentence_words=limpiar_conversacion(sentence)
    
    contenedor=[0]*len(palabras)
    
    for i in sentence_words:
        for j,w in enumerate(palabras):
            if w==i: 
                contenedor[j]=1
                if show_details:
                    print("encontrado: ",w)
    return (np.array(contenedor))

def predict_class(sentence,model):
    p = bow(sentence,palabras,show_details=False) 
    res = model.predict(np.array([p]))[0] 
    
    ERROR_THRESHOLD=0.25
    results= [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD] 
    results.sort(key=lambda x: x[1], reverse=True) 
    
    return_list = []    
    for r in results:   
        return_list.append({"intent": categorias[r[0]], "probability": str(r[1])})   
    print("print de return list: ", return_list) 
    return return_list



def get_response(ints,intenciones_json, texto):
    tag= ints[0]["intent"]
    list_of_intents=intenciones_json["intenciones"] 
    
    for i  in list_of_intents:
        if (i["etiqueta"]==tag and tag == "agendar_cita"):
            result= expresion_regular(texto)
            break

        elif (i["etiqueta"]==tag and tag == "servicios"):
            result = i["respuestas"]
            break

        elif (i["etiqueta"]==tag and tag == "agradecimientos"):
            result = random.choice(i["respuestas"])
            break

        elif (i["etiqueta"]==tag):
            result= random.choice(i["respuestas"]) 
            break

    return result

def chatbot_response(text): 
    ints=predict_class(text,modelo) 
    res=get_response(ints, intenciones, text)
    return res


    
    
def bot(texto_us):
    res = chatbot_response(texto_us)
    return res

    
    
from intents_reference import start_intents
from model_builder import start_model
#from main import enviar_foto, enviar_respuesta

if __name__ == '__main__':
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = chatbot_response(sentence)
        print(resp)

