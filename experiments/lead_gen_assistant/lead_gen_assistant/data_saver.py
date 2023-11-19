import json


class DataSaver:
    """Save data however you need to"""

    def __init__(self):
        pass

    def save_name(self, name: str) -> str:
        """Save the result returned by GPT"""
        print(f"NAME: {name}")
        return json.dumps({"success": True})

    def save_email(self, email: str) -> str:
        """Save the result returned by GPT"""
        print(f"EMAIL: {email}")
        return json.dumps({"success": True})

    def save_phone_number(self, phone_number: str) -> str:
        """Save the result returned by GPT"""
        print(f"PHONE: {phone_number}")
        return json.dumps({"success": True})

    def save_budget(self, budget: int) -> str:
        """Save the result returned by GPT"""
        print(f"BUDGET: {budget}")
        return json.dumps({"success": True})

    def save_investment_goal(self, investment_goal: str) -> str:
        """Save the result returned by GPT"""
        print(f"GOAL: {investment_goal}")
        return json.dumps({"success": True})

    def save_property_type(self, property_type: str) -> str:
        """Save the result returned by GPT"""
        print(f"PROPERTY TYPE: {property_type}")
        return json.dumps({"success": True})

    def save_property_count(self, property_count: int) -> str:
        """Save the result returned by GPT"""
        print(f"PROPERTY COUNT: {property_count}")
        return json.dumps({"success": True})

    def save_referral_source(self, referral_source: str) -> str:
        """Save the result returned by GPT"""
        print(f"REFERRAL SOURCE: {referral_source}")
        return json.dumps({"success": True})

    def save_referrer_name(self, referrer_name: str) -> str:
        """Save the result returned by GPT"""
        print(f"REFERRER NAME: {referrer_name}")
        return json.dumps({"success": True})
