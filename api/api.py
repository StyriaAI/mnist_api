import logging
from io import BytesIO

from flask import Blueprint, request, current_app

from helpers import ApiException, generate_ok_response, preprocess_jpeg_image
from model_client import IMAGE_SHAPE

bp = Blueprint('digit', __name__)


@bp.route("/", methods=["GET"])
def status():
    """
    Return basic status on root route.
    """
    return generate_ok_response("API running")


@bp.route("/classify", methods=["POST"])
def classify():
    """
    Classify image from request body.
    """
    raw_img = BytesIO(request.get_data())

    try:
        img = preprocess_jpeg_image(raw_img, IMAGE_SHAPE)
    except Exception as e:
        logging.exception(e)
        raise ApiException("Invalid image")

    digit = current_app.model_client.classify(img)
    return generate_ok_response({"digit": digit})
