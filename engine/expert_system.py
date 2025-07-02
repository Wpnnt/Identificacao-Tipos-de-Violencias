from typing import Dict, List, Any
from .rules import ViolenceRules
from .text_processor import TextProcessor
from .facts import AnalysisResult

class ExpertSystem:
    """Sistema especialista que conecta processador de texto e motor de regras."""
    
    def __init__(self, api_key=None):
        """Inicializa o sistema com processador de texto e motor de regras."""
        self.text_processor = TextProcessor(api_key=api_key)
        self.engine = ViolenceRules()
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analisa um texto livre e retorna resultados estruturados.
        
        Args:
            text: Texto do relato
            
        Returns:
            Dict: Resultados da análise
        """
        # 1. Processar texto e obter fatos compatíveis com Experta
        facts = self.text_processor.create_experta_facts(text)
        
        # 2. Reiniciar o motor
        self.engine.reset()
        
        # 3. Inserir fatos no motor
        for fact in facts:
            self.engine.declare(fact)
        
        # 4. Executar o motor
        self.engine.run()
        
        # 5. Coletar resultados
        results = self._collect_results()
        
        return results
    
    def _collect_results(self) -> Dict[str, Any]:
        """Coleta resultados do motor após execução."""
        results = {
            "classifications": [],
            "primary_result": None,
            "multiple_types": False,
            "ambiguity_level": 0.0
        }
        
        # Buscar resultado da análise
        for fact_id in self.engine.get_matching_facts(AnalysisResult):
            result = self.engine.facts[fact_id]
            results["classifications"] = result["classifications"]
            results["primary_result"] = result["primary_result"]
            results["multiple_types"] = result["multiple_types"]
            results["ambiguity_level"] = result["ambiguity_level"]
            break
        
        return results