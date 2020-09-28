import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle

from http.server import HTTPServer, BaseHTTPRequestHandler
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
api = Api(app)

with open("intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)


    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)


def chat(msg):
    # print("Start talking with the bot (type quit to stop)!")
    # while True:
    # inp = input("You: ")
    output_msg = ""
    inp = msg
    if inp.lower() == "quit":
        output_msg = "quit"

    results = model.predict([bag_of_words(inp, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    if results[results_index] > 0.7:

        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        # print(random.choice(responses))
        output_msg = random.choice(responses)

    else:
        output_msg = "I didn't get that, try again";
    
    return output_msg

def saveJson (json_obj):
    
    """ jsonObjs = {
        "status": "success",
        "data": {
            "id": 311,
            "name": "Wint"
        }
    } """

    with open('questions.json', 'r+') as f:

        """ data = json.load(outfile)
        data.update(json_obj)
        outfile.seek(0)
        json.dump(data, outfile) """

        f.seek(0,2)                                #Go to the end of file    
        if f.tell() == 0 :                         #Check if file is empty
            f.write(json.dumps([json_obj]).encode())  #If empty, write an array
        else :
            f.seek(-1,2)           
            f.truncate()                           #Remove the last character, open the array
            f.write(' , '.encode())                #Write the separator
            f.write(json.dumps(json_obj).encode())    #Dump the dictionary
            f.write(']'.encode()) 

@app.route('/', methods=['GET','OPTIONS'])
# @cross_origin(origin='*',headers=['Content-Type','Authorization'])
class Chat(Resource):
    def get(self, msg):
        # print(msg)

        response = chat(msg)
        # if (response == "I didn't get that, try again"):
        #     saveJson(msg)
        
        # response.headers.add('Access-Control-Allow-Origin', '*')
        
        return jsonify(response)
        # return response

api.add_resource(Chat, "/chat/<msg>")

if __name__ == '__main__':
    app.run(port=5002)