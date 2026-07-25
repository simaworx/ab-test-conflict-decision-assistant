from flask import Flask, jsonify, render_template

from decision_engine import serialise_tree


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tree")
def tree_data():
    return jsonify(serialise_tree())


if __name__ == "__main__":
    app.run(debug=True)