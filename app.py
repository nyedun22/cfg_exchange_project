from flask import Flask, jsonify, request

# run app file to view flask site
app = Flask(__name__)

# creating app routes -- example used for now
@app.route('/')
def hello_world():
    return jsonify({'hello':'universe'})



if __name__ == '__main__':
     # app.run(debug=True, host='0.0.0.0')
     app.run(debug=True, port=5003)

