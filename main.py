from flask import Flask, request
from flask_api import status
import logging
from nomeroff import Nomeroff
from object_pool import ObjectPool

recognizer_pool = ObjectPool(Nomeroff,
                             min_init=3,
                             max_capacity=10,
                             max_reusable=1000,
                             expires=60*60)

logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World from numberplate recognizer"


@app.route('/recognize', methods=['POST'])
def solve_captcha():
    response = {"result": "ok", "data": list()}

    if request.is_json:
        result_json = request.get_json()

        with recognizer_pool.get() as (recognizer, recognizer_stats):
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
