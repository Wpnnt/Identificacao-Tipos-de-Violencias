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
        
        # 4. Executar o motor (que já consolida os resultados no final)
        self.engine.run()
        
        # 5. Coletar resultados
        results = self._collect_results()
        
        return results

    def _collect_results(self) -> Dict[str, Any]:
        """Coleta resultados do motor após execução."""
        results = {
            "classifications": [],
            "primary_result": {"violence_type": "", "subtype": "", "confidence": 0.0},
            "multiple_types": False,
            "ambiguity_level": 0.0
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
                results["ambiguity_level"] = getattr(fact, "ambiguity_level", 0.0)
                break
        
        # Se não encontrou AnalysisResult ou classifications está vazio, busque diretamente ViolenceClassification
        if not results["classifications"]:
            classifications = []
            for fact_id in self.engine.get_matching_facts(ViolenceClassification):
                fact = self.engine.facts[fact_id]
                classifications.append({
                    "violence_type": fact["violence_type"],
                    "subtype": fact["subtype"],
                    "confidence": fact["confidence_level"],
                    "score": fact["score"],
                    "explanation": self.engine.get_explanation(fact["violence_type"], fact["subtype"])
                })
            
            # Se encontrou classificações, use-as
            if classifications:
                results["classifications"] = classifications
                
                # Determine a classificação principal
                primary = sorted(
                    classifications, 
                    key=lambda x: (x.get("score", 0), x.get("confidence", 0)),
                    reverse=True
                )[0]
                results["primary_result"] = primary
        
        return results