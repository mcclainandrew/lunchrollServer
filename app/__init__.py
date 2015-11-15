from flask import Flask

app = Flask(__name__)

from app import repository
from app import services
from app import views