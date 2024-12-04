import requests
from datetime import datetime
import json
import base64
from django.http import JsonResponse
from .genrateAcesstoken import get_access_token
from decimal import Decimal
import os
from dotenv import load_dotenv
load_dotenv()

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def initiate_stk_push(request):
   
    amount = request.POST.get('amount',500)  # Get the amount from the POST data
  
    access_token_response = get_access_token(request)
    if isinstance(access_token_response, JsonResponse):
        print("stk sent")
        access_token = access_token_response.content.decode('utf-8')
        access_token_json = json.loads(access_token)
        access_token = access_token_json.get('access_token')
        if access_token:
            amount = amount
            phone = 705752300
            try:
                
                if str(phone).startswith('0'):
                    phone_number = phone[1:]
                phone = f'254{phone_number}'
                print(phone)
            except Exception as e:
                if request.method == 'POST':
                    phone = request.POST['phone'].strip()
                    if str(phone).startswith('0'):
                        phone_number = phone[1:]
                        phone = f'254{phone_number}'
                        
                    # amount = request.POST['phone'].strip()
                phone = phone
            passkey = os.environ.get('passkey') 
            business_short_code = os.environ.get('business_short_code') 
            process_request_url = 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
            callback_url = ' https://6d25-102-212-236-41.ngrok-free.app/process_stk_callback/'
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()
            party_a = phone
            party_b = os.environ.get('party_b') 
            account_reference = 'KELISOLS AGENCIES'
            transaction_desc = 'stkPush test'
            stk_push_headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + access_token
            }
            
            stk_push_payload = {
                'BusinessShortCode': business_short_code,
                'Password': password,
                'Timestamp': timestamp,
                'TransactionType': 'CustomerBuyGoodsOnline',
                'Amount': amount,
                'PartyA': party_a,
                'PartyB': party_b,
                'PhoneNumber': party_a,
                'CallBackURL': callback_url,
                'AccountReference': account_reference,
                'TransactionDesc': transaction_desc,
                
            }

            try:
                response = requests.post(process_request_url, headers=stk_push_headers, json=stk_push_payload)
                response.raise_for_status()   
                # Raise exception for non-2xx status codes
                response_data = response.json()
                checkout_request_id = response_data['CheckoutRequestID']
                response_code = response_data['ResponseCode']
                
                if response_code == "0":
                    return JsonResponse({'CheckoutRequestID': checkout_request_id, 'ResponseCode': response_code})
                else:
                    return JsonResponse({'error': 'STK push failed.'})
            except requests.exceptions.RequestException as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'error': 'Access token not found.'})
    else:
        return JsonResponse({'error': 'Failed to retrieve access token.'})