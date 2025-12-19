from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session, joinedload
from common import models, database #
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

app = FastAPI(title="Pricely Discovery Service")

# Enable CORS for Mobile App access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/v1/catalog/nearby")
def search_products(
    search: Optional[str] = Query(None), 
    db: Session = Depends(database.get_db)
):
    """
    Returns a list of products joined with their shop details.
    If search is empty, it returns all items.
    """
    query = db.query(models.Inventory).options(joinedload(models.Inventory.shop))
    
    if search:
        query = query.filter(models.Inventory.name.contains(search))
    
    items = query.all()
    
    # Flattening the joined structure for the Mobile App
    return [
        {
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "mrp": item.mrp,
            "unit": item.unit,
            "category": item.category,
            "sub_category": item.sub_category,
            "shop_id": item.shop_id,
            "shop_name": item.shop.name,
            "latitude": item.shop.latitude,
            "longitude": item.shop.longitude,
            "mobile_number": item.shop.mobile_number,
            "rating": item.shop.rating
        } for item in items
    ]

@app.get("/api/v1/shops/{shop_id}/inventory")
def get_shop_inventory(shop_id: str, db: Session = Depends(database.get_db)):
    """
    Returns all items belonging to a specific shop.
    Used by the Vendor App to show the owner their stock.
    """
    items = db.query(models.Inventory).filter(models.Inventory.shop_id == shop_id).all()
    return items