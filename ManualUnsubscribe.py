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

def unsub():
    emails = str(input("Input emails separated by commas: "))
    emails = emails.split(',')
    leads = []
    for i in emails:
        leads.append(
            {"email":i, 
             'Unsubscribed':'True', 
             'UnsubscribedReason': 'Direct Email Request'
            }
        )
    update = mc.execute(
        method='create_update_leads',
        leads=leads,
        action='updateOnly',
        lookupField='email',
        partitionName='Default'
    )
    for i in emails:
        print(str(i) + " has been unsubscribed.")
    input("\nAll set! Press enter to close.")

unsub()
