from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import database as db
import ai_utils
import datetime
import json

app = FastAPI()

# Setup Templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency
def get_db():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.on_event("startup")
def startup():
    db.init_db()

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, session: Session = Depends(get_db)):
    targets_count = session.query(db.Target).count()
    templates_count = session.query(db.Template).count()
    campaigns_count = session.query(db.Campaign).count()
    clicks_count = session.query(db.Click).count()
    
    # Recent clicks
    recent_clicks = session.query(db.Click).order_by(db.Click.timestamp.desc()).limit(5).all()
    
    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={
            "targets_count": targets_count,
            "templates_count": templates_count,
            "campaigns_count": campaigns_count,
            "clicks_count": clicks_count,
            "recent_clicks": recent_clicks
        }
    )

@app.get("/targets", response_class=HTMLResponse)
async def list_targets(request: Request, session: Session = Depends(get_db)):
    targets = session.query(db.Target).all()
    return templates.TemplateResponse(request=request, name="targets.html", context={"targets": targets})

@app.post("/targets")
async def add_target(email: str = Form(...), name: str = Form(...), session: Session = Depends(get_db)):
    new_target = db.Target(email=email, name=name)
    session.add(new_target)
    session.commit()
    return RedirectResponse(url="/targets", status_code=303)

@app.post("/targets/delete/{target_id}")
async def delete_target(target_id: int, session: Session = Depends(get_db)):
    target = session.query(db.Target).filter(db.Target.id == target_id).first()
    if target:
        # Get all campaigns associated with this target
        campaigns = session.query(db.Campaign).filter(db.Campaign.target_id == target_id).all()
        campaign_ids = [c.id for c in campaigns]
        
        if campaign_ids:
            # Delete associated clicks first
            session.query(db.Click).filter(db.Click.campaign_id.in_(campaign_ids)).delete(synchronize_session=False)
            # Delete associated campaigns
            session.query(db.Campaign).filter(db.Campaign.target_id == target_id).delete(synchronize_session=False)
            
        session.delete(target)
        session.commit()
    return RedirectResponse(url="/targets", status_code=303)

@app.get("/templates", response_class=HTMLResponse)
async def list_templates(request: Request, session: Session = Depends(get_db)):
    all_templates = session.query(db.Template).all()
    return templates.TemplateResponse(request=request, name="templates.html", context={"templates": all_templates})

@app.post("/templates/delete/{template_id}")
async def delete_template(template_id: int, session: Session = Depends(get_db)):
    template = session.query(db.Template).filter(db.Template.id == template_id).first()
    if template:
        # Get all campaigns associated with this template
        campaigns = session.query(db.Campaign).filter(db.Campaign.template_id == template_id).all()
        campaign_ids = [c.id for c in campaigns]
        
        if campaign_ids:
            # Delete associated clicks first
            session.query(db.Click).filter(db.Click.campaign_id.in_(campaign_ids)).delete(synchronize_session=False)
            # Delete associated campaigns
            session.query(db.Campaign).filter(db.Campaign.template_id == template_id).delete(synchronize_session=False)
            
        session.delete(template)
        session.commit()
    return RedirectResponse(url="/templates", status_code=303)

@app.post("/templates/generate")
async def generate_template(theme: str = Form(...), session: Session = Depends(get_db)):
    ai_resp = ai_utils.generate_phishing_template(theme)
    analysis_json = json.dumps(ai_resp.get("red_flags", []))
    new_template = db.Template(
        subject=ai_resp["subject"], 
        body_content=ai_resp["body"],
        analysis=analysis_json
    )
    session.add(new_template)
    session.commit()
    return RedirectResponse(url="/templates", status_code=303)

@app.get("/campaigns", response_class=HTMLResponse)
async def list_campaigns(request: Request, session: Session = Depends(get_db)):
    campaigns = session.query(db.Campaign).all()
    targets = session.query(db.Target).all()
    all_templates = session.query(db.Template).all()
    
    # Process campaigns to include the actual "inbox" view with [LINK] replaced
    processed_campaigns = []
    for c in campaigns:
        # Create a preview of the email with the actual tracking link
        tracking_url = f"http://localhost:8000/track/{c.id}"
        full_email_body = c.template.body_content.replace("[LINK]", tracking_url)
        
        red_flags = []
        if c.template and c.template.analysis:
            try:
                red_flags = json.loads(c.template.analysis)
            except json.JSONDecodeError:
                pass

        processed_campaigns.append({
            "id": c.id,
            "target": c.target,
            "template": c.template,
            "status": c.status,
            "full_body": full_email_body,
            "tracking_url": tracking_url,
            "red_flags": red_flags
        })

    return templates.TemplateResponse(request=request, name="campaigns.html", context={
        "campaigns": processed_campaigns,
        "targets": targets,
        "templates": all_templates
    })

@app.post("/campaigns/launch")
async def launch_campaign(target_id: int = Form(...), template_id: int = Form(...), session: Session = Depends(get_db)):
    new_campaign = db.Campaign(target_id=target_id, template_id=template_id, status="Sent", sent_at=datetime.datetime.utcnow())
    session.add(new_campaign)
    session.commit()
    return RedirectResponse(url="/campaigns", status_code=303)

@app.post("/campaigns/delete/{campaign_id}")
async def delete_campaign(campaign_id: int, session: Session = Depends(get_db)):
    campaign = session.query(db.Campaign).filter(db.Campaign.id == campaign_id).first()
    if campaign:
        # Delete associated clicks first
        session.query(db.Click).filter(db.Click.campaign_id == campaign_id).delete(synchronize_session=False)
        session.delete(campaign)
        session.commit()
    return RedirectResponse(url="/campaigns", status_code=303)

@app.get("/track/{campaign_id}")
async def track_click(campaign_id: int, request: Request, session: Session = Depends(get_db)):
    campaign = session.query(db.Campaign).filter(db.Campaign.id == campaign_id).first()
    if campaign:
        new_click = db.Click(
            campaign_id=campaign_id,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
        session.add(new_click)
        session.commit()
        return RedirectResponse(url=f"/success/{campaign_id}")
    return RedirectResponse(url="/")

@app.get("/success/{campaign_id}", response_class=HTMLResponse)
async def success_page(campaign_id: int, request: Request, session: Session = Depends(get_db)):
    campaign = session.query(db.Campaign).filter(db.Campaign.id == campaign_id).first()
    red_flags = []
    if campaign and campaign.template and campaign.template.analysis:
        try:
            red_flags = json.loads(campaign.template.analysis)
        except json.JSONDecodeError:
            pass
    return templates.TemplateResponse(request=request, name="success.html", context={"campaign": campaign, "red_flags": red_flags})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
