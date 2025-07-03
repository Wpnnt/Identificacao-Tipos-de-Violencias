import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from experta import Fact, Rule, KnowledgeEngine
from engine.facts import ViolenceBehavior, FrequencyFact

class SimpleEngine(KnowledgeEngine):
    @Rule(ViolenceBehavior(behavior_type="interrupcao"))
    def simple_rule_1(self):
        print("✅ REGRA 1 DISPAROU - comportamento de interrupção detectado!")
        
    @Rule(FrequencyFact(value="repetidamente"))
    def simple_rule_2(self):
        print("✅ REGRA 2 DISPAROU - frequência repetida detectada!")
        
    @Rule(
        ViolenceBehavior(behavior_type="interrupcao"),
        FrequencyFact(value="repetidamente")
    )
    def combined_rule(self):
        print("✅ REGRA COMBINADA DISPAROU - interrupção repetida detectada!")
        
print("🔄 Iniciando teste simples do Experta...")
engine = SimpleEngine()
engine.reset()

# Declarar fatos
print("\n📌 Declarando fatos:")
behavior = ViolenceBehavior(behavior_type="interrupcao")
engine.declare(behavior)
print(f"- Declarado: ViolenceBehavior(behavior_type='interrupcao')")

freq = FrequencyFact(value="repetidamente")
engine.declare(freq)
print(f"- Declarado: FrequencyFact(value='repetidamente')")

# Executar
print("\n🔄 Executando motor:")
engine.run()

print("\n✅ Teste concluído")