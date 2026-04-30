from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, init_db, Interaction, HCP
import schemas
from agent.graph import graph
from langchain_core.messages import HumanMessage
from typing import List

app = FastAPI(title="AI-First CRM HCP Module")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    init_db()

@app.post("/api/chat", response_model=schemas.ChatResponse)
def chat_endpoint(chat_request: schemas.ChatMessage):
    messages = [HumanMessage(content=chat_request.message)]
    result = graph.invoke({"messages": messages})
    response_msg = result["messages"][-1].content
    return {"response": response_msg}

@app.post("/api/interactions", response_model=schemas.InteractionResponse)
def create_interaction(interaction: schemas.InteractionCreate, db: Session = Depends(get_db)):
    db_hcp = db.query(HCP).filter(HCP.id == interaction.hcp_id).first()
    if not db_hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
    new_interaction = Interaction(**interaction.dict())
    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)
    return new_interaction

@app.get("/api/interactions", response_model=List[schemas.InteractionResponse])
def get_interactions(db: Session = Depends(get_db)):
    return db.query(Interaction).order_by(Interaction.date.desc()).all()

@app.get("/api/hcps", response_model=List[schemas.HCPResponse])
def get_hcps(db: Session = Depends(get_db)):
    return db.query(HCP).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
