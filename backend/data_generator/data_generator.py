from sqlalchemy.orm import Session
from datetime import datetime
import random
import string

from backend.database import SessionLocal
from backend.models import users as users_model
from backend.models import family as family_model
from backend.models import purchase as purchase_model
from backend.models import store_product as store_product_model
from backend.core.utils import hash_password

NUM_FAMILIES = 120
MIN_PURCHASES = 60
MAX_PURCHASES = 80
MIN_ITEMS_PER_PURCHASE = 3
MAX_ITEMS_PER_PURCHASE = 10


def random_username():
    return "".join(random.choices(string.ascii_lowercase, k=8))


def random_email():
    return f"{random_username()}@example.com"


db: Session = SessionLocal()

store_products = db.query(store_product_model.StoreProduct).all()
store_product_ids = [p.id for p in store_products]

if len(store_product_ids) < 100:
    raise Exception("At least 100 store products are required.")

for i in range(NUM_FAMILIES):
    users = []
    for _ in range(random.randint(3, 4)):
        user = users_model.User(
            username=random_username(),
            email=random_email(),
            hashed_password=hash_password("password"),
            family_id=None,
        )
        db.add(user)
        db.flush()
        users.append(user)

    family = family_model.Family(name=f"Family_{i}", owner_id=users[0].id)
    db.add(family)
    db.flush()

    for user in users:
        user.family_id = family.id
    db.commit()

    for _ in range(random.randint(MIN_PURCHASES, MAX_PURCHASES)):
        purchase = purchase_model.Purchase(
            family_id=family.id, purchased_at=datetime.now()
        )
        db.add(purchase)
        db.flush()

        for pid in random.sample(
            store_product_ids,
            k=random.randint(MIN_ITEMS_PER_PURCHASE, MAX_ITEMS_PER_PURCHASE),
        ):
            db.add(
                purchase_model.PurchaseItem(
                    purchase_id=purchase.id,
                    product_id=pid,
                    quantity=random.randint(1, 5),
                )
            )

    db.commit()

db.close()
print("completed")
