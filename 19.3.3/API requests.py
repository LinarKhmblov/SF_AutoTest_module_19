import requests
import json


status = 'available'
base_url = 'https://petstore.swagger.io/v2'
data = {
    'id': 0,
    'name': "Uno",
    'status': "available"
}
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

# GET запрос
get_response = requests.get(f'{base_url}/pet/findByStatus?status={status}', headers={'accept':'application/json'})
print("GET:", get_response.json())

# POST запрос
post_response = requests.post(f'{base_url}/pet', json=data, headers=headers)
print("POST:", post_response.json())

get_new_data = json.loads(post_response.content)
mypetId = get_new_data['id']

# DELETE запрос
delete_response = requests.delete(f'{base_url}/pet/{mypetId}')
print("DELETE:", delete_response.status_code)

# PUT запрос
new_data = {
    'id': mypetId,
    'name': "Tolyan"
}
put_response = requests.put(f'{base_url}/pet', json=new_data)
print("PUT:", put_response.json())
