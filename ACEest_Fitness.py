from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api")
def api_home():
    return jsonify(
        {
            "application": "ACEest Fitness & Gym",
            "status": "running",
            "service": "devops-cicd-assignment",
        }
    )


@app.get("/health")
def health():
    return jsonify({"health": "ok"})


@app.get("/versions")
def versions():
    return jsonify(
        {
            "versions": [
                "Aceestver-1.0.py",
                "Aceestver-1.1.py",
                "Aceestver1.1.2.py",
                "Aceestver2.0.1.py",
                "Aceestver-2.1.2.py",
                "Aceestver-2.2.1.py",
                "Aceestver-2.2.4.py",
                "Aceestver-3.0.1.py",
                "Aceestver-3.1.2.py",
                "Aceestver-3.2.4.py",
            ]
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
