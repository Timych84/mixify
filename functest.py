from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('functest.html')

@app.route('/transform', methods=['POST'])
def transform():
    text = request.form['inputText']
    transformed_text = text + ' modified'
    return jsonify({'transformed_text': transformed_text})

if __name__ == '__main__':
    app.run(debug=True)
