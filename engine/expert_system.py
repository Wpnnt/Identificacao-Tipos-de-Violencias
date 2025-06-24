from experta import KnowledgeEngine
from .rules import ViolenceRules

class ExpertSystem(ViolenceRules, KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.results = []

    def add_results(self, resultado):
        self.results.append(resultado)

    pass