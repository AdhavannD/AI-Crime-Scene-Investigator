import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from features.controllers import prompt_controller

def test_import_prompt_controller():
    assert hasattr(prompt_controller, "PromptController")
    controller = prompt_controller.PromptController()
    assert hasattr(controller, "process_description")
