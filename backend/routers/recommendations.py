from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.users import User
from backend.models.purchase import Purchase, PurchaseItem
from backend.models.cart import CartDB
from backend.models.store_product import StoreProduct
from backend.core.utils import get_current_user
from sqlalchemy import func
from collections import defaultdict, Counter
from math import exp
from datetime import datetime

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @router.get("/family")
# def get_family_recommendations(
#     db: Session = Depends(get_db),
#     user_id: int = Depends(get_current_user),
# ):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user or not user.family_id:
#         raise HTTPException(status_code=400, detail="User must belong to a family")

#     # Get product IDs currently in the cart (not purchased or deleted)
#     cart_product_ids = (
#         db.query(CartDB.store_product_id)
#         .filter(
#             CartDB.family_id == user.family_id,
#             CartDB.purchased == False,
#             CartDB.is_deleted == False,
#         )
#         .subquery()
#     )

#     # Top 10 previously purchased items not currently in the cart
#     top_purchased_ids = (
#         db.query(PurchaseItem.product_id, func.count(PurchaseItem.id).label("times"))
#         .join(Purchase)
#         .filter(Purchase.family_id == user.family_id)
#         .filter(~PurchaseItem.product_id.in_(cart_product_ids))
#         .group_by(PurchaseItem.product_id)
#         .order_by(func.count(PurchaseItem.id).desc())
#         .limit(10)
#         .all()
#     )

#     product_ids = [pid for pid, _ in top_purchased_ids]

#     recommended_products = (
#         db.query(StoreProduct).filter(StoreProduct.id.in_(product_ids)).all()
#     )

#     return recommended_products


@router.get("/family/")
def get_smart_family_recommendations(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.family_id:
        raise HTTPException(status_code=400, detail="User must belong to a family")
    now = datetime.now()
    cart_product_ids = {
        id
        for (id,) in db.query(CartDB.store_product_id)
        .filter(
            CartDB.family_id == user.family_id,
            CartDB.purchased == False,
            CartDB.is_deleted == False,
        )
        .all()
    }
    past_purchases = (
        db.query(PurchaseItem.product_id, Purchase.purchased_at)
        .join(Purchase)
        .filter(Purchase.family_id == user.family_id)
        .all()
    )
    product_stats = defaultdict(lambda: {"frequency": 0, "recent": None})
    for product_id, purchased_at in past_purchases:
        if product_id in cart_product_ids:
            continue
        product_stats[product_id]["frequency"] += 1
        if (
            product_stats[product_id]["recent"] is None
            or purchased_at > product_stats[product_id]["recent"]
        ):
            product_stats[product_id]["recent"] = purchased_at

    max_freq = max([v["frequency"] for v in product_stats.values()], default=1)
    family_product_map = defaultdict(set)
    product_to_families = defaultdict(set)
    all_fam_purchases = (
        db.query(Purchase.family_id, PurchaseItem.product_id).join(PurchaseItem).all()
    )
    for fam_id, prod_id in all_fam_purchases:
        if fam_id != user.family_id:
            family_product_map[fam_id].add(prod_id)
            product_to_families[prod_id].add(fam_id)

    my_products = {pid for pid, _ in past_purchases}
    similarity_scores = Counter()
    for fam_id, their_products in family_product_map.items():
        shared = my_products & their_products
        if not shared:
            continue
        for prod in their_products - my_products:
            similarity_scores[prod] += len(shared)

    max_sim = max(similarity_scores.values(), default=1)
    familiar_scores = {}
    for product_id, stats in product_stats.items():
        freq_score = stats["frequency"] / max_freq
        days_since = (now - stats["recent"]).days if stats["recent"] else 999
        recency_score = exp(-days_since / 30)
        cross_score = (
            similarity_scores[product_id] / max_sim
            if product_id in similarity_scores
            else 0
        )
        final_score = 0.5 * freq_score + 0.3 * recency_score + 0.2 * cross_score
        familiar_scores[product_id] = final_score

    new_scores = {}
    for pid, sim_score in similarity_scores.items():
        if pid in product_stats or pid in cart_product_ids:
            continue
        new_scores[pid] = sim_score / max_sim

    top_familiar = sorted(familiar_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    top_new = sorted(new_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    final_ids = []
    for pid, _ in top_familiar:
        final_ids.append(pid)
    for pid, _ in top_new:
        final_ids.append(pid)

    final_products = db.query(StoreProduct).filter(StoreProduct.id.in_(final_ids)).all()

    print("FINAL PRODUCTS ARE")
    print(final_products)
    return final_products
    # final_list = []
    # for pid in final_ids:
    #     product = final_products.get(pid)
    #     if not product:
    #         continue
    #     source = "familiar" if pid in familiar_scores else "new"
    #     final_list.append(
    #         {
    #             "id": product.id,
    #             "name": product.name,
    #             "price": product.price,
    #             "score": round(familiar_scores.get(pid, new_scores.get(pid, 0)), 4),
    #             "source": source,
    #             "bought_by_families": (
    #                 list(product_to_families.get(pid, [])) if source == "new" else []
    #             ),
    #         }
    #     )

    # return final_list


@router.get("/past")
def get_past_top_family_purchases(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.family_id:
        raise HTTPException(status_code=400, detail="User must belong to a family")
    top_purchased_ids = (
        db.query(PurchaseItem.product_id, func.count(PurchaseItem.id).label("times"))
        .join(Purchase)
        .filter(Purchase.family_id == user.family_id)
        .group_by(PurchaseItem.product_id)
        .order_by(func.count(PurchaseItem.id).desc())
        .limit(10)
        .all()
    )

    product_ids = [pid for pid, _ in top_purchased_ids]
    products = db.query(StoreProduct).filter(StoreProduct.id.in_(product_ids)).all()
    products.sort(key=lambda p: product_ids.index(p.id))

    return products
