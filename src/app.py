import os
from flask import Flask, render_template, request
from utils import APIException, generate_sitemap
from flask_cors import CORS
from datastructures import FamilyStructure
from flask import Flask, jsonify

app = Flask(__name__)

jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [ 7, 13, 22],
    "id": 1
})

jackson_family.add_member({
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3],
    "id":2
   
})

jackson_family.add_member({
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1],
    "id":3
})

jackson_family.add_member({
    "first_name": "Tommy",
    "age": 23,
    "lucky_numbers": [34,65,23,4,6],
    "id": 3443  # Asegúrate de usar este ID exacto
})


@app.route("/")
def home():
    return generate_sitemap(app)

@app.route('/member', methods=['GET'])
def handle_hello():
    member = jackson_family.get_all_members()
    return jsonify(member), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if  member:
         return jsonify(member), 200
    return jsonify({"error":"Member not found"}), 404
   
@app.route('/member', methods=['POST'])  # Cambiado de '/add' a '/member'
def add_member():
    try:
        new_member = {
            "first_name": request.json['first_name'],
            "age": request.json['age'],
            "lucky_numbers": request.json['lucky_numbers'],
            "id": request.json.get('id', jackson_family._generateId())  # Usar id proporcionado o generar uno
        }
        jackson_family.add_member(new_member)
        return jsonify(new_member), 200  # Cambiado para devolver el miembro añadido
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    if jackson_family.delete_member(id):
        return jsonify({"done": True}), 200  # Cambiado para coincidir con el test
    return jsonify({"error": "Member not found"}), 404

@app.route('/member/<int:id>', methods=['PUT'])
def update_member(id):
    #Obtener los datos JSON del cuerpo de la solicitud
    update_data = request.get_json()
    if not update_data:
        return jsonify({"error":"No data provided"}),400
    #verificar si el miembro existe
    member = jackson_family.get_member(id)
    if not member:
        return jsonify({"error":"Member not found"}),404
    
    # jackson_family.update_member(id,update_data)

    # return jsonify({"message": "Member deleted successfully"}), 200
    try:
        jackson_family.update_member(id, update_data)
        return jsonify({"message": "Member updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
   
if __name__ == "__main__":
    app.run(debug=True)
