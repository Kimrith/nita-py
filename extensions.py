from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
cors = CORS(
    resources={
        r"/api/*": {
            "origins": ["http://localhost:4200"]
        }
    },
)

# Initialize rate limiter (specific limits configured on POST routes)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
)