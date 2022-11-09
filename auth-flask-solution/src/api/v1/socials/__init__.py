from flask import Blueprint

auth_socials_v1 = Blueprint('auth_socials_v1', __name__)

from . import google, facebook
