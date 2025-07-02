import os
from typing import Dict, List, Any
import json

from knowledge_base.keywords_dictionary import KEYWORDS_DICT, FIELDS_QUESTIONS
from utils.groq_integration import GroqAPI
from engine.classifier import classify_by_mapping
# Importar fatos do Experta para criar objetos compatíveis com o motor de regras
from engine.facts import (
    TextRelato, KeywordFact, ViolenceBehavior, ContextFact, FrequencyFact,
    TargetFact, RelationshipFact, ImpactFact, ViolenceClassification,
    create_facts_from_groq_response
)

class TextProcessor:
    """
    Processa texto livre do usuário para extrair fatos e disparar regras.
    """
    def __init__(self, api_key: str = None, 
                 model: str = "meta-llama/llama-4-scout-17b-16e-instruct"):

        self.api_key = api_key if api_key else os.environ.get("GROQ_API_KEY", "")
        self.model = model
        self.groq_api = GroqAPI(api_key=self.api_key, model=self.model)
        self.conversation_context = []

    def process_user_text(self, text: str) -> Dict[str, Any]:
        """
        Processa texto do usuário e retorna informações extraídas (para interface).
        """
        self.conversation_context.append({"role": "user", "content": text})
        prompt = self.groq_api.build_prompt(text, KEYWORDS_DICT)
        response = self.groq_api.send_request(prompt)

        keywords = response.get("identified_keywords", {})
        missing = response.get("missing_information", [])
        questions = response.get("follow_up_questions", [])

        critical_fields = ["action_type"]
        missing_critical = any(field in missing for field in critical_fields)

        facts = self._extract_facts_from_keywords(keywords)

        if missing_critical:
            return {
                "status": "incomplete",
                "identified_keywords": keywords,
                "missing_fields": missing,
                "questions": questions,
                "facts": facts
            }

        classifications = classify_by_mapping(facts)
        return {
            "status": "complete",
            "identified_keywords": keywords,
            "facts": facts,
            "classifications": classifications
        }

    # NOVO MÉTODO: Cria objetos Fact do Experta
    def create_experta_facts(self, text: str) -> List[Any]:
        """
        Cria fatos Experta a partir de um texto, para inserção no motor de regras.
        
        Args:
            text: Texto do relato
            
        Returns:
            List[Fact]: Lista de fatos para o motor Experta
        """
        print(f"\n🔍 Processando texto para criar fatos: {text[:100]}{'...' if len(text) > 100 else ''}")
        
        # Adicionar o TextRelato original
        facts = [TextRelato(text=text, processed=True)]
        
        try:
            # Extrair palavras-chave usando o Groq
            prompt = self.groq_api.build_prompt(text, KEYWORDS_DICT)
            response = self.groq_api.send_request(prompt)
            
            if "identified_keywords" in response and response["identified_keywords"]:
                print(f"✅ Palavras-chave identificadas: {json.dumps(response['identified_keywords'], indent=2)}")
                
                # Converter resposta em fatos Experta
                keyword_facts = create_facts_from_groq_response(response)
                facts.extend(keyword_facts)
                
                for fact in keyword_facts:
                    print(f"📌 Criado fato Experta: {fact}")
            else:
                print("⚠️ Nenhuma palavra-chave identificada no texto")
                # Caso não encontre palavras-chave, usar classificação direta
                # e criar fatos ViolenceClassification
                result = self._direct_classification(text)
                facts.extend(result)
        except Exception as e:
            print(f"❌ Erro ao processar texto: {str(e)}")
            # Usar classificação direta como fallback
            result = self._direct_classification(text)
            facts.extend(result)
        
        return facts
    
    def _direct_classification(self, text: str) -> List[Any]:
        """
        Realiza classificação direta e retorna fatos ViolenceClassification.
        
        Args:
            text: Texto para classificação
            
        Returns:
            List: Lista de fatos ViolenceClassification
        """
        print("🔄 Usando classificação direta do texto...")
        
        classifications = classify_by_mapping({"text": text})
        facts = []
        
        for c in classifications:
            fact = ViolenceClassification(
                violence_type=c["violence_type"],
                subtype=c.get("subtype"),
                score=c.get("score", 0),
                confidence_level=c.get("confidence", 0.0)
            )
            facts.append(fact)
            print(f"📌 Criado fato de classificação: {fact}")
        
        return facts

    def _process_followup(self, follow_up_text: str, previous_keywords: Dict, missing_fields: List[str]) -> Dict[str, Any]:
        """
        Processa resposta de follow-up para complementar informações.
        """
        self.conversation_context.append({"role": "user", "content": follow_up_text})
        prompt = self.groq_api.build_prompt(follow_up_text, KEYWORDS_DICT, is_follow_up=True, missing_fields=missing_fields)
        response = self.groq_api.send_request(prompt)

        combined_keywords = self._combine_keywords(previous_keywords, response.get("identified_keywords", {}))
        facts = self._extract_facts_from_keywords(combined_keywords)

        missing = response.get("missing_information", [])
        questions = response.get("follow_up_questions", [])
        missing_critical = any(field in missing for field in ["action_type"])

        if missing_critical:
            return {
                "status": "incomplete",
                "identified_keywords": combined_keywords,
                "missing_fields": missing,
                "questions": questions,
                "facts": facts
            }

        classifications = classify_by_mapping(facts)
        return {
            "status": "complete",
            "identified_keywords": combined_keywords,
            "facts": facts,
            "classifications": classifications
        }

    def _extract_facts_from_keywords(self, keywords: Dict) -> Dict:
        """
        Extrai fatos do dicionário de palavras-chave para o formato simplificado.
        """
        return {category: values[0] if values else None for category, values in keywords.items() if values}

    def _combine_keywords(self, previous: Dict, new: Dict) -> Dict:
        """
        Combina palavras-chave anteriores com novas.
        """
        result = previous.copy()
        for category, values in new.items():
            if category in result:
                result[category] = list(set(result[category] + values))
            else:
                result[category] = values
        return result
    
    def create_experta_facts(self, text: str) -> List[Any]:
        """
        Cria fatos Experta a partir de um texto, para inserção no motor de regras.
        
        Args:
            text: Texto do relato
            
        Returns:
            List[Fact]: Lista de fatos para o motor Experta
        """
        print(f"\n🔍 Processando texto para criar fatos: {text[:100]}{'...' if len(text) > 100 else ''}")
        
        # Adicionar o TextRelato original
        facts = [TextRelato(text=text, processed=True)]
        
        try:
            # Usar seu método existente para processar o texto
            result = self.process_user_text(text)
            
            # Criar fatos a partir das keywords identificadas
            if "identified_keywords" in result and result["identified_keywords"]:
                keywords = result["identified_keywords"]
                
                # Converter keywords em fatos Experta usando a função existente
                keyword_facts = create_facts_from_groq_response({"identified_keywords": keywords})
                facts.extend(keyword_facts)
                
                for fact in keyword_facts:
                    print(f"📌 Criado fato Experta: {fact}")
            
            # Se houver classificações diretas, adicione-as como ViolenceClassification
            if "classifications" in result and result["classifications"]:
                for c in result["classifications"]:
                    fact = ViolenceClassification(
                        violence_type=c["violence_type"],
                        subtype=c.get("subtype"),
                        score=c.get("score", 0),
                        confidence_level=c.get("confidence", 0.0)
                    )
                    facts.append(fact)
                    
        except Exception as e:
            print(f"❌ Erro ao processar texto: {str(e)}")
            # Usar classificação direta como fallback se disponível
            if hasattr(self, '_direct_classification'):
                facts.extend(self._direct_classification(text))
        
        return facts