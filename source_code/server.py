'''
Created on Jan 10, 2017

@author: hanif
'''

from flask import Flask, flash, render_template, redirect, url_for, request, \
	session, jsonify
from module.database import Database
import logging , sys , json

logger = logging.getLogger('APP_LOGGER')
logger.setLevel(logging.DEBUG)
format = logging.Formatter(
	"%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
logger.addHandler(ch)


app = Flask(__name__)
app.secret_key = "mys3cr3tk3y"
db = Database()

@app.route('/')
def index():
    data = db.read(None)
    
    return render_template('index.html', data = data)

@app.route('/add/')
def add():
    return render_template('add.html')

@app.route('/get', methods = ['GET'])
def getdata():
    result = {}
    data = db.get_record(None)
    success_msg = "Total records in PhoneBook"
    result['result'] = 'success'
    result['count'] = data['data']
    result['msg'] = success_msg
    logger.debug(result)
    return jsonify(result)

@app.route('/addphone', methods = ['POST', 'GET'])
def addphone():
	result = {}
	if request.method == 'POST' or request.form['save']:

		if request.headers['Content-Type'] == 'text/plain':
			return "Text Message: " + request.data

		elif request.headers['Content-Type'] == 'application/json':
			data_str = json.dumps(request.json)
			data = json.loads(data_str)

		elif request.headers[
			'Content-Type'] == 'application/x-www-form-urlencoded':
			if request.form['save']:
				logger.debug(request.form)
			data = request.form

		if db.insert(data):
			success_msg = "A new phone number has been added"
			result['result'] = 'success'
			result['msg'] = success_msg
			flash(success_msg)
		else:
			error_msg = "A new phone number can not be added"
			result['result'] = 'failure'
			result['msg'] = error_msg
			flash(error_msg)

		if request.headers['Content-Type'] == 'application/json':
			return jsonify(result)
		else:
			return redirect(url_for('index'))
	else:
		if request.headers['Content-Type'] == 'application/json':
			return jsonify(result)
		else:
			return redirect(url_for('index'))

@app.route('/update/<int:id>/')
def update(id):
    data = db.read(id);
    
    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['update'] = id
        return render_template('update.html', data = data)

@app.route('/updatephone', methods = ['POST'])
def updatephone():
    if request.method == 'POST' and request.form['update']:
        
        if db.update(session['update'], request.form):
            flash('A phone number has been updated')
           
        else:
            flash('A phone number can not be updated')
        
        session.pop('update', None)
        
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    
@app.route('/delete/<int:id>/')
def delete(id):
    data = db.read(id);
    
    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['delete'] = id
        return render_template('delete.html', data = data)

@app.route('/deletephone', methods = ['POST'])
def deletephone():
    if request.method == 'POST' and request.form['delete']:
        
        if db.delete(session['delete']):
            flash('A phone number has been deleted')
           
        else:
            flash('A phone number can not be deleted')
        
        session.pop('delete', None)
        
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug = True, port=5002, host="0.0.0.0")