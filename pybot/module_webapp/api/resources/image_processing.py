from flask_restx import Resource
from flask_restx.api import HTTPStatus
from sqlalchemy_media.exceptions import ValidationError, AnalyzeError
from sqlalchemy.exc import IntegrityError

from pybot.module_webapp.dao import user

from ..api import api

from pybot.module_webapp.models import UserId

from sqlalchemy.exc import NoResultFound

from jsonschema.exceptions import ValidationError as JsonSchemaValidationError
from ..model import img_parser, img_model


import json

ns = api.namespace("image-processing", description="Card operations")

from cardscan import scan
import cv2

from flask_restx import Resource
from flask import Response

import numpy as np


@ns.route("/find-card")
class FindCard(Resource):
    @ns.doc("find_card")
    @ns.expect(img_parser)
    def post(self):
        """Create a new user"""
        args = img_parser.parse_args()
        img = args["image"]
        if img is None:
            return "Error: No img provided", 404 # TODO better error
        img_data = img.read()
        nparr = np.frombuffer(img_data, np.uint8)
        cv2img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cards = scan(cv2img, blur=True);
        if len(cards) == 0:
            print("NO RESULTS")
            return None, HTTPStatus.OK
        card = cards[0]
        _, buffer = cv2.imencode(".png", card)
        return Response(buffer.tobytes(), content_type="image/png")
        return buffer.tobytes()
        cards = scan(cv2img)

        if len(cards) == 0:
            return None, HTTPStatus.OK
        card = cards[0]
        _, buffer = cv2.imencode(".png", card)
        return buffer.tobytes() # TODO

        return Response(buffer.tobytes(), content_type="image/png")
