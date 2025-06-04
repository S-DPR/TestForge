# yourapp/pipeline.py

def custom_create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'user': user}

    email = details.get('email')
    if not email:
        raise ValueError('이메일 누락')

    return {
        'user': strategy.create_user(email=email)
    }
