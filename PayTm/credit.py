import stripe
from django.conf import settings

def process_payment(amount, stripe_token):
    #stripe.api_key = 

    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency='usd',
            source=stripe_token
        )
        # Update your backend database accordingly (e.g., mark the order as paid, send a confirmation email to the user)
        return True, 'Payment successful'
    except stripe.error.CardError as e:
        return False, 'Card was declined'