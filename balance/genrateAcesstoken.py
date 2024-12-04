import requests
from django.http import JsonResponse
import os
from dotenv import load_dotenv
load_dotenv()

def get_access_token(request):
    consumer_key =os.environ.get('consumer_key')  
    consumer_secret = os.environ.get('consumer_secret') 
    access_token_url = os.environ.get('access_token_url') 
    headers = {'Content-Type': 'application/json'}
    auth = (consumer_key, consumer_secret)
    try:
        response = requests.get(access_token_url, headers=headers, auth=auth)
        response.raise_for_status() 
        result = response.json()
        access_token = result['access_token']
        return JsonResponse({'access_token': access_token})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)})
    





    