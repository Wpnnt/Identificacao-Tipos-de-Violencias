from experta import KnowledgeEngine
from .rules import RegrasViolencia

class SistemaEspecialista(RegrasViolencia, KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.results = []

    def add_results(self, resultado):
        self.results.append(resultado)



    pass