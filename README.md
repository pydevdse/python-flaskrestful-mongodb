# python-flaskrestful-mongodb

phone contats book:

     - endpoints: "/api_mongo", "/api_mongo/":
            post - json={"number": number), # reqiured
                         "name": "name"),
                         "lastname": "lastname",
                         "note": "note",
                         }
            get: - for all list contacts
            get: json={'id':id}  - for one contact
            put:  json ={"id":id, # reqiured
                         "number": number, 
                         "name": "name",
                         "lastname": "lastname",
                         "note": "note",
                         }
            delete: json ={"id":id} # reqiured

