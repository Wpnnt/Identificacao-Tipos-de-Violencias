import os
from typing import Dict, List, Any
import json

from knowledge_base.keywords_dictionary import KEYWORDS_DICT, FIELDS_QUESTIONS
from utils.groq_integration import GroqAPI

# Importar fatos do Experta para criar objetos compatíveis com o motor de regras
from engine.facts import (
    TextRelato, KeywordFact, ViolenceBehavior, ContextFact, FrequencyFact,
    TargetFact, RelationshipFact, ImpactFact, create_facts_from_groq_response
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

        return {
            "status": "complete" if not missing_critical else "incomplete",
            "identified_keywords": keywords,
            "missing_fields": missing,
            "questions": questions,
            "facts": facts
        }

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

        return {
            "status": "complete" if not missing_critical else "incomplete",
            "identified_keywords": combined_keywords,
            "missing_fields": missing,
            "questions": questions,
            "facts": facts
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
                keywords = response["identified_keywords"]
                
                # Criar fatos KeywordFact
                for category, values in keywords.items():
                    for keyword in values:
                        facts.append(KeywordFact(category=category, keyword=keyword))
                        
                        # Criar fatos específicos correspondentes
                        if category == "action_type":
                            facts.append(ViolenceBehavior(behavior_type=keyword))
                        elif category == "context":
                            facts.append(ContextFact(location=keyword))
                        elif category == "frequency":
                            facts.append(FrequencyFact(value=keyword))
                        elif category == "target":
                            facts.append(TargetFact(characteristic=keyword))
                        elif category == "relationship":
                            facts.append(RelationshipFact(type=keyword))
                        elif category == "impact":
                            facts.append(ImpactFact(type=keyword))
                
                for fact in facts:
                    print(f"📌 Criado fato Experta: {fact}")
            else:
                print("⚠️ Nenhuma palavra-chave identificada no texto")
        except Exception as e:
            print(f"❌ Erro ao processar texto: {str(e)}")
        
        return facts