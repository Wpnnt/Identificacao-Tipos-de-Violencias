import sys
import os
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar apenas o motor de regras sem depender diretamente das classes experta
from engine.rules import ViolenceRules
from engine.facts import (
    TextRelato, KeywordFact, ViolenceBehavior, ContextFact, FrequencyFact,
    TargetFact, RelationshipFact, ImpactFact, ViolenceClassification,
    AnalysisResult
)
from engine.expert_system import ExpertSystem
from engine.text_processor import TextProcessor


class TestViolenceRules(unittest.TestCase):
    """Testes para o motor de regras ViolenceRules."""
    
    def setUp(self):
        """Configura o ambiente de teste."""
        self.engine = ViolenceRules()
        self.engine.reset()  # Resetar o motor antes de cada teste
    
    def test_initial_facts(self):
        """Testa se os fatos iniciais são criados corretamente."""
        self.engine.reset()
        self.engine.run(steps=1)  # Executar apenas o primeiro ciclo
        
        # Verificar se o fato engine_ready foi criado
        facts = list(self.engine.facts.values())
        self.assertTrue(any(fact.get('engine_ready', False) for fact in facts), 
                        "O fato 'engine_ready' não foi criado")
    
    def test_interrupcoes_constantes_detection(self):
        """Testa se a regra de interrupções constantes é ativada corretamente."""
        # Declarar fatos necessários para ativar a regra
        self.engine.declare(ViolenceBehavior(behavior_type="interrupcao"))
        self.engine.declare(FrequencyFact(value="repetidamente"))
        
        # Executar o motor
        self.engine.run()
        
        # Verificar se a classificação foi criada
        classifications = []
        for fact_id in self.engine.get_matching_facts(ViolenceClassification):
            fact = self.engine.facts[fact_id]
            classifications.append({
                'violence_type': fact['violence_type'],
                'subtype': fact['subtype']
            })
        
        self.assertTrue(any(c['violence_type'] == "microagressoes" and 
                          c['subtype'] == "interrupcoes_constantes" 
                          for c in classifications),
                      "Microagressão do tipo interrupções constantes não foi detectada")
    
    def test_discriminacao_genero_detection(self):
        """Testa se a regra de discriminação de gênero é ativada corretamente."""
        # Declarar fatos para discriminação flagrante
        self.engine.declare(ViolenceBehavior(behavior_type="exclusao"))
        self.engine.declare(TargetFact(characteristic="genero"))
        
        # Executar o motor
        self.engine.run()
        
        # Verificar se a classificação foi criada
        classifications = []
        for fact_id in self.engine.get_matching_facts(ViolenceClassification):
            fact = self.engine.facts[fact_id]
            classifications.append({
                'violence_type': fact['violence_type'],
                'subtype': fact['subtype']
            })
        
        self.assertTrue(any(c['violence_type'] == "discriminacao_genero" and 
                          c['subtype'] == "discriminacao_flagrante" 
                          for c in classifications),
                      "Discriminação flagrante de gênero não foi detectada")
    
    def test_perseguicao_detection(self):
        """Testa se a regra de perseguição é ativada corretamente."""
        # Declarar fatos para perseguição com medo
        self.engine.declare(KeywordFact(category="action_type", keyword="perseguicao"))
        self.engine.declare(KeywordFact(category="impact", keyword="medo"))
        
        # Executar o motor
        self.engine.run()
        
        # Verificar se a classificação foi criada
        classifications = []
        for fact_id in self.engine.get_matching_facts(ViolenceClassification):
            fact = self.engine.facts[fact_id]
            classifications.append({
                'violence_type': fact['violence_type'],
                'subtype': fact['subtype']
            })
        
        self.assertTrue(any(c['violence_type'] == "perseguicao" for c in classifications),
                      "Perseguição não foi detectada")
    
    def test_multiple_violence_types(self):
        """Testa se múltiplos tipos de violência são detectados quando apropriado."""
        # Declarar fatos que devem ativar múltiplas regras
        self.engine.declare(KeywordFact(category="action_type", keyword="perseguicao"))
        self.engine.declare(KeywordFact(category="impact", keyword="medo"))
        self.engine.declare(KeywordFact(category="action_type", keyword="humilhacao"))
        self.engine.declare(KeywordFact(category="relationship", keyword="superior_hierarquico"))
        
        # Executar o motor
        self.engine.run()
        
        # Verificar se múltiplas classificações foram criadas
        classifications = []
        for fact_id in self.engine.get_matching_facts(ViolenceClassification):
            fact = self.engine.facts[fact_id]
            classifications.append({
                'violence_type': fact['violence_type'],
                'subtype': fact['subtype']
            })
        
        # Deve detectar pelo menos perseguição e abuso psicológico
        self.assertTrue(any(c['violence_type'] == "perseguicao" for c in classifications),
                      "Perseguição não foi detectada em cenário múltiplo")
        self.assertTrue(any(c['violence_type'] == "abuso_psicologico" for c in classifications),
                      "Abuso psicológico não foi detectado em cenário múltiplo")
        
        # Verificar se o resultado da análise indica múltiplos tipos
        results = []
        for fact_id in self.engine.get_matching_facts(AnalysisResult):
            result = self.engine.facts[fact_id]
            results.append(result)
        
        self.assertTrue(len(results) > 0, "Nenhum resultado de análise foi criado")
        if results:
            self.assertTrue(results[0]['multiple_types'], 
                          "O resultado não indicou múltiplos tipos de violência")
    
    def test_confidence_calculation(self):
        """Testa se os níveis de confiança são calculados corretamente."""
        # Adicionar pontuação alta para um tipo de violência
        self.engine.add_score("microagressoes", "interrupcoes_constantes", 30, ["Teste de confiança alta"])
        
        # Executar o motor
        self.engine.run()
        
        # Verificar o nível de confiança
        for fact_id in self.engine.get_matching_facts(ViolenceClassification):
            fact = self.engine.facts[fact_id]
            if fact['violence_type'] == "microagressoes" and fact['subtype'] == "interrupcoes_constantes":
                # Com pontuação 30, deve ter alta confiança
                self.assertGreater(fact['confidence_level'], 0.75, 
                                  "O nível de confiança não foi calculado corretamente")


class TestExpertSystemIntegration(unittest.TestCase):
    """Testes de integração para o ExpertSystem."""

    @patch('engine.expert_system.TextProcessor')  # Mocka o TextProcessor
    def test_analyze_text_integration(self, mock_text_processor_class):
        """Testa se o fluxo de análise de texto funciona corretamente."""

        # Mock do TextProcessor
        mock_text_processor = mock_text_processor_class.return_value
        mock_text_processor.create_experta_facts.return_value = [
            TextRelato(text="Teste", processed=True),
            KeywordFact(category="action_type", keyword="interrupcao"),
            KeywordFact(category="frequency", keyword="repetidamente")
        ]

        # Instanciar o ExpertSystem (com o TextProcessor mockado automaticamente)
        expert_system = ExpertSystem()

        # Substituir o motor de regras por um mock manualmente
        mock_engine = MagicMock()
        mock_engine.facts = {
            1: AnalysisResult(
                classifications=[
                    {'violence_type': 'microagressoes', 'subtype': 'interrupcoes_constantes'}
                ],
                primary_result={'violence_type': 'microagressoes', 'subtype': 'interrupcoes_constantes'},
                multiple_types=False,
                ambiguity_level=0.0
            )
        }
        expert_system.engine = mock_engine

        # Executar o método
        result = expert_system.analyze_text("Teste")

        # Verificações
        mock_text_processor.create_experta_facts.assert_called_once_with("Teste")
        mock_engine.reset.assert_called_once()
        mock_engine.run.assert_called_once()

        self.assertEqual(result['primary_result']['violence_type'], 'microagressoes')
        self.assertEqual(result['primary_result']['subtype'], 'interrupcoes_constantes')
        self.assertFalse(result['multiple_types'])


class TestRealWorldScenarios(unittest.TestCase):
    """Testes com cenários reais de relatos."""
    
    def setUp(self):
        """Configura o ambiente de teste."""
        self.engine = ViolenceRules()
    
    def test_interruption_scenario(self):
        """Testa um cenário de interrupções constantes."""
        # Criar fatos para um cenário de interrupções constantes em sala de aula
        facts = [
            TextRelato(text="Meu professor sempre me interrompe quando estou falando em sala de aula", processed=True),
            KeywordFact(category="action_type", keyword="interrupcao"),
            KeywordFact(category="frequency", keyword="continuamente"),
            KeywordFact(category="context", keyword="sala_aula"),
            KeywordFact(category="relationship", keyword="superior_hierarquico")
        ]
        
        # Resetar o motor e declarar os fatos
        self.engine.reset()
        for fact in facts:
            self.engine.declare(fact)
        
        # Executar o motor
        self.engine.run()
        
        # Verificar se a microagressão foi detectada
        detected = False
        for fact_id in self.engine.get_matching_facts(ViolenceClassification):
            fact = self.engine.facts[fact_id]
            if fact['violence_type'] == "microagressoes" and fact['subtype'] == "interrupcoes_constantes":
                detected = True
                break
        
        self.assertTrue(detected, "O cenário de interrupções constantes não foi detectado corretamente")
    
    def test_sexual_harassment_scenario(self):
        """Testa um cenário de assédio sexual."""
        # Criar fatos para um cenário de assédio sexual
        facts = [
            TextRelato(text="Um colega de trabalho faz constantemente comentários sobre meu corpo", processed=True),
            KeywordFact(category="action_type", keyword="natureza_sexual_nao_consentido"),
            KeywordFact(category="context", keyword="local_trabalho"),
            KeywordFact(category="impact", keyword="constrangimento")
        ]
        
        # Resetar o motor e declarar os fatos
        self.engine.reset()
        for fact in facts:
            self.engine.declare(fact)
        
        # Executar o motor
        self.engine.run()
        
        # Verificar se o assédio sexual foi detectado
        detected = False
        for fact_id in self.engine.get_matching_facts(ViolenceClassification):
            fact = self.engine.facts[fact_id]
            if fact['violence_type'] == "violencia_sexual" and fact['subtype'] == "assedio_sexual":
                detected = True
                break
        
        self.assertTrue(detected, "O cenário de assédio sexual não foi detectado corretamente")
    
    def test_gordofobia_scenario(self):
        """Testa um cenário de gordofobia."""
        # Criar fatos para um cenário de gordofobia
        facts = [
            TextRelato(text="Meus colegas fazem piadas sobre meu peso constantemente", processed=True),
            KeywordFact(category="action_type", keyword="piadas_sobre_peso"),
            KeywordFact(category="frequency", keyword="continuamente"),
            KeywordFact(category="target", keyword="peso_corporal"),
            KeywordFact(category="impact", keyword="constrangimento")
        ]
        
        # Resetar o motor e declarar os fatos
        self.engine.reset()
        for fact in facts:
            self.engine.declare(fact)
        
        # Executar o motor
        self.engine.run()
        
        # Verificar se a gordofobia foi detectada
        detected = False
        for fact_id in self.engine.get_matching_facts(ViolenceClassification):
            fact = self.engine.facts[fact_id]
            if fact['violence_type'] == "gordofobia" and fact['subtype'] == "discriminacao_direta":
                detected = True
                break
        
        self.assertTrue(detected, "O cenário de gordofobia não foi detectado corretamente")


if __name__ == "__main__":
    unittest.main()