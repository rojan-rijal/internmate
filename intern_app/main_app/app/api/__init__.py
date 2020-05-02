"""
@@File_Name: __init__.py
@@File_Description: This code creates a blueprint
allowing app/__init__.py to run api routes through
the views.py file for API calls.
@@Last_Update_Date: April 20, 2020 
@@CODEOWNERS: Rojan Rijal
"""
from flask import Blueprint

api = Blueprint('api', __name__)

from . import views
