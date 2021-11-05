import datetime
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask_restful import Resource, Api

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "restdb"
app.config["MONGO_URI"] = "mongodb://localhost:27017/restdb"
mongo = PyMongo(app).db

api = Api(app)

"""
@app.before_first_request
def create_user():
    contact_count = mongo.phones_table.count_documents({})

    
"""

"""
        contact_json = {
            "id": id,
            "number": number,
            "name": "name",
            "lastname": "lastname",
            "note": "note",
            "date": date,
            "update": datetime.datetime.utcnow(),
        }
"""

class ApiMongo(Resource):
    def post(self):
        if not request.json:
            return jsonify(Error="JSON not found in request")
        req = request.get_json()
        if not req:
            return jsonify(Error="Json not found")
        req_keys = req.keys()
        if "number" not in req_keys:
            return jsonify(Error="Field number not found")
        number = req.get("number")
        if not isinstance(number, int):
            return jsonify(Error="Number is not int")
        find_duplicate = mongo.phones_table.find_one(
            {"number": number}
        )  # .exits({'number': number})#
        if find_duplicate:
            return jsonify(Error="This number already use")
        name = req.get("name")
        if not name:
            name = ""
        if not isinstance(name, str):
            return jsonify(Error="Name not string")
        lastname = req.get("lastname")
        if not lastname:
            lastname = ""
        if not isinstance(lastname, str):
            return jsonify(Error="Last name not string")
        note = req.get("note")
        if not note:
            note = ""
        if not isinstance(note, str):
            return jsonify(Error="Note not string")
        users_count = mongo.phones_table.count_documents({}) + 1
        while True:
            if mongo.phones_table.find_one({"id": users_count}):
                users_count += 1
            else:
                break
        record_id = mongo.phones_table.insert_one(
            {
                "id": users_count,
                "number": number,
                "name": name,
                "lastname": lastname,
                "note": note,
                "date": datetime.datetime.utcnow(),
            }
        )
        return jsonify(id=users_count)

    def get(self):
        if not request.json:
            return jsonify(Error="JSON not found in request")
        if "id" in request.json:  # if id in request: find and return contact
            contact = mongo.phones_table.find_one({"id": request.json.get("id")})
            if not contact:
                return jsonify(
                    Error=f"Contact with id={request.json.get('id')} not found"
                )
            contact_json = {
                "id": contact.get("id"),
                "number": contact.get("number"),
                "name": contact.get("name"),
                "lastname": contact.get("lastname"),
                "note": contact.get("note"),
                "date": contact.get("date"),
                "update": contact.get("update"),
            }
            return jsonify(contact=contact_json)

        user_info = mongo.phones_table.find()  # else find all contacts and return
        list_users = []
        for user in user_info:
            key_user = {}
            for k in user.keys():
                if k == "_id":
                    continue
                key_user[k] = user[k]
            list_users.append(key_user)
        return jsonify({"contacts": list_users})

    def put(self):
        if not request.json:
            return jsonify(Error="JSON not found in request")
        if "id" not in request.json:  # if id in request: find and return contact
            return jsonify(Error="Id not found in request")
        contact = mongo.phones_table.find_one({"id": request.json.get("id")})
        contact_json = {
            "id": contact.get("id"),
            "number": contact.get("number"),
            "name": contact.get("name"),
            "lastname": contact.get("lastname"),
            "note": contact.get("note"),
            "date": contact.get("date"),
            "update": datetime.datetime.utcnow(),
        }
        if "number" in request.json:
            contact_json["number"] = request.json.get("number")
        if "name" in request.json:
            contact_json["name"] = request.json.get("name")
        if "lastname" in request.json:
            contact_json["lastname"] = request.json.get("lastname")
        if "note" in request.json:
            contact_json["note"] = request.json.get("note")
        contact_put = mongo.phones_table.update_one(contact, {"$set": contact_json})
        return jsonify(Update=str(contact_put))

    def delete(self):
        if not request.json:
            return jsonify(Error="JSON not found in request")
        if "id" not in request.json:  # if id in request: find and return contact
            return jsonify(Error="Id not found in request")

        result = mongo.phones_table.delete_one({"id": request.json.get("id")})
        return jsonify(Delete=result.deleted_count)


api.add_resource(ApiMongo, "/api_mongo", "/api_mongo/")

if __name__ == "__main__":
    app.run(debug=True)
