class CrimeRepository:
    def __init__(self):
        self.storage = []

    def save_description(self, description: str):
        self.storage.append(description)

    def get_all_descriptions(self):
        return self.storage
