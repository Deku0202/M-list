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


def lookup(title):

    url = "https://imdb8.p.rapidapi.com/title/v2/find"
    q = {"title": title,"titleType":"movie,tvSeries,tvMiniSeries","limit":"25","sortArg":"moviemeter,asc"}

    headers = {
            "X-RapidAPI-Key": "092b95aacemsh4b71bfb8d191abap10fc36jsne17d93bc13d8",
            "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
        }    

    response = requests.get(url, headers=headers, params=q)
    search = response.json()

    results = search["results"]

    return results


def look(title):

    url = "https://imdb8.p.rapidapi.com/title/find"
    q = {"q": title}

    headers = {
            "X-RapidAPI-Key": "092b95aacemsh4b71bfb8d191abap10fc36jsne17d93bc13d8",
            "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
        }    
 
    response = requests.get(url, headers=headers, params=q)
    search = response.json()

    results = search["results"]

    return results

def rating(title):
    
    url = "https://imdb8.p.rapidapi.com/title/get-ratings"

    q = {"tconst":title}

    headers = {
            "X-RapidAPI-Key": "092b95aacemsh4b71bfb8d191abap10fc36jsne17d93bc13d8",
            "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
        }    

    response = requests.get(url, headers=headers, params=q)
    raw = response.json()

    rating = raw["rating"]

    return rating
