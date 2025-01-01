from marketorestpython.client import MarketoClient

#Storing Marketo REST API credentials in a dictionary
credentials = {
	"munchkinID":"",
	"client_id":"",
	"client_secret":""
}

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

def copyTokens(mc,tokens):
    name = str(input("Target folder name: \n"))
    folder = mc.execute(method='get_folder_by_name', name=name)
    id=folder[0].get('folderId')
    for i in tokens:
        mc.execute(method='create_token', id=str(id.get('id')), folderType=id.get('type'), name=i.get('name'), value=i.get('value'), type=i.get('type'))
        print(i.get('name')+" copied!")

def deleteTokens(mc,tokens,id):
    tokens = tokens
    id=id
    for i in tokens:
        mc.execute(method='delete_tokens', id=str(id.get('id')), folderType=id.get('type'), name=i.get('name'), type=i.get('type'))
        print(i.get('name')+" deleted!")

def createToken():
    name = input("Name:\n")
    type = input("Type:\n")
    value = input("Value:\n")
    token = {'name':name,'type':type,'value':value}
    return token

def getTokens(mc):
    name = str(input("Folder Name: \n"))
    folder = mc.execute(method='get_folder_by_name', name=name)
    id=folder[0].get('folderId')
    tokens = mc.execute(method='get_tokens', id=str(id.get('id')), folderType=id.get('type'))
    tokens = tokens[0].get('tokens')
    tokenlist =[]
    for i in tokens:
        tokenlist.append(i.get('name'))
    print(tokenlist)
    menu = input("Ready to copy?\nY\nN\nDel\n")
    if menu == "Y":
        copyTokens(tokens)
    if menu == "Del":
        deleteTokens(tokens,id)
    else:
        exit()

getTokens()