import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from features.services import prompt_service

def test_import_prompt_service():
    assert hasattr(prompt_service, "PromptService")
    service = prompt_service.PromptService()
    assert hasattr(service, "analyze_crime_scene")
