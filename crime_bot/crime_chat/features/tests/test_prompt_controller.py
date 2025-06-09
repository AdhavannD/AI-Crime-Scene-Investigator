import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from features.controllers.prompt_controller import PromptController

class DummyService:
    def analyze_crime_scene(self, text):
        return f"Processed: {text}"

def test_process_description(monkeypatch):
    controller = PromptController()
    # Patch the service with a dummy
    controller.service = DummyService()
    result = controller.process_description("test crime scene")
    assert result == "Processed: test crime scene"
