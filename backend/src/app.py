from flask import Flask, request, jsonify #Request se encarga de extrar los datos que el cliente me podria estar enviando.  
from flask_pymongo import PyMongo
from flask_cors import CORS

from bson import ObjectId

app = Flask(__name__) #inicializa flask.
app.config['MONGO_URI'] = 'mongodb://localhost/pythonreactdb' #base de datos local.
mongo = PyMongo(app) #devuelve un objeto para pader manipularlo. es la conexión con la base de datos local.

CORS(app)

db = mongo.db.users #colección de usuarios

@app.route('/users', methods=['POST']) # Crea rutas para crear usuarios 
def createUser():
    id = db.insert_one({         #Guardar datos con metodo Insert
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    })

    return jsonify(str(id.inserted_id)) #str convierte el objeto en formato string                


@app.route('/users', methods=['GET']) # Crea rutas para obtener usuarios // consultar todos los datos
def getUsers():
    users = []
    for doc in db.find(): #busquead de todos los datos y retorna una lista.
         users.append({
            '_id': str(ObjectId(doc['_id'])), #ID en formato string
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password']
         })
    return jsonify(users)

@app.route('/user/<id>', methods=['GET']) # Crea rutas para obtener un usuario 
def getUser(id):
    user = db.find_one({'_id':ObjectId(id)})
    print(user)
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'email': user['email'],
        'password': user['password']        
    })

@app.route('/users/<id>', methods=['DELETE']) # Crea rutas para eliminar usuarios 
def deleteUser(id):
    db.delete_one({'_id': ObjectId(id)}) #Elimina el primer dato que coincide con la búsqueda. 
    return jsonify({'msg': 'User delete'})

@app.route('/users/<id>', methods=['PUT']) # Crea rutas para poder editar usuario 
def updeteUser(id):
    db.update_one({'_id': ObjectId(id)}, {'$set':{
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }})
    return jsonify({'msg': 'User update'})

if __name__ == "__main__":
    app.run(debug=True) #debug cada vez que hace cambio el código reinicia.
