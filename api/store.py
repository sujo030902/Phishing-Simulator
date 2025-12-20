from datetime import datetime

# Global In-Memory Store
# NOTE: This data resets on every serverless "cold start" or redeploy.
# Ideal for demos, NOT for production persistence.

class Store:
    def __init__(self):
        self.users = []
        self.targets = []
        self.campaigns = []
        self.templates = []
        self.results = []
        
        # Seed Data
        self._seed()

    def _seed(self):
        # Seed Templates
        self.templates.append({
            "id": 1,
            "name": "Urgent Password Reset",
            "subject": "ACTION REQUIRED: Password Expiry Notice",
            "body_content": "<p>Your password expires in 24 hours. <a href='http://phishing-link'>Click here to reset</a>.</p>",
            "created_by": 1,
            "is_ai_generated": False
        })
        self.templates.append({
            "id": 2,
            "name": "HR Policy Update",
            "subject": "New WFH Policy",
            "body_content": "<p>Please review the attached policy update regarding remote work. <a href='http://phishing-link'>View Document</a>.</p>",
            "created_by": 1,
            "is_ai_generated": False
        })
        
        # Seed Targets
        self.targets.append({
            "id": 1,
            "email": "employee@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "department": "Sales"
        })

    def get_all_templates(self):
        return self.templates

    def get_template(self, template_id):
        return next((t for t in self.templates if t["id"] == template_id), None)

    def add_template(self, template_data):
        new_id = len(self.templates) + 1
        template = {
            "id": new_id,
            "name": template_data.get("name", "Untitled"),
            "subject": template_data.get("subject", ""),
            "body_content": template_data.get("body_content") or template_data.get("body", ""),
            "is_ai_generated": template_data.get("is_ai_generated", False),
            "created_by": template_data.get("created_by")
        }
        self.templates.append(template)
        return template

    def delete_template(self, template_id):
        self.templates = [t for t in self.templates if t["id"] != template_id]
        # Cleanup campaigns using this template? Or keep them?
        # For simple demo, we won't cascade delete campaigns to avoid complex errors, 
        # but in production we should.

    def update_template(self, template_id, updates):
        template = next((t for t in self.templates if t["id"] == template_id), None)
        if not template:
            return None
            
        # Only allow updating specific fields
        if "name" in updates:
            template["name"] = updates["name"]
        if "subject" in updates:
            template["subject"] = updates["subject"]
        if "body_content" in updates:
            template["body_content"] = updates["body_content"]
            
        return template

    def get_all_targets(self):
        # Augment with history if needed, but keeping it simple for now
        # Ideally we join with results here
        targets_with_history = []
        for t in self.targets:
            t_copy = t.copy()
            # Find history
            history = [r for r in self.results if r["target_id"] == t["id"]]
            # We need to format history as frontend expects
            formatted_history = []
            for h in history:
                campaign = next((c for c in self.campaigns if c["id"] == h["campaign_id"]), None)
                template = self.get_template(campaign["template_id"]) if campaign else None
                
                status = "Sent"
                if h.get("clicked_link"): status = "Clicked"
                elif h.get("opened"): status = "Opened"
                
                formatted_history.append({
                    "result_id": h["id"],
                    "campaign_name": campaign["name"] if campaign else "Unknown",
                    "email_subject": template["subject"] if template else "Unknown",
                    "email_body": template["body_content"] if template else "",
                    "sent_at": h["sent_at"],
                    "status": status
                })
            t_copy["history"] = formatted_history
            targets_with_history.append(t_copy)
        return targets_with_history

    def add_target(self, target_data):
        # Check uniqueness
        if any(t["email"] == target_data["email"] for t in self.targets):
            raise ValueError("Email already exists")
            
        new_id = len(self.targets) + 1
        target = {
            "id": new_id,
            "email": target_data["email"],
            "first_name": target_data.get("first_name"),
            "last_name": target_data.get("last_name"),
            "department": target_data.get("department")
        }
        self.targets.append(target)
        return target

    def delete_target(self, target_id):
        self.targets = [t for t in self.targets if t["id"] != target_id]
        # Cleanup results
        self.results = [r for r in self.results if r["target_id"] != target_id]

    def get_all_campaigns(self):
        return self.campaigns

    def create_campaign(self, name, template_id):
        new_id = len(self.campaigns) + 1
        campaign = {
            "id": new_id,
            "name": name,
            "template_id": template_id,
            "status": "draft",
            "created_at": datetime.now().isoformat()
        }
        self.campaigns.append(campaign)
        return campaign

    def launch_campaign(self, campaign_id, target_ids=None):
        campaign = next((c for c in self.campaigns if c["id"] == campaign_id), None)
        if not campaign:
            raise ValueError("Campaign not found")
        
        campaign["status"] = "active"
        
        targets_to_fish = []
        if target_ids:
            targets_to_fish = [t for t in self.targets if t["id"] in target_ids]
        else:
            targets_to_fish = self.targets
            
        for t in targets_to_fish:
            new_result_id = len(self.results) + 1
            self.results.append({
                "id": new_result_id,
                "campaign_id": campaign_id,
                "target_id": t["id"],
                "sent_at": datetime.now().isoformat(),
                "opened": False,
                "clicked_link": False,
                "submitted_credentials": False
            })
            
        return len(targets_to_fish)

    def get_campaign_stats(self, campaign_id):
        campaign = next((c for c in self.campaigns if c["id"] == campaign_id), None)
        if not campaign:
            return None
            
        campaign_results = [r for r in self.results if r["campaign_id"] == campaign_id]
        
        return {
            "campaign": campaign["name"],
            "status": campaign["status"],
            "total_sent": len(campaign_results),
            "opened": sum(1 for r in campaign_results if r.get("opened")),
            "clicked": sum(1 for r in campaign_results if r.get("clicked_link")),
            "submitted": sum(1 for r in campaign_results if r.get("submitted_credentials"))
        }

    def delete_campaign(self, campaign_id):
        self.campaigns = [c for c in self.campaigns if c["id"] != campaign_id]
        self.results = [r for r in self.results if r["campaign_id"] != campaign_id]

    def track_action(self, result_id, action_type):
        result = next((r for r in self.results if r["id"] == result_id), None)
        if not result:
            return False
            
        if action_type == "open":
            result["opened"] = True
        elif action_type == "click":
            result["clicked_link"] = True
            result["opened"] = True # implied
            
        return True

# Singleton Instance
data_store = Store()
