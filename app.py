from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import json
import os

app = Flask(__name__, static_url_path='/static')

DB_FILE = "database.json"
HTML_TEMPLATE = "template.html"
PARAMETERS_IN_INFO = ["problem_type", "description", "example", "additional_resources", "image_url"]
LIST_OBJECTS = ["additional_resources", "image_url", "example"]
# This is not really a good way of doing this, but I'll try to change this up later

if os.path.exists(DB_FILE) == False:
	os.system("echo {} >  " + DB_FILE)

def create_db_backup():
	os.system("cp {} {}".format(DB_FILE, DB_FILE.partition(".")[0]+"_backup.json"))

def add_problem_to_file(problemType, data):
	# This means the field had text before submission
	create_db_backup()
	a = json.load(open(DB_FILE))
	a[problemType] = data
	with open(DB_FILE, 'w') as outfile:
		json.dump(a, outfile)

def modify_problem(problemType, param, data):
	# This means the field had text before submission
	create_db_backup()
	a = json.load(open(DB_FILE))
	val = request.form.get(param, None)
	if val != None and param in a[problemType]:
		if param in LIST_OBJECTS:
			a[problemType][param].append(val)
		else:
			a[problemType][param] = val
	with open(DB_FILE, 'w') as outfile:
		json.dump(a, outfile)

def get_problem_type_info(problemType):
	return json.load(open(DB_FILE))[problemType]

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html", params=PARAMETERS_IN_INFO)


'''@app.route('/addNewProblem', methods=['POST'])
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
	return ('', 204)'''

@app.route('/add/<problem_type>', methods=['POST'])
def add_problem(problem_type):
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

@app.route('/guide/<problemType>', methods=['GET'])
def get_guide(problemType):
	if os.path.exists("templates/{}.html".format(problemType)) == False:
		os.system("cp templates/{} templates/{}.html".format(HTML_TEMPLATE, problemType))
	problem_info = get_problem_type_info(problemType)
	return render_template("{}.html".format(problemType), info=problem_info, mykeys=problem_info.keys())

@app.route('/getGuideNames', methods=['GET'])
def get_guide_names():
	a = json.load(open(DB_FILE))
	return jsonify(a.keys())

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
