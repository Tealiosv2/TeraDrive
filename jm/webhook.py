# webhook to listen for changes then update database accordingly

from flask import Flask, request, abort, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        data = request.get_json()
        challenge = data["challenge"]

        print(request.json)
        
        return jsonify({"challenge": challenge})

        # print(request.json)
        # return "success", 200
    else:
        abort(400)

if __name__ == "__main__":
    app.run(debug=True)
