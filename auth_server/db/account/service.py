from db.account.models import Account
from django.contrib.auth.hashers import make_password

def create_account(login_id, password):
    account = Account.objects.create(login_id=login_id, password=make_password(password))
    return account

def get_account(account_id):
    return Account.objects.get(id=account_id)

def update_account(account_id, login_id, password):
    account = Account.objects.get(id=account_id)
    account.login_id = login_id
    account.password = make_password(password)
    account.save()
    return account

def delete_account(account_id):
    account = Account.objects.get(id=account_id)
    if account:
        account.delete()
        return True
    return False
