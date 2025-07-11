import os
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Numeric,
)
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

load_dotenv()

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL environment variable not set. Please create a .env file with the database URL.")

engine = create_engine(database_url, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class Car(Base):
    __tablename__ = "cars"

    # Using modern SQLAlchemy 2.0 syntax with type hints for better static analysis and clarity.
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    brand: Mapped[str] = mapped_column(String(50), index=True)
    model: Mapped[str] = mapped_column(String(50))
    year: Mapped[int] = mapped_column(index=True)
    engine: Mapped[str] = mapped_column(String(10))
    fuel_type: Mapped[str] = mapped_column(String(20))
    color: Mapped[str] = mapped_column(String(30))
    mileage: Mapped[int] = mapped_column()
    doors: Mapped[int] = mapped_column()
    transmission: Mapped[str] = mapped_column(String(20))
    # Using Numeric for price is crucial for financial data to avoid floating point inaccuracies.
    price: Mapped[float] = mapped_column(Numeric(10, 2), index=True)
    license_plate: Mapped[str] = mapped_column(String(10), unique=True, nullable=True)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}(id={self.id}, brand={self.brand!r}, model={self.model!r}, "
            f"year={self.year}, price={self.price})>"
        )
