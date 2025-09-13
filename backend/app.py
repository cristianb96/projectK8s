from flask import Flask
app = Flask(__name__)

@app.route('/health')
def health():
    return {'status': 'ok'}

@app.route('/api/orders')
def orders():
    return {'orders': []}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
