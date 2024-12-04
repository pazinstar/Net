from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserBalance
from django.utils import timezone


from .genrateAcesstoken import get_access_token
from .stkPush import initiate_stk_push
from .query import query_stk_status
from .tokens import generate_token
from .callback import process_stk_callback

consumer_key= "0G0Y7IyT3yQyRKOllANXPeX7cmMbKGQzYuxR9FDA3UERMMSo"
consumer_secret="SMGGLnq75FlyxFwfbrrKUyHvbe6JwgmCBaxsaNZc9GmR8YQD8CP9Um81I5Xk38gk" 
access_token_url="https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
passkey="e98f96c005c16dcefcf3dcfeb2265fd8fab0184fbd617ad20920262ff5ae23b0"
business_short_code=6434570
party_b=8701060

def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
    
        user = UserBalance.objects.filter(username=username).first()
       
        if user:
            return redirect('balance:show_balance', username=username)
        else:
            messages.error(request, 'User does not exist. Contact admin.')
    return render(request, 'balance/home.html')

def show_balance(request, username):
    user = UserBalance.objects.get(username=username)
    return render(request, 'balance/show_balance.html', {'user': user})
def Contact_view(request):
    
    return render(request, 'balance/contact.html')



def admin_login_view(request):
   # Check if the user is logged in through the session
    if request.session.get('admin_logged_in') and request.session.get('admin_username') == "Wivock":
        # Redirect to the superadmin login if the logged-in user is Wivock
        return redirect('admin:login')
    else:
        # Redirect to a different page or show an error for unauthorized access
        return redirect('balance:admin_dashboard')

def deposit(request):
    username = request.GET.get('username', '')  # Retrieve the username from the request
    context = {
        "username": username,
        "paybill": "247247",
        "account": "0600184509295",
    }
   
    return render(request, 'balance/deposit.html', context)



from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import UserBalance  # Replace with your actual model
from .forms import UserBalanceForm
from django.utils.timezone import now

def admin_dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('balance:loginadmin')
    # Initialize variables
    form = UserBalanceForm()
    balances = UserBalance.objects.all()
    editing = False
  
    if request.method == 'POST':
        if 'edit_id' in request.POST:  # Handle editing an existing balance
            balance_id = request.POST['edit_id']
            user_balance = get_object_or_404(UserBalance, id=balance_id)
            form = UserBalanceForm(instance=user_balance)  # Prepopulate the form
            editing = True
        elif 'save_id' in request.POST:  # Save the edited record
            user_balance = get_object_or_404(UserBalance, id=request.POST['save_id'])
            form = UserBalanceForm(request.POST, instance=user_balance)
            if form.is_valid():
                form.save()
                messages.success(request, "Balance updated successfully.")
                return redirect('balance:admin_dashboard')
            else:
                messages.error(request, "Failed to update balance. Check your input.")
        else:  # Handle creating a new balance
            form = UserBalanceForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "New balance created successfully.")
                return redirect('balance:admin_dashboard')
            else:
                messages.error(request, "Failed to create balance. Check your input.")

    elif 'edit_id' in request.GET:  # Populate the form for editing when requested via GET
        balance_id = request.GET['edit_id']
        user_balance = get_object_or_404(UserBalance, id=balance_id)
        form = UserBalanceForm(instance=user_balance)
        editing = True

    context = {
        'form': form,
        'balances': balances,
        'editing': editing,
         'today': now(),
    }
    return render(request, 'balance/admin.html', context)

from .models import AdminList


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AdminList

def loginadmin(request):
    # Redirect if the user is already logged in
    if request.user.is_authenticated:
        return redirect('balance:admin_dashboard')

    if request.method == 'POST':
        # Get the username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Attempt to find the admin in AdminList
        admin = AdminList.objects.filter(username=username).first()

        # Check if admin exists and password matches
        if admin and admin.password == password:  # Check plain-text password match
            # If the credentials are correct, log the user in (set the session)
            request.session['admin_logged_in'] = True
            request.session['admin_username'] = username
            return redirect('balance:admin_dashboard')  # Redirect to the admin dashboard
        else:
            # If authentication fails, show an error message
            messages.error(request, "Invalid username or password. Please try again.")
            return render(request, 'balance/adminlogin.html')  # Render the login page again with an error

    # If it's a GET request, render the login page
    return render(request, 'balance/adminlogin.html')
def logoutadmin(request):
    # Clear the session data to log the user out
    request.session.flush()  # This will clear the session and log the user out

    # Optionally, add a success message
    messages.success(request, "You have been logged out successfully.")

    # Redirect to the login page after logging out
    return redirect('balance:loginadmin')  # Adjust the URL if needed