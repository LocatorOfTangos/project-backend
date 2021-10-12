import json


# Return true if two responses have the same text component
def resp_comp(a, b):
	print("Response 1\n----------")
	print(a.json())
	print("\nResponse 2\n----------")
	print(b.json())
	return json.loads(a.text) == json.loads(b.text)

# Convert the returns 
def resp_data(resp):
	return resp.json()

