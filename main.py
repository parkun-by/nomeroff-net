from flask import Flask, request
from flask_api import status
import logging
from nomeroff import Nomeroff
from pool import Pool


recognizer_pool = Pool(Nomeroff, amount=4)

logger = logging.getLogger(__name__)
app = Flask(__name__)


def hello():
    return "Hello World from numberplate recognizer"


@app.route('/recognize', methods=['POST'])
def solve_captcha():
    response = {"result": "ok", "data": list()}

    if request.is_json:
        result_json = request.get_json()

        with recognizer_pool.get() as recognizer:
            try:
                result = recognizer.recognize(result_json["path"])
                response["data"] = result

                return response, status.HTTP_200_OK
            except Exception:
                logger.exception("While numberplate recognition error occurred")

                response["result"] = "error"
                return response, status.HTTP_500_INTERNAL_SERVER_ERROR

    else:
        response["result"] = "error"
        return response, status.HTTP_204_NO_CONTENT


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=5000)
