from flask import render_template, Response
from app import app

@app.route('/', methods = ['GET'])
def index():
	return render_template(
        'index.html', 
        title="192.168.13.100",
        description="")