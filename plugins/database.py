# database.py
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Role(Base):
    __tablename__ = "roles"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, unique=True, index=True)

class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String, unique=True, index=True)
    password = sa.Column(sa.String)
    full_name = sa.Column(sa.String)
    role_id = sa.Column(sa.Integer, sa.ForeignKey("roles.id"))

class Category(Base):
    __tablename__ = "categories"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, unique=True, index=True)
    parameter = sa.Column(sa.String, nullable=True)
    unit = sa.Column(sa.String)

class Item(Base):
    __tablename__ = "items"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, index=True)
    category_id = sa.Column(sa.Integer, sa.ForeignKey("categories.id"))
    parameter_value = sa.Column(sa.String)
    unit = sa.Column(sa.String)
    cost_price = sa.Column(sa.Integer)
    selling_price = sa.Column(sa.Integer)
    image_id = sa.Column(sa.String, nullable=True)

def get_db_sessionmaker(db_path: str):
    engine = sa.create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(bind=engine)  # Создаем таблицы при инициализации
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)