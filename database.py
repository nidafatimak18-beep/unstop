from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime
import os

DATABASE_URL = "sqlite:///./crm.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class HCP(Base):
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specialty = Column(String)
    hospital = Column(String)
    contact_info = Column(String)

    interactions = relationship("Interaction", back_populates="hcp")

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    notes = Column(Text)
    sentiment = Column(String)

    hcp = relationship("HCP", back_populates="interactions")
    action_items = relationship("ActionItem", back_populates="interaction")

class ActionItem(Base):
    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id"))
    description = Column(String)
    due_date = Column(DateTime, nullable=True)
    status = Column(String, default="Pending")

    interaction = relationship("Interaction", back_populates="action_items")

def init_db():
    Base.metadata.create_all(bind=engine)
    # Add a dummy HCP for testing
    db = SessionLocal()
    if not db.query(HCP).first():
        dummy_hcp = HCP(name="Dr. Smith", specialty="Cardiology", hospital="General Hospital", contact_info="smith@hospital.com")
        db.add(dummy_hcp)
        db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
