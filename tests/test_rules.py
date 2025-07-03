import sys
import os

# Adicionar o diretório raiz ao path para importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.rules import ViolenceRules
from engine.facts import (
    ViolenceBehavior, 
    FrequencyFact, 
    ContextFact, 
    ImpactFact, 
    TargetFact, 
    RelationshipFact, 
    ViolenceClassification,
    AnalysisResult
)

def test_interrupcoes_constantes():
    """Testa se o motor identifica corretamente interrupções constantes."""
    print("\n===== TESTE DE INTERRUPÇÕES CONSTANTES =====")
    
    # Instanciar o motor de regras
    engine = ViolenceRules()
    engine.reset()
    
    # Criar e declarar os fatos necessários
    engine.declare(ViolenceBehavior(behavior_type="interrupcao"))
    engine.declare(FrequencyFact(value="repetidamente"))
    
    # Executar o motor
    print("🔄 Executando motor de regras...")
    engine.run()
    
    # Verificar os resultados
    print("\n✅ Resultados:")
    found_classification = False
    for fact_id in engine.facts:
        fact = engine.facts[fact_id]
        if isinstance(fact, ViolenceClassification):
            found_classification = True
            print(f"- Tipo de violência: {fact['violence_type']}")
            print(f"- Subtipo: {fact['subtype']}")
            print(f"- Pontuação: {fact['score']}")
            print(f"- Confiança: {fact['confidence_level']:.2f}")
    
    if not found_classification:
        print("❌ Nenhuma classificação encontrada!")
        
    # Verificar o resultado consolidado
    for fact_id in engine.facts:
        fact = engine.facts[fact_id]
        if isinstance(fact, AnalysisResult):
            print("\n🔍 Análise final:")
            primary = fact["primary_result"]
            if primary:
                print(f"- Resultado principal: {primary.get('violence_type', '')} - {primary.get('subtype', '')}")
                print(f"- Confiança: {primary.get('confidence', 0):.2f}")
            else:
                print("- Nenhum resultado principal encontrado")
            
            print(f"- Múltiplos tipos: {fact['multiple_types']}")
            print(f"- Ambiguidade: {fact['ambiguity_level']:.2f}")
            
def test_assedio_sexual():
    """Testa se o motor identifica corretamente assédio sexual."""
    print("\n===== TESTE DE ASSÉDIO SEXUAL =====")
    
    # Instanciar o motor de regras
    engine = ViolenceRules()
    engine.reset()
    
    # Criar e declarar os fatos necessários
    engine.declare(ViolenceBehavior(behavior_type="natureza_sexual_nao_consentido"))
    engine.declare(ImpactFact(type="constrangimento"))
    engine.declare(ContextFact(location="local_trabalho"))
    
    # Executar o motor
    print("🔄 Executando motor de regras...")
    engine.run()
    
    # Verificar os resultados
    print("\n✅ Resultados:")
    found_classification = False
    for fact_id in engine.facts:
        fact = engine.facts[fact_id]
        if isinstance(fact, ViolenceClassification):
            found_classification = True
            print(f"- Tipo de violência: {fact['violence_type']}")
            print(f"- Subtipo: {fact['subtype']}")
            print(f"- Pontuação: {fact['score']}")
            print(f"- Confiança: {fact['confidence_level']:.2f}")
    
    if not found_classification:
        print("❌ Nenhuma classificação encontrada!")

def test_multiple_classifications():
    """Testa se o motor identifica múltiplos tipos de violência."""
    print("\n===== TESTE DE MÚLTIPLAS CLASSIFICAÇÕES =====")
    
    # Instanciar o motor de regras
    engine = ViolenceRules()
    engine.reset()
    
    # Declarar fatos para dois tipos diferentes de violência
    # Perseguição
    engine.declare(ViolenceBehavior(behavior_type="perseguicao"))
    engine.declare(ImpactFact(type="medo_inseguranca"))
    
    # Discriminação de gênero
    engine.declare(ViolenceBehavior(behavior_type="exclusao"))
    engine.declare(TargetFact(characteristic="genero"))
    
    # Executar o motor
    print("🔄 Executando motor de regras...")
    engine.run()
    
    # Verificar os resultados
    print("\n✅ Resultados:")
    classifications = []
    for fact_id in engine.facts:
        fact = engine.facts[fact_id]
        if isinstance(fact, ViolenceClassification):
            classifications.append(fact)
            print(f"- Tipo: {fact['violence_type']}, Subtipo: {fact['subtype']}, Score: {fact['score']}")
    
    print(f"\nTotal de classificações: {len(classifications)}")
    
    # Verificar o resultado consolidado
    for fact_id in engine.facts:
        fact = engine.facts[fact_id]
        if isinstance(fact, AnalysisResult):
            print("\n🔍 Análise final:")
            print(f"- Múltiplos tipos: {fact['multiple_types']}")
            print(f"- Ambiguidade: {fact['ambiguity_level']:.2f}")
            break

if __name__ == "__main__":
    # Executar os testes
    test_interrupcoes_constantes()
    test_assedio_sexual()
    test_multiple_classifications()