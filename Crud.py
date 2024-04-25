from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Configura la conexión a MongoDB en la nube
client = MongoClient('mongodb+srv://greatstackdev:12345@cluster0.tyi79fn.mongodb.net/distribuidos')
db = client['mydatabase']
collection = db['items']

# Verifica la conexión
try:
    client.server_info()  # Intente obtener información del servidor MongoDB
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print("Error al conectar a MongoDB:", e)

# Rutas para el CRUD
@app.route('/items', methods=['GET'])
def get_items():
    items = list(collection.find())
    return jsonify({'items': items})

@app.route('/items/<id>', methods=['GET'])
def get_item(id):
    try:
        # Convertir el ID en un entero para buscar por el campo "_id"
        item_id = int(id)
        item = collection.find_one({'_id': item_id})
        if item:
            return jsonify(item)
        else:
            return jsonify({'error': 'Elemento no encontrado'}), 404
    except ValueError:
        return jsonify({'error': 'ID inválido'}), 400


@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    if 'nombre' not in data or 'descripcion' not in data or 'precio' not in data or '_id' not in data:
        return jsonify({'error': 'Faltan campos obligatorios (nombre, descripcion, precio, _id)'}), 400
    item_id = data['_id']  # Obtener el ID proporcionado por el usuario
    if collection.find_one({'_id': item_id}):
        return jsonify({'error': 'El ID proporcionado ya existe'}), 400
    collection.insert_one(data)  # Inserta el elemento en la base de datos
    return jsonify({'id': item_id})


@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    data = request.json
    try:
        # Convierte el ID a un ObjectId
        item_id = int(id)
        result = collection.update_one({'_id': item_id}, {'$set': data})
        return jsonify({'modified_count': result.modified_count})
    except ValueError:
        return jsonify({'error': 'ID inválido'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    try:
        # Convierte el ID a un ObjectId
        item_id = int(id)
        result = collection.delete_one({'_id': item_id})
        if result.deleted_count > 0:
            return jsonify({'message': 'Producto eliminado'})
        else:
            return jsonify({'message': 'Producto no encontrado'}), 404
    except ValueError:
        return jsonify({'error': 'ID inválido'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
