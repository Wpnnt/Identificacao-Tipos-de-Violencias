from experta import *
from .facts import ViolenceRelact
from .classifier import classify_by_mapping


class ViolenceRules(KnowledgeEngine):  # ✅ Certifique-se de herdar de KnowledgeEngine
    @Rule(ViolenceRelact(action_type=MATCH.action, context=MATCH.context, target=MATCH.target))
    def classify_violence(self, action, context, target):
        user_input = {
            "action_type": action,
            "context": context,
            "target": target
        }

        results = classify_by_mapping(user_input)
        if results:
            for result in results:
                self.add_results(result)  # ✅ certifique-se que self.add_results está implementado