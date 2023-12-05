from flask import Flask, url_for, request, redirect, abort, jsonify

app = Flask(__name__, static_url_path='', static_folder='staticpages')

chocolates=[
    {"id": 1, "chocolateName": "DairyMilk", "Brand": "Cadbury", "Price": 1000},
    {"id": 2, "chocolateName": "MarsBar", "Brand": "Mars", "Price": 2000},
    {"id": 3, "chocolateName": "Kitkat", "Brand": "Nestle", "Price": 1500}
]
nextId=4

@app.route('/')
def index():
    return "hello"
#get all
@app.route('/chocolates')
def getAll():
    return jsonify(chocolates)
# find By id
@app.route('/chocolates/<int:id>')
def findById(id):
    foundchocolates = list(filter (lambda t : t["id"]== id, chocolates))
    if len(foundchocolates) == 0:
        return jsonify({}) , 204
    return jsonify(foundchocolates[0])

# create
# curl -X POST -d "{\"chocolateName\":\"test\", \"Brand\":\"some guy\", \"Price\":123}" http://127.0.0.1:5000/chocolates
@app.route('/chocolates', methods=['POST'])
def create():
    global nextId
    if not request.json:
        abort(400)
    
    chocolate = {
        "id": nextId,
        "chocolateName": request.json["chocolateName"],
        "Brand": request.json["Brand"],
        "Price": request.json["Price"]
    }
    chocolates.append(chocolate)
    nextId += 1
    return jsonify(chocolate)


    return "served by Create "

#update
# curl -X PUT -d "{\"chocolateName\":\"new chocolateName\", \"Price\":999}" -H "content-type:application/json" http://127.0.0.1:5000/chocolates/1
@app.route('/chocolates/<int:id>', methods=['PUT'])
def update(id):
    foundchocolates = list(filter(lambda t: t["id"] == id, chocolates))
    if len(foundchocolates) == 0:
        return jsonify({}), 404
    currentchocolate = foundchocolates[0]
    if 'chocolateName' in request.json:
        currentchocolate['chocolateName'] = request.json['chocolateName']
    if 'Brand' in request.json:
        currentchocolate['Brand'] = request.json['Brand']
    if 'Price' in request.json:
        currentchocolate['Price'] = request.json['Price']

    return jsonify(currentchocolate)

#delete
# curl -X DELETE http://127.0.0.1:5000/chocolates/1
@app.route('/chocolates/<int:id>', methods=['DELETE'])
def delete(id):
    foundchocolates = list(filter(lambda t: t["id"] == id, chocolates))
    if len(foundchocolates) == 0:
        return jsonify({}), 404
    chocolates.remove(foundchocolates[0])

    return jsonify({"done":True})


if __name__ == "__main__":
    app.run(debug=True)