# views.py
from django.http import JsonResponse

import json

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

@csrf_exempt
def process_stk_callback(request):
    print("Callback received")
    if request.method == 'POST':
        stk_callback_response = request.body.decode('utf-8')
        print("its post")
        # Log the response
        log_file = "stkresponse.json"
        with open(log_file, "a") as log:
            log.write(stk_callback_response)
        
        # Decode JSON data
        data = json.loads(stk_callback_response)
        
        if data and 'Body' in data and 'stkCallback' in data['Body']:
            stk_callback = data['Body']['stkCallback']
            result_code = stk_callback['ResultCode']
            print("has body")
            if result_code == 0:
                print("payed")
                callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
                amount = None
                transaction_id = None
                phone_number = None
                
                # Retrieve the authenticated user
                if request.user.is_authenticated:
                    user_instance = request.user
                else:
                    # Handle anonymous user case
                    # You might want to customize this based on your authentication logic
                    user_instance = None

                for item in callback_metadata:
                    if 'Name' in item and 'Value' in item:
                        if item['Name'] == 'Amount':
                            amount = item['Value']
                        elif item['Name'] == 'MpesaReceiptNumber':
                            transaction_id = item['Value'] 
                        elif item['Name'] == 'PhoneNumber':
                            phone_number = item['Value']
                
                if all([amount, transaction_id, phone_number]):
                    # Save to database
                    # transaction = Transactions(
                    #     user=user_instance,
                    #     amount=amount,
                    #     transactionCode=transaction_id,
                    #     phoneNumber=phone_number
                    # )
                    # transaction.save()
                    
                    return JsonResponse({'success': True})

    return JsonResponse({'success': False})
