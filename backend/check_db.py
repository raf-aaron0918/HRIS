from app.core.config import settings
from sqlalchemy import create_engine, text

print('DATABASE_URL_SET=', bool(settings.database_url))
print('DATABASE_URL=', settings.database_url)
engine = create_engine(settings.database_url)
with engine.connect() as conn:
    print('VERSION=', conn.execute(text('select version()')).scalar())
    print('DATABASE=', conn.execute(text('select current_database()')).scalar())
