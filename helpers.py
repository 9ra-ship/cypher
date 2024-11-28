import os
import requests
import urllib.parse
import yfinance as yf  # Import the yfinance library

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol using Yahoo Finance."""
    
    try:
        # Use yfinance to get the data for the given symbol
        stock = yf.Ticker(symbol)
        stock_info = stock.history(period="1d")  # Get the most recent data
        
        # If no data is found, return None
        if stock_info.empty:
            return None
        
        # Extract relevant information from the stock data
        quote = stock_info.iloc[-1]  # Get the last day's data (most recent)
        
        return {
            "name": stock.info.get("longName", "N/A"),
            "price": quote["Close"],  # Latest closing price
            "symbol": symbol,
            "week52High": stock.info.get("fiftyTwoWeekHigh", "N/A"),
            "week52Low": stock.info.get("fiftyTwoWeekLow", "N/A"),
            "marketCap": stock.info.get("marketCap", "N/A"),
            "avgTotalVolume": stock.info.get("averageVolume", "N/A"),
            "primaryExchange": stock.info.get("exchange", "N/A")
        }
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
