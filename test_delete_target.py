from fastapi.testclient import TestClient
from main import app, get_db
import database as db
from sqlalchemy.orm import Session

client = TestClient(app, follow_redirects=False)

def test_delete_target():
    session = next(get_db())
    # Cleanup any existing test data
    existing = session.query(db.Target).filter(db.Target.email == "test@example.com").first()
    if existing:
        # Delete campaigns and clicks first
        campaigns = session.query(db.Campaign).filter(db.Campaign.target_id == existing.id).all()
        for c in campaigns:
            session.query(db.Click).filter(db.Click.campaign_id == c.id).delete()
            session.delete(c)
        session.delete(existing)
        session.commit()

    # 1. Add a target
    response = client.post("/targets", data={"name": "Test User", "email": "test@example.com"})
    assert response.status_code == 303
    
    # Verify it's in the DB
    session = next(get_db())
    target = session.query(db.Target).filter(db.Target.email == "test@example.com").first()
    assert target is not None
    target_id = target.id
    
    # 2. Add a template (needed for campaign)
    new_template = db.Template(subject="Test Subject", body_content="Test Body")
    session.add(new_template)
    session.commit()
    template_id = new_template.id
    
    # 3. Create a campaign for this target
    response = client.post("/campaigns/launch", data={"target_id": target_id, "template_id": template_id})
    assert response.status_code == 303
    
    campaign = session.query(db.Campaign).filter(db.Campaign.target_id == target_id).first()
    assert campaign is not None
    campaign_id = campaign.id
    
    # 4. Create a click for this campaign
    new_click = db.Click(campaign_id=campaign_id, ip_address="127.0.0.1", user_agent="TestAgent")
    session.add(new_click)
    session.commit()
    
    click = session.query(db.Click).filter(db.Click.campaign_id == campaign_id).first()
    assert click is not None
    
    # 5. Delete the target
    response = client.post(f"/targets/delete/{target_id}")
    assert response.status_code == 303
    
    # 6. Verify target is gone
    session = next(get_db()) # Refresh session
    target = session.query(db.Target).filter(db.Target.id == target_id).first()
    assert target is None
    
    # 7. Verify campaign is gone
    campaign = session.query(db.Campaign).filter(db.Campaign.target_id == target_id).first()
    assert campaign is None
    
    # 8. Verify click is gone
    click = session.query(db.Click).filter(db.Click.campaign_id == campaign_id).first()
    assert click is None
    
    print("Test passed!")

if __name__ == "__main__":
    test_delete_target()
