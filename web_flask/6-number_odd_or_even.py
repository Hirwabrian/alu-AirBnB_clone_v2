#!/usr/bin/python3
""" a flask web application """

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/',strict_slashes =False)
def hello():
    """ return the string hello hbnb """
    return 'Hello HBNB!'

@app.route('hbnb',strict_slashes =False)
def hbnb():
    """ return the string hbnb """
    return 'HBNB'

@app.route('/c/<text>',strict_slashes =False)
def text(text):
    """ return the string c followed by the value of the text variable """
    return 'C %s' % text.replace('_', ' ')

@app.route('/python/',defaults = {'text': 'is cool'} ,strict_slashes =False)
@app.route('/python/<text>',strict_slashes =False)
def python(text='is cool'):
    """ return the string python followed by the value of the text variable """
    return 'Python %s' % text.replace('_', ' ')

@app.route('/number/(<int:n>)',strict_slashes =False)
def number(n):
    """ return the string n is a number only if n is an integer """
    return f"{n} is a number"

@app.route('/number_template/<int:n>',strict_slashes =False)
def template(n):
    """display a HTML page only if n is an integer"""
    return render_template('5-number.html', n=n)

@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def even_odd(n):
    """display a HTML page only if n is an integer"""
    even_0dd = "even" if n % 2 == 0 else "odd"
    return render_template('6-number_odd_or_even.html', n=n, even_0dd = even_0dd)


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=5000)