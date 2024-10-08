import json
from faker import Faker
import random
from typing import Dict, List, Any

fake = Faker()

# Store generated users, products, transactions, and reviews globally
users: List[Dict[str, Any]] = []
products: List[Dict[str, Any]] = []
transactions: List[Dict[str, Any]] = []
product_reviews: List[Dict[str, Any]] = []


def generate_user_profile() -> Dict[str, Any]:
    """
    Generate a fake user profile with some semi-structured inconsistencies.
    """
    user_id = fake.uuid4()  # Unique user ID
    user_profile = {
        "user_id": user_id,
        "name": fake.name(),
        "age": random.choice([None, fake.random_int(min=18, max=80), "unknown"]),
        "email": random.choice([None, fake.email(), ""]),
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "zip_code": random.choice([fake.zipcode(), None])
        }
    }
    users.append(user_profile)  # Store user profile to maintain uniqueness
    return user_profile


def generate_transaction() -> Dict[str, Any]:
    """
    Generate a fake transaction with some semi-structured inconsistencies.
    """
    user_id = random.choice([None] + [user["user_id"] for user in users])  # Choose a valid user ID
    transaction = {
        "user_id": user_id,
        "amount": round(random.uniform(10.0, 500.0), 2),
        "date": random.choice([fake.date_this_year(), None, "unknown"]),
        "description": fake.sentence(nb_words=5)
    }
    transactions.append(transaction)  # Store transaction
    return transaction


def generate_product_review() -> Dict[str, Any]:
    """
    Generate a fake product review with some semi-structured inconsistencies.
    """
    user_id = random.choice([None] + [user["user_id"] for user in users])  # Choose a valid user ID
    product_id = random.choice([None] + [product["product_id"] for product in products])  # Choose a valid product ID
    product_review = {
        "user_id": user_id,
        "product_id": product_id if product_id else fake.uuid4(),  # If product_id is None, create a new ID
        "rating": random.choice([random.randint(1, 5), None, "unrated"]),
        "review_text": fake.text(max_nb_chars=200),
        "review_date": random.choice([fake.date_this_year(), None, "unknown"]),
        "helpful_votes": random.choice([None, random.randint(0, 100)])
    }

    # Simulate missing fields
    if random.random() > 0.5:
        product_review.pop("review_date")

    if random.random() > 0.6:
        product_review.pop("helpful_votes")

    # Add random extra fields
    if random.random() > 0.7:
        product_review["extra_notes"] = fake.sentence(nb_words=8)

    product_reviews.append(product_review)  # Store product review
    return product_review


def generate_product_metadata() -> Dict[str, Any]:
    """
    Generate fake product metadata with some semi-structured inconsistencies.
    """
    product_id = fake.uuid4()  # Unique product ID
    product_metadata = {
        "product_id": product_id,
        "product_name": fake.catch_phrase(),
        "category": fake.word(),
        "price": round(random.uniform(5.0, 100.0), 2),
        "stock": random.choice([None, fake.random_int(min=0, max=100)])
    }
    products.append(product_metadata)  # Store product metadata
    return product_metadata


def generate_data(num_docs: int) -> Dict[str, List[Dict[str, Any]]]:
    """
    Generate a dictionary containing separate collections of fake data documents.
    """
    for _ in range(num_docs):
        document_type = random.choice(["user", "transaction", "review", "product"])
        if document_type == "user":
            generate_user_profile()
        elif document_type == "transaction":
            generate_transaction()
        elif document_type == "review":
            generate_product_review()
        elif document_type == "product":
            generate_product_metadata()

    return {
        "users": users,
        "transactions": transactions,
        "product_reviews": product_reviews,
        "products": products,
    }

