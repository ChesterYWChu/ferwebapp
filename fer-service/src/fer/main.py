from flask import Flask, current_app, request, jsonify
import io
import model
import base64
import logging

app = Flask(__name__)
@app.route('/', methods=['POST'])
def predict():
    data = {}
    try:
        data = request.get_json()['data']
    except Exception:
        return jsonify(status_code='400', msg='Bad Request'), 400

    data = base64.b64decode(data)

    image = io.BytesIO(data)
    msg, predictions = model.predict(image)
    current_app.logger.info('predictions: %s', predictions)
    return jsonify(predictions=predictions, msg=msg)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)