from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session

from base64 import decodestring
import json
import os
import glob
from flask_cors import CORS, cross_origin
import random
app = Flask(__name__, static_url_path='/static')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


DB_FILE = "database.json"
BLANK_SCHEMA = "schema.json"
HTML_TEMPLATE = "template.html"
PARAMETERS_IN_INFO = ["problem_type", "description", "example", "additional_resources", "image_url"]
LIST_OBJECTS = ["additional_resources", "image_url", "example"]
LESSON_DATA = ["title", "color1", "color2"]
# This is not really a good way of doing this, but I'll try to change this up later

if os.path.exists(DB_FILE) == False:
	os.system("echo {} >  " + DB_FILE)

def create_db_backup():
	a = glob.glob("static/backups/")
	os.system("cp {} {}".format(DB_FILE, "static/backups/" + DB_FILE.partition(".")[0]+"{}_backup.json".format(len(a)+1)))

def add_problem_to_file(problemType, data):
	# This means the field had text before submission
	problemType = problemType.lower()
	create_db_backup()
	a = json.load(open(DB_FILE))
	a[problemType] = data
	with open(DB_FILE, 'w') as outfile:
		json.dump(a, outfile, indent=4)

def modify_problem(problemType, param, data):
	# This means the field had text before submission
	problemType = problemType.lower()
	create_db_backup()
	a = json.load(open(DB_FILE))
	val = request.form.get(param, None)
	if val != None and param in a[problemType]:
		if param in LIST_OBJECTS:
			a[problemType][param].append(val)
		else:
			a[problemType][param] = val
	with open(DB_FILE, 'w') as outfile:
		json.dump(a, outfile, indent=4)

def get_problem_type_info(problemType):
	problemType = problemType.lower()
	myJsonFile = json.load(open(DB_FILE))
	if problemType not in myJsonFile:
		return None
	return myJsonFile[problemType]

@app.route('/', methods=['GET'])
def index():
	return redirect("https://steppy.netlify.com/", code=302)

@app.route('/admin', methods=['GET'])
def indexTest():
	return render_template("mainPage.html")

@app.route('/addNewProblem', methods=['POST'])
@cross_origin()
def add_problem():
	temp_dict = {}
	# Dictionary holding new problem information
	problem_type = request.form.get('problem_type', None)
	# This is the problem/guide name
	print request.form
	if problem_type != None:
		# This means the problem type was specified
		for val in PARAMETERS_IN_INFO:
			if val in LIST_OBJECTS:
				temp_dict[val] = request.form.getlist(val)
			else:
				temp_dict[val] = request.form.get(val, None)
		add_problem_to_file(problem_type, temp_dict)
		# Adds the inputted problem to a file
	return ('', 204)

def disable_cors(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@app.route("/users", methods=["GET"])
@cross_origin()
def get_users():
	DB = json.load(open(DB_FILE))
	return DB.keys()

@app.route('/delete', methods=['GET'])
@cross_origin()
def delete():
	a = json.load(open(DB_FILE))
	returnPage = "<h1>Warning: Clicking any of these links will delete the lessons.  Use with care.</h1>"
	for i, val in enumerate(a['thomais']['lessons']):
		returnPage += '''<h2><a onclick="return confirm('Are you sure you want to delete this item?');" href="delete/{}'''.format(val[0]['id']) + '">Delete: {}</a></h2>'.format(val[0]['title'])
	return returnPage

@app.route('/backups', methods=['GET'])
@cross_origin()
def backups():
	g = []
	for val in glob.glob("static/backups/*"):
		v = "static/" + val.partition("static/")[2]
		g.append(v)
	returnPage = "<h1>Backups</h1>"
	for v in g:
		returnPage += '''<h2><a href="{}'''.format(v) + '">Backup: {}</a></h2>'.format(v)
	return returnPage

@app.route('/delete/<task_id>', methods=['GET'])
@cross_origin()
def delete_single(task_id):
	valz = False
	create_db_backup()
	a = json.load(open(DB_FILE))
	for i, val in enumerate(a['thomais']['lessons']):
		if str(val[0]['id']) == task_id:
			del a['thomais']['lessons'][i]
			valz = True
	if valz == True:
		with open(DB_FILE, 'w') as outfile:
			json.dump(a, outfile, indent=4)
	return redirect("https://steppy.netlify.com/", code=302)

@app.route('/remove/<int:task_id>', methods=['DELETE'])
@cross_origin()
def delete_task(task_id):
	val = False
	create_db_backup()
	a = json.load(open(DB_FILE))
	for i, va in enumerate(a['thomais']['lessons']):
		if va[0]['id'] == task_id:
			del a['thomais']['lessons'][i]
			val = True
	if val == True:
		with open(DB_FILE, 'w') as outfile:
			json.dump(a, outfile, indent=4)
	return jsonify({'result': val})

@app.route("/lessons/<username>", methods=["GET"])
@cross_origin()
def get_lessons(username):
	username = username.lower()
	DB = json.load(open(DB_FILE))
	if username in DB:
		return jsonify([x[0] for x in DB[username]['lessons']])
	else:
		return jsonify([])

@app.route('/update', methods=['POST'])
@cross_origin()
def update_problem():
	problem_type = request.form.get('problem_type', None)
	if problem_type != None:
		problemType = problem_type.lower()
		create_db_backup()
		a = json.load(open(DB_FILE))
		param = request.form.get('param', None)
		if problem_type in a:
			if param != None:
				val = request.form.get('update', None)
				if val != None and param in a[problemType]:
					if param in LIST_OBJECTS:
						a[problemType][param].append(val)
					else:
						a[problemType][param] = val
				with open(DB_FILE, 'w') as outfile:
					json.dump(a, outfile, indent=4)
	return ('', 204)

@app.route('/addImage', methods=['POST'])
@cross_origin()
def add_image():
	#print request.form
	#print request.json
	problem_type = request.json.get('image', None)
	if problem_type != None:
		fileType = problem_type.partition('/')[2].partition(';')[0]
		g = []
		for i in range(10):
			g.append(str(random.randint(1,9)))
		name = ''.join(g)
		imagestr = problem_type.partition('base64,')[2]
		with open("static/{}.{}".format(name, fileType),"wb") as f:
			f.write(decodestring(imagestr))
		return "https://teamthomais.herokuapp.com/static/{}.{}".format(name, fileType)
	return "https://via.placeholder.com/140x100"

@app.route('/addUser', methods=['POST'])
def add_user():
	username = request.form.get('username', None)
	if username != None:
		create_db_backup()
		a = json.load(open(DB_FILE))
		a[username] = {"lessons": []}
		with open(DB_FILE, 'w') as outfile:
			json.dump(a, outfile, indent=4)
	return ('', 204)

@app.route('/addLesson', methods=['POST'])
def add_lesson():
	info = {}
	username = "thomais"
	allData = request.json
	print len(allData)
	info['title'] = allData.pop(0)['value']
	info['color1'] = allData.pop(0)['value']
	info['color2'] = allData.pop(0)['value']
	#info['color2'] = allData.pop(0)
	info['steps'] = []
	indexVal = 0
	while len(allData) > 0:
		info['steps'].append({"step_index": indexVal, "step_description": allData.pop(0)['value'], "step_img": allData.pop(0)['value'], "ex_description": allData.pop(0)['value'], "example_img": allData.pop(0)['value']})
		indexVal += 1
	if username != None:
		create_db_backup()
		a = json.load(open(DB_FILE))
		if username in a:
			maxNum = 0
			for val in a[username]['lessons']:
				if val[0]['id'] > maxNum:
					maxNum = val[0]['id']
			info['id'] = maxNum + 1
			a[username]['lessons'].append([info])
			with open(DB_FILE, 'w') as outfile:
				json.dump(a, outfile, indent=4)
	return ('', 204)



@app.route('/guide/<problemType>', methods=['GET'])
def get_guide(problemType):
	problemType = problemType.lower()
	if os.path.exists("templates/{}.html".format(problemType)) == False:
		os.system("cp templates/{} templates/{}.html".format(HTML_TEMPLATE, problemType))
	problem_info = get_problem_type_info(problemType)
	if problem_info == None:
		return "<h1>{} Does not exist</h1>".format(problemType)
	return render_template("{}.html".format(problemType), info=problem_info, single_params=[x for x in problem_info.keys() if x not in LIST_OBJECTS], list_objects=LIST_OBJECTS)

@app.route('/getGuideNames', methods=['GET'])
def get_guide_names():
	a = json.load(open(DB_FILE))
	return jsonify(a.keys())

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
