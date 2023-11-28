import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course):
    try:
        product = stripe.Product.create(name=course.title, description=course.description)
        price = stripe.Price.create(product=product.id, unit_amount=int(course.price * 100), currency="usd")
        return product, price
    except Exception as e:
        print(f"Ошибка при создании продукта в Stripe: {e}")
        return None, None