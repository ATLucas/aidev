import json


class DataSaver:
    def save_interests(self, interests: str) -> str:
        """Save reader's interests"""
        print(f"INTERESTS: {interests}\n")
        return json.dumps({"success": True})

    def save_industry(self, industry: str) -> str:
        """Save reader's industry"""
        print(f"INDUSTRY: {industry}\n")
        return json.dumps({"success": True})

    def save_occupation(self, occupation: str) -> str:
        """Save reader's occupation"""
        print(f"OCCUPATION: {occupation}\n")
        return json.dumps({"success": True})

    def save_coding_skill_level(self, coding_skill_level: str) -> str:
        """Save reader's coding skill level"""
        print(f"CODING SKILL LEVEL: {coding_skill_level}\n")
        return json.dumps({"success": True})

    def save_professional_goals(self, professional_goals: str) -> str:
        """Save reader's professional goals or challenges relating to AI"""
        print(f"PROFESSIONAL GOALS: {professional_goals}\n")
        return json.dumps({"success": True})

    def save_referral_source(self, referral_source: str) -> str:
        """Save how reader found the newsletter"""
        print(f"REFERRAL SOURCE: {referral_source}\n")
        return json.dumps({"success": True})

    def save_region_or_timezone(self, region_or_timezone: str) -> str:
        """Save reader's region or time zone"""
        print(f"REGION OR TIME ZONE: {region_or_timezone}\n")
        return json.dumps({"success": True})

    def save_feedback(self, feedback: str) -> str:
        """Save reader's feedback for the newsletter"""
        print(f"FEEDBACK: {feedback}\n")
        return json.dumps({"success": True})
