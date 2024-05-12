from psycopg_pool import ConnectionPool
import logging

logging.basicConfig(level=logging.INFO)
try:
    pool = ConnectionPool(
        "postgresql://postgres:1998@localhost:5432/booking",
        open=True,
        min_size=1,
        max_size=3
    )
    logging.info("Connection pool created successfully")
    
except Exception as e:
    logging.info(f"Error creating connection pool: {e}")



