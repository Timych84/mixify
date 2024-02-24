from flask import Flask, render_template, request

app = Flask(__name__)

def some_function():
    # Function that you want to execute when the button is clicked
    # This could be any complex logic you want
    try:
        # Your function logic here
        raise ValueError("Simulated error during playlist creation")
        result = "Success!"
    except Exception as e:
        # Handle any exceptions or errors
        result = f"Error: {str(e)}"

    return result

@app.route('/')
def index():
    return render_template('functest.html')

@app.route('/run-function', methods=['POST'])
def run_function():
    result = some_function()
    return result

if __name__ == '__main__':
    app.run(debug=True)
