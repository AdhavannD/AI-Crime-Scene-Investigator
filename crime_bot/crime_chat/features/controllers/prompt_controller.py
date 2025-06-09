from features.services.prompt_service import PromptService

class PromptController:
    def __init__(self):
        self.service = PromptService()

    def process_description(self, text: str):
        return self.service.analyze_crime_scene(text)
