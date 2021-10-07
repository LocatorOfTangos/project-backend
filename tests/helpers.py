import json


# Return true if two responses have the same text component
def resp_comp(a, b):
	return json.loads(a.text) == json.loads(b.text)

def resp_data(resp):
	return json.loads(resp.text)

