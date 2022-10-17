import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# def lookup(title):
#     """Look up quote for symbol."""
#     # url = "https://imdb8.p.rapidapi.com/auto-complete"
#     # querystring = {"q": title }
#     # headers = {
# 	# "X-RapidAPI-Key": "092b95aacemsh4b71bfb8d191abap10fc36jsne17d93bc13d8",
# 	# "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
#     # }
#     # Contact API
#     try:
#         api_key = os.environ.get("API_KEY")
#         response = requests.get(url)
#         response.raise_for_status()
#     except requests.RequestException:
#         return None

#     # Parse response
#     try:
#         quote = response.json()
#         return {
#             "name": quote["companyName"],
#             "price": float(quote["latestPrice"]),
#             "symbol": quote["symbol"]
#         }
#     except (KeyError, TypeError, ValueError):
#         return None
