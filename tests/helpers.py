import json


# Return true if two responses have the same text component
def resp_comp(a, b):
	print("Response 1\n----------")
	print(json.loads(a.text))
	print("\nResponse 2\n----------")
	print(json.loads(b.text))
	return json.loads(a.text) == json.loads(b.text)

# Convert the returns 
def resp_data(resp):
	return json.loads(resp.text)

