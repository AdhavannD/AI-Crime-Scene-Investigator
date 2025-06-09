import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from streamlit_app import PromptController

def test_streamlit_app_controller():
    controller = PromptController()
    assert hasattr(controller, "process_description")
