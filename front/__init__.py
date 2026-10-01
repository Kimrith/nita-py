from flask import Blueprint

user_bp = Blueprint('user', __name__)

# Import route modules so decorators attach to user_bp
from . import home
from . import account
from . import products
from . import auth
from . import cart
from . import checkout
from . import contact