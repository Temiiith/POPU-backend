from sqlalchemy import text

from app.core.database import engine


print("Testing Supabase connection...")

with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print("Database response:", result.scalar())

print("Supabase connection successful!")