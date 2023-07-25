from django.shortcuts import render, redirect, get_object_or_404
from .forms import AccountForm, TransactionForm
from .models import Account, Transaction

# Create your views here.
#This function will render the Home page when requested
def home(request):
    form = TransactionForm(data=request.POST or None) #retrieve transaction form
    # Checks if request method is POST
    if request.method == 'POST':
        pk = request.POST['account'] # If the form is submitted, retrieve which account the user wants to view
        return balance(request, pk) # call balance function to render that account's balance sheet
    content = {'form': form} # Pass content to the template in a dictionary
    #Adds content of form to page
    return render(request, 'checkbook/index.html', content)

#This function will rend the Create New Account page when requested
def create_account(request):
    form = AccountForm(data=request.POST or None)  # Retrieve the Account form
    # Checks if request method is POST
    if request.method == 'POST':
        if form.is_valid():  # Chek to see if the submitted form is valid if so, saves the form
            form.save()  # Saves new account
            return redirect('index')  # Returns user back to the home page
    content = {'form': form}  # Saves content to the template as a dictionary
    # adds content to form to page
    return render(request, 'checkbook/CreateNewAccount.html', content)


# This function will render the Balance page when requested
def balance(request, pk):
    account = get_object_or_404(Account, pk=pk) # REtrieve the requested account using its primary key
    transactions = Transaction.Transactions.filter(account=pk) # Retrieve all of that account's transactions
    current_total = account.initial_deposit # Create account total variable, starting with initial deposit value
    table_contents = {} # Create a dictionary into which transaction information will be placed
    for t in transactions: # Loop through transactions and determine which is a deposit or withdrawal
        if t.type == 'Deposit':
            current_total += t.amount # If deposit add amount to balance
            table_contents.update({t: current_total}) # Add transaction and total to the dictionary
        else:
            current_total -= t.amount # If withdrawal subtract amount from balance
            table_contents.update({t: current_total}) # Add transaction and total to the dictionary
    #Pass account, account total balance, and transaction information to the template
    content = {'account': account, 'table_contents': table_contents, 'balance': current_total}
    return render(request, 'checkbook/BalanceSheet.html', content)

#This function will render the Transaction page when requested
def transaction(request):
    form = TransactionForm(data=request.POST or None) # Retrieve the Transaction form
    # Checks if request method is POST
    if request.method == 'POST':
        if form.is_valid(): #Check to see if the submitted from is valid and if so, saves the form
            pk = request.POST['account'] #Retrieve which account the transaction was for
            form.save() # Saves the transaction form
            return balance(request, pk) # Renders balance of the accounts Balance Sheet
        return redirect('index')  # Redirects the uer to the home page after form submission
    # Pass content to the template in a dictionary
    content = {'form': form}
    #Adds content of form to page
    return render(request, 'checkbook/AddTransaction.html', content)




