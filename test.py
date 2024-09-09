import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import os

DATABASE_URL = "postgresql+psycopg2://inventory_data_4oji_user:TO9HnXjkRbckWr54AByc2bbSs1pnMi9X@dpg-crfaivlsvqrc73f61ll0-a.oregon-postgres.render.com:5432/inventory_data_4oji"
# engine = create_engine(DATABASE_URL)
# DATABASE_URL = "postgresql+psycopg2://postgres:1@localhost/my_inventory"
engine = create_engine(DATABASE_URL)

def export_thu_chi():
    today_date = datetime.now().strftime("%Y-%m-%d")
    query = text("SELECT * FROM thu_chi WHERE date = :today_date")
    df = pd.read_sql_query(query, engine, params={"today_date": today_date})

    file_path = f"data/thu_chi/thu_chi_{today_date}.xlsx"

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_excel(file_path, index=False)

def export_hoa_binh():
    today_date = datetime.now().strftime("%Y-%m-%d")
    query = text("SELECT * FROM hoa_binh WHERE date = :today_date")
    df = pd.read_sql_query(query, engine, params={"today_date": today_date})

    file_path = f"data/hoa_binh/hoa_binh_{today_date}.xlsx"

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_excel(file_path, index=False)

def export_deo():
    today_date = datetime.now().strftime("%Y-%m-%d")
    query = text("SELECT * FROM deo WHERE date = :today_date")
    df = pd.read_sql_query(query, engine, params={"today_date": today_date})

    file_path = f"data/deo/deo_{today_date}.xlsx"

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_excel(file_path, index=False)

export_thu_chi()
export_hoa_binh()
export_deo()
