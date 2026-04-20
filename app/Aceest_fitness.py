from flask import Flask, jsonify

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to ACEest Fitness Gym App",
        "version": "v1"
    })

# Members route
@app.route('/members')
def members():
    return jsonify({
        "members": ["John", "Alice", "Rahul"]
    })

# Plans route
@app.route('/plans')
def plans():
    return jsonify({
        "plans": ["Basic", "Premium", "Pro"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
