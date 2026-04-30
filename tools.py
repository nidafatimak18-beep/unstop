from langchain_core.tools import tool
from database import SessionLocal, HCP, Interaction, ActionItem
from datetime import datetime

@tool
def log_interaction(hcp_id: int, notes: str, sentiment: str) -> str:
    """
    Logs a new interaction with an HCP.
    Args:
        hcp_id: The ID of the Healthcare Professional.
        notes: The discussion notes or summary.
        sentiment: The sentiment of the meeting (e.g., Positive, Neutral, Negative).
    """
    db = SessionLocal()
    try:
        new_interaction = Interaction(hcp_id=hcp_id, notes=notes, sentiment=sentiment)
        db.add(new_interaction)
        db.commit()
        db.refresh(new_interaction)
        return f"Interaction successfully logged with ID: {new_interaction.id}"
    except Exception as e:
        return f"Error logging interaction: {str(e)}"
    finally:
        db.close()

@tool
def edit_interaction(interaction_id: int, updated_notes: str, updated_sentiment: str) -> str:
    """
    Edits an existing interaction log.
    Args:
        interaction_id: The ID of the interaction to update.
        updated_notes: The new notes.
        updated_sentiment: The new sentiment.
    """
    db = SessionLocal()
    try:
        interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        if not interaction:
            return f"Interaction with ID {interaction_id} not found."
        interaction.notes = updated_notes
        if updated_sentiment:
            interaction.sentiment = updated_sentiment
        db.commit()
        return f"Interaction {interaction_id} updated successfully."
    except Exception as e:
        return f"Error editing interaction: {str(e)}"
    finally:
        db.close()

@tool
def get_hcp_details(hcp_name: str) -> str:
    """
    Retrieves details of a Healthcare Professional by their name.
    Args:
        hcp_name: The name or partial name of the HCP.
    """
    db = SessionLocal()
    try:
        hcp = db.query(HCP).filter(HCP.name.ilike(f"%{hcp_name}%")).first()
        if not hcp:
            return f"No HCP found matching '{hcp_name}'."
        return f"Found HCP: ID={hcp.id}, Name={hcp.name}, Specialty={hcp.specialty}, Hospital={hcp.hospital}"
    finally:
        db.close()

@tool
def get_past_interactions(hcp_id: int) -> str:
    """
    Retrieves the past interactions logged for a specific HCP.
    Args:
        hcp_id: The ID of the Healthcare Professional.
    """
    db = SessionLocal()
    try:
        interactions = db.query(Interaction).filter(Interaction.hcp_id == hcp_id).order_by(Interaction.date.desc()).limit(5).all()
        if not interactions:
            return f"No past interactions found for HCP ID {hcp_id}."
        res = [f"ID: {i.id}, Date: {i.date}, Notes: {i.notes}, Sentiment: {i.sentiment}" for i in interactions]
        return "\n".join(res)
    finally:
        db.close()

@tool
def schedule_follow_up(interaction_id: int, description: str) -> str:
    """
    Schedules a follow-up action item linked to a specific interaction.
    Args:
        interaction_id: The ID of the interaction.
        description: A brief description of the follow-up task.
    """
    db = SessionLocal()
    try:
        new_action = ActionItem(interaction_id=interaction_id, description=description)
        db.add(new_action)
        db.commit()
        return f"Follow-up scheduled successfully: '{description}'"
    except Exception as e:
        return f"Error scheduling follow up: {str(e)}"
    finally:
        db.close()

agent_tools = [
    log_interaction,
    edit_interaction,
    get_hcp_details,
    get_past_interactions,
    schedule_follow_up
]
