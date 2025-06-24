from experta import Rule
from .facts import ViolenceRelact

class ViolenceRules:

    @Rule(ViolenceRelact(action_type="piada", context="trabalho", target="mulher"))
    def gender_moral_harassment(self):
        self.add_results("Assédio moral de gênero")

    @Rule(ViolenceRelact(action_type="comentario", contex="ambiente publico", target="minorias", intencao="diminuir"))
    def microagression(self):
        self.add_results("Microagressão")