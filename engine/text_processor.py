import os
from typing import Dict, List, Any
from knowledge_base.keywords_dictionary import KEYWORDS_DICT, FIELDS_QUESTIONS
from utils.groq_integration import GroqAPI
from engine.classifier import classify_by_mapping

class TextProcessor:
    """
    Processa texto livre do usuário para extrair fatos e disparar regras.
    """
    def __init__(self, api_key: str = None, 
                 model: str = "meta-llama/llama-4-scout-17b-16e-instruct"):
        # Usa a chave da API fornecida ou busca da variável de ambiente
        self.api_key = api_key if api_key else os.environ.get("GROQ_API_KEY", "")
        self.model = model
        self.groq_api = GroqAPI(api_key=self.api_key, model=self.model)
        self.conversation_context = []

    def process_user_text(self, text: str) -> Dict[str, Any]:
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

    def _process_followup(self, follow_up_text: str, previous_keywords: Dict, missing_fields: List[str]) -> Dict[str, Any]:
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
        return {category: values[0] for category, values in keywords.items() if values}

    def _combine_keywords(self, previous: Dict, new: Dict) -> Dict:
        result = previous.copy()
        for category, values in new.items():
            if category in result:
                result[category] = list(set(result[category] + values))
            else:
                result[category] = values
        return result