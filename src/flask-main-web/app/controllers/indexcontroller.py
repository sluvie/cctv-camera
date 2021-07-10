from flask import render_template, Response
from app import app

@app.route('/', methods = ['GET'])
def index():
	return render_template(
        'index.html', 
        title="Camera Management System",
        description="")