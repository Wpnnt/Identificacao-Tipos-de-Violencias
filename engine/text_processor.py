import os
from typing import Dict, List, Any
import json

from knowledge_base.keywords_dictionary import KEYWORDS_DICT, FIELDS_QUESTIONS
from utils.groq_integration import GroqAPI

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
        
        # Lista para armazenar os fatos que serão retornados
        facts = [TextRelato(text=text, processed=True)]
        
        try:
            # Extrair palavras-chave usando o Groq
            prompt = self.groq_api.build_prompt(text, KEYWORDS_DICT)
            response = self.groq_api.send_request(prompt)
            
            if "identified_keywords" in response and response["identified_keywords"]:
                print(f"✅ Palavras-chave identificadas: {json.dumps(response['identified_keywords'], indent=2)}")
                
                # Converter resposta em fatos Experta
                keywords = response["identified_keywords"]
                
                for category, values in keywords.items():
                    for keyword in values:
                        # Criar fato KeywordFact
                        kw_fact = KeywordFact(category=category, keyword=keyword)
                        facts.append(kw_fact)
                        print(f"📌 Criado fato Experta: KeywordFact(category='{category}', keyword='{keyword}')")
                        
                        # Criar fatos específicos correspondentes
                        if category == "action_type":
                            behavior_fact = ViolenceBehavior(behavior_type=keyword)
                            facts.append(behavior_fact)
                            print(f"📌 Criado fato Experta: ViolenceBehavior(behavior_type='{keyword}')")
                        
                        elif category == "context":
                            context_fact = ContextFact(location=keyword)
                            facts.append(context_fact)
                            print(f"📌 Criado fato Experta: ContextFact(location='{keyword}')")
                        
                        elif category == "frequency":
                            freq_fact = FrequencyFact(value=keyword)
                            facts.append(freq_fact)
                            print(f"📌 Criado fato Experta: FrequencyFact(value='{keyword}')")
                        
                        elif category == "target":
                            target_fact = TargetFact(characteristic=keyword)
                            facts.append(target_fact)
                            print(f"📌 Criado fato Experta: TargetFact(characteristic='{keyword}')")
                        
                        elif category == "relationship":
                            rel_fact = RelationshipFact(type=keyword)
                            facts.append(rel_fact)
                            print(f"📌 Criado fato Experta: RelationshipFact(type='{keyword}')")
                        
                        elif category == "impact":
                            impact_fact = ImpactFact(type=keyword)
                            facts.append(impact_fact)
                            print(f"📌 Criado fato Experta: ImpactFact(type='{keyword}')")
            else:
                print("⚠️ Nenhuma palavra-chave identificada no texto")
        
        except Exception as e:
            print(f"❌ Erro ao processar texto: {str(e)}")
        
        return facts