import os

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

SOURCES = [
    {
        "nombre": "disnort",
        "base_url": os.getenv("DISNORT_BASE_URL"),
        "user": os.getenv("DISNORT_USER"),
        "password": os.getenv("DISNORT_PASSWORD"),
        "listas_precios": [5, 8, 9],
        "depositos_stock": [1],
    },
    {
        "nombre": "surbeb",
        "base_url": os.getenv("SURBEB_BASE_URL"),
        "user": os.getenv("SURBEB_USER"),
        "password": os.getenv("SURBEB_PASSWORD"),
        "listas_precios": [4, 5],
        "depositos_stock": [1],
    },
]