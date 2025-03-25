from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        value = float(request.form['value'])
        result = value * 2  # Placeholder logic for calculations
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Please enter a valid number'}), 400

if __name__ == '__main__':
    app.run(debug=True)
