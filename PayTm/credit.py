import stripe
from django.conf import settings

def process_payment(amount, stripe_token):
    stripe.api_key = settings.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

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