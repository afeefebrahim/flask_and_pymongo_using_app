import os
from os.path import join
import json
import csv
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,make_response,jsonify,make_response
from werkzeug import secure_filename
from gridfs import GridFS
from gridfs.errors import NoFile
from pymongo import MongoClient
from werkzeug import secure_filename
from pymongo import MongoClient
from collections import defaultdict
from bson import json_util
# import xlwt as xlwt
# import xlrd
import ast
#output = xlwt.Workbook()
# Flask
app = Flask(__name__)

#MongoDb configuration details here:
client = MongoClient('127.0.0.1', 27017)
db = client.MappingNowDE  # use a database called "test_database"
collection1 = db.InputHR   # and inside that DB, a collection called "files"
collection2 = db.InputFIN


grid_fs = GridFS(db)

def toJson(data):
	return json.dumps(data, default=json_util.default)


# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv','json','xlxs'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/upload', methods=['POST'])
def upload():

    	file = request.files['file']
        print type(file)
        folder = os.path.abspath('uploads')
        if len(os.listdir(folder)) > 0:
          for the_file in os.listdir(folder):
              file_path = os.path.join(folder, the_file)
              try:
                  if os.path.isfile(file_path):
                       os.unlink(file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
              except Exception as e:
                  print e

        if file or allowed_file(file.filename):
            print "*************************"
            print file
            filename = secure_filename(file.filename)
            print type(filename),filename
            print "*************************"
            fileid = {}
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = 'uploads/'+filename
            with open(path) as myFile:
                 fileid = grid_fs.put(myFile,content_type="application/csv",filename=file.filename)
            print path
            print grid_fs.get(fileid)
        return redirect(url_for('uploads', filename=file.filename))




@app.route('/uploads/<filename>', methods=['GET'])
def uploads(filename):
    print "#######################"
    print filename
    filename = filename
    print "#######################"
#    for files in filenames:
    file_url = 'uploads/'+filename

    with open(file_url) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print "row"
            text_file_doc = {"file_name": filename, "contents" : row }
            collection1.insert(text_file_doc)
 #   files=files+1
     #collection.update({ _id: "" },{"$set":{"testing":"appleStore"}},{ "$setOnInsert": { "defaultQty": "100" }})
    #return json.dumps({'status': 'File saved successfully'}), 200
    return render_template('index2.html', filename=filename)
    #return redirect(url_for('upload_second', filename=filename))



################################################################For Second HTML File#####################################################################################

@app.route('/uploads/upload_second', methods=['POST'])
def upload_second():

    	file = request.files['file']

    #filenames = []
        folder = os.path.abspath('uploads')
        if len(os.listdir(folder)) > 0:
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                    print(e)

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #filenames.append(filename)

        return redirect(url_for('uploads_second', filename=filename))
    #return redirect(url_for('uploads', filename=filenames))



@app.route('/uploads/upload_second/<filename>', methods=['GET'])
def uploads_second(filename):
#    for files in filenames:
    file_url = 'uploads/'+filename
    with open(file_url) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            text_file_doc = {"file_name": filename, "contents" : row }
            collection2.insert(text_file_doc)
 #   files=files+1
     #collection.update({ _id: "" },{"$set":{"testing":"appleStore"}},{ "$setOnInsert": { "defaultQty": "100" }})
    #return json.dumps({'status': 'File saved successfully'}), 200
    return render_template('out.html', filename=filename)


##########################################################################################################################################################################


#########################################################For Third HTML FILE OUTPUT #######################################################################################
@app.route('/uploads/upload_second/upload_output', methods=['POST'])
def upload_output():
    # Get the name of the uploaded files
    	file = request.files['file']
    #filenames = []
    #for file in uploaded_files:

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Save the filename into a list, we'll use it later
            #filenames.append(filename)

        return redirect(url_for('uploads_out', filename=filename))
    #return redirect(url_for('uploads', filename=filenames))




@app.route('/uploads/upload_second/upload_output/<filename>', methods=['GET'])
def uploads_out(filename):
   file_url = 'uploads/'+filename
   f = open(file_url, 'rb')
   reader = csv.reader(f)
   headers = reader.next()
   head = []
   for r in headers:
     head.append(r)
  # print head
   json_results = []
   if request.method == 'GET':
     result1 = collection1.find_one()
     result2=collection2.find_one()
     for result, v in result1.items():
			#print result , v
			if(result=='contents'):
				for k,l in result1['contents'].iteritems():
					#print k
					json_results.append(k)
     for result, v in result2.items():
			#print result , v
			if(result=='contents'):
				for k,l in ast.literal_eval(result2['contents']).iteritems():
					#print k
					json_results.append(k)

   #return jsonify({'output' : head ,'input'  : json_results})
   #return redirect(url_for('index11'))
   return render_template('Display.html', head=head, obj=json_results)

###########################################################################################################################################################################

###########################################################Reandering HTML Page for Mapping#################################################################################
@app.route('/uploads/upload_second/upload_output/index11', methods=['GET','POST'])
def index11():


	#if request.method == 'POST':
		#for i in request.get_current_object():

	#head = uploads_out()
	select11 = request.form.getlist('Item_1')
	out_head=request.form.getlist('output_head')
	#lll=request.form.getlist('ll')
	##print lll

	#for i in out_head:
	#	print i

	#print head
	#print select11
	#print out_head
	dictionary = dict(zip(out_head,  [[i] for i in select11]))
	#print dictionary

	content= json.dumps(dictionary)
		#jsonify({(str(out_head)) : (str(select11))})
	   	#return render_template("tasks.html")
	#return "Hello Final"
	dict_out={}
	#content = request.get_json(force=True)
	cursor1 = collection1.find()
	cursor2=collection2.find()
	#print cursor1
	dlist=[]
	dd = defaultdict(list)
	resultDict={}
	for dict1 in cursor1:
	      #for attribute1, value1 in dict1.iteritems():
		#print attribute1, value1

		dict_out={}
		for k,v in dict1['contents'].items():
			dict_out[k]=v
			#print k,v
		#print dict_out
		dlist.append(dict_out)
	       	#dict_out.clear()

	for dict1 in cursor2:
	      #for attribute1, value1 in dict1.iteritems():
		#print attribute1, value1

		dict_out={}
        if type(dict1) == dict:
            for  k,v in dict1['contents'].items():
                dict_out[k]=v
			#print k,v
		#print dict_out
        dlist.append(dict_out)
	       	#dict_out.clear()

	#print dlist



	for d in (dlist): # you can list as many input dicts as you want here
	    for key, value in d.iteritems():
		dd[key].append(value)

	#print(dd)
	#print content
	resultDict={}
	dict2={}
	for at1, val1 in dd.iteritems():
 		#print at1
		#print "hello"
        	for k2,v2 in dictionary.items():
                       	#print v2[0]
        	 	if v2[0]==at1:
  				#print v2,at1
            			resultDict[at1]=val1

	#print resultDict
	#return jsonify(resultDict)
	response = make_response(jsonify(resultDict))
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
   	response.headers["Content-Disposition"] = "attachment; filename=Mapping.json"
    	return response





############################################################################################################################################################################################

#@app.route('/uploads/<filename>')
#def uploaded_file(filename):
   #  return send_from_directory(app.config['UPLOAD_FOLDER'],
        #                       filename)

if __name__ == '__main__':
      app.run(debug=True)
