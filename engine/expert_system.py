from experta import KnowledgeEngine
from .rules import *

class ExpertSystem(ViolenceRules, KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.results = []

    def add_results(self, result):
        self.results.append(result)

    pass
