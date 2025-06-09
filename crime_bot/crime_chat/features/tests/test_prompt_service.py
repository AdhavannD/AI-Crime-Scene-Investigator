import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from features.services.prompt_service import PromptService

class DummyRepo:
    def save_description(self, description):
        self.saved = description

class DummyAgent:
    def invoke(self, input_dict):
        return f"dummy-{list(input_dict.values())[0]}"

def test_analyze_crime_scene(monkeypatch):
    service = PromptService()
    # Patch repo and agents
    service.repo = DummyRepo()
    service._create_agent = lambda role: DummyAgent()
    result = service.analyze_crime_scene("scene text")
    assert "dummy-scene text" in result
    assert hasattr(service.repo, "saved") and service.repo.saved == "scene text"
