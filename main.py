from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from enum import Enum
from typing import List
from uuid import uuid4
from datetime import datetime

from sqlmodel import Session, select

import database, models

app = FastAPI(
    title="Papiprints Printing Service",
    description="Backend API for student printing orders",
    version="0.1.0",
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React dev server
        "http://localhost:5173",      # Vite dev server
        "http://127.0.0.1:5500",      # Live Server
        "http://127.0.0.1:8080",      # Vue dev server
        "*",                          # Allow all origins (development only!)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create tables on startup
@app.on_event("startup")
def on_startup():
    database.init_db()


# pricing constants (PHP per page)
PRICES = {
    models.PrintType.black_white: 2.0,
    models.PrintType.colored: 5.0,
    models.PrintType.photo: 20.0,
}


class OrderBase(BaseModel):
    user_id: str
    pages: int
    print_type: models.PrintType
    filename: str | None = None


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: str
    status: str = "pending"
    cost: float
    created_at: datetime


def calculate_cost(pages: int, print_type: models.PrintType) -> float:
    price = PRICES.get(print_type)
    return pages * price


def get_session():
    with database.get_session() as session:
        yield session


@app.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    """Create a new print order. Cost is calculated automatically."""
    cost = calculate_cost(order.pages, order.print_type)
    db_order = models.Order(
        user_id=order.user_id,
        pages=order.pages,
        print_type=order.print_type,
        filename=order.filename,
        cost=cost,
    )
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


@app.get("/orders", response_model=List[OrderResponse])
def list_orders(session: Session = Depends(get_session)):
    """Return all orders (for admins)."""
    orders = session.exec(select(models.Order)).all()
    return orders


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, session: Session = Depends(get_session)):
    order = session.get(models.Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.patch("/orders/{order_id}/status", response_model=OrderResponse)
def update_status(order_id: str, status: str, session: Session = Depends(get_session)):
    """Update a single order's status (e.g. pending -> completed)."""
    order = session.get(models.Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


@app.get("/users/{user_id}/orders", response_model=List[OrderResponse])
def get_user_orders(user_id: str, session: Session = Depends(get_session)):
    """Retrieve orders for a specific student."""
    orders = session.exec(
        select(models.Order).where(models.Order.user_id == user_id)
    ).all()
    return orders
