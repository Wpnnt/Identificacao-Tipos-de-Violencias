from experta import Rule
from .facts import ViolenceRelact

class ViolenceRules:

    @Rule(ViolenceRelact(action_type="piada", context="trabalho", target="mulher"))
    def gender_moral_harassment(self):
        self.add_results("Assédio moral de gênero")

    @Rule(ViolenceRelact(action_type="comentario", context="ambiente público", target="minorias"))
    def microagression(self):
        self.add_results("Microagressão")