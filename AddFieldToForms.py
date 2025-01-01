from marketorestpython.client import MarketoClient
import json
import csv
import pandas as pd

#add Pandas dataframe as output option
#add JSON as a potential output option
#add CSV as a potential output option

#Storing Marketo REST API credentials in a dictionary
credentials = {
	"munchkinID":"",
	"client_id":"",
	"client_secret":""
}

# API name of field you'd like to add
fieldToAdd = "" 

# Forms to update
formNamePattern = ""

#Options: CSV, Pandas dataframe (write in 'pandas'), JSON
preferredOutput = ''

#Marketo REST API configuration options
api_limit=None
max_retry_time=None
requests_timeout=(3.0, 10.0)

#Establish a connection to the Marketo REST API
mc = MarketoClient(
	credentials['munchkinID'], 
	credentials['client_id'], 
	credentials['client_secret'], 
	api_limit, 
	max_retry_time, 
	requests_timeout
	)

def getForms(mc,formNamePattern):
	retrievedForms = mc.execute( 
		method='get_forms', 
		status="approved", 
		folderId=None, 
		folderType=None, 
		maxReturn=None
		)
	formList = []
	for form in retrievedForms:
		if form['name'] == formNamePattern:
			formList.append(
				{
					"id":form['id'],
					"url":form['url'],
					"name":form['name']
				}
			)
	return formList

def addField(mc,formList,fieldToAdd):
	for form in formList:
		field = mc.execute(
			method='create_form_field', 
			id=form["id"], 
			fieldId=fieldToAdd, 
			formPrefill=False
		)
		form['success'] = field['result']['success']
	return formList

def output(data,choice=None):
	if choice == None:
		choice = input(
			'''Data is ready for output! Please select your output format:
			
			1 - CSV
			2 - Pandas DataFrame
			3 - JSON file'''
		)
	if type(choice) == str:
		choice.lower()

	if choice == 1 or choice == 'csv':
		fileName = input('File Name: ')
		with open(fileName+'.csv','w',newline='') as csvfile:
			fieldnames = data[0].keys()
			writer = csv.DictWriter(csvfile,fieldnames=fieldnames,extrasaction='ignore')
			writer.writeheader()
			for i in data:
				writer.writerow(i)
			csvfile.close()
		return fileName+".csv"
	if choice == 2 or choice == 'pandas':
		df = pd.DataFrame(data)
		return df
	if choice == 3 or choice == 'json':
		fileName = input('File Name: ')
		with open(fileName+".json","w") as writefile:
			file = json.dump(data,writefile)
			writefile.close()
			return file
		
def init(mc,fieldToAdd=None,preferredOutput=None,formNamePattern=None):
	if formNamePattern == None:
		formNamePattern = input('Types of forms to modify: ')
	print('Retrieving forms...')
	formList = getForms(mc,formNamePattern)
	print(str(len(formList))+" found.")
	if fieldToAdd == None:
		fieldToAdd = input('Field to add: ')
	formList = addField(mc,formList,fieldToAdd)
	file = output(formList,preferredOutput)
	print(file)
	print('To set your new field as a hidden field, use the URL values in your output file to go through each form and adjust as needed.')
