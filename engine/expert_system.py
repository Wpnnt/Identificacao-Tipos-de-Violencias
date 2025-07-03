from typing import Dict, Any
from .rules import ViolenceRules
from .text_processor import TextProcessor
from .facts import AnalysisResult, ViolenceClassification

class ExpertSystem:
    """Sistema especialista que conecta processador de texto e motor de regras."""
    
    def __init__(self, api_key=None):
        """Inicializa o sistema com processador de texto e motor de regras."""
        self.text_processor = TextProcessor(api_key=api_key)
        self.engine = ViolenceRules()
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analisa um texto livre e retorna resultados estruturados.
        """
        # 1. Reiniciar o motor para garantir um estado limpo
        self.engine.reset()
        
        # 2. Processar texto e obter fatos compatíveis com Experta
        facts = self.text_processor.create_experta_facts(text)
        
        # 3. Inserir fatos no motor
        for fact in facts:
            self.engine.declare(fact)
        
        # 4. Executar o método de debug para verificar fatos
        self.engine.debug_facts()
        
        # 5. Executar o motor (que já consolida os resultados no final)
        self.engine.run()
        
        # 6. Coletar resultados
        results = self._collect_results()
        
        return results

    def _collect_results(self) -> Dict[str, Any]:
        """Coleta resultados do motor após execução."""
        results = {
            "classifications": [],
            "primary_result": {"violence_type": "", "subtype": ""},
            "multiple_types": False
        }
        
        # Buscar resultado da análise
        for fact in self.engine.facts.values():
            if isinstance(fact, AnalysisResult):
                results["classifications"] = getattr(fact, "classifications", [])
                
                # Atualizar primary_result se disponível
                primary_result = getattr(fact, "primary_result", None)
                if primary_result is not None:
                    results["primary_result"] = primary_result
                
                results["multiple_types"] = getattr(fact, "multiple_types", False)
                break
        
        # Se não encontrou AnalysisResult ou classifications está vazio, busque diretamente ViolenceClassification
        if not results["classifications"]:
            classifications = []
            for fact_id in self.engine.get_matching_facts(ViolenceClassification):
                fact = self.engine.facts[fact_id]
                classifications.append({
                    "violence_type": fact["violence_type"],
                    "subtype": fact["subtype"],
                    "explanation": self.engine.get_explanation(fact["violence_type"], fact["subtype"])
                })
            
            # Se encontrou classificações, use-as
            if classifications:
                results["classifications"] = classifications
                results["primary_result"] = classifications[0]
        
        return results