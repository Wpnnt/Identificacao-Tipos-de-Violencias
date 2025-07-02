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
        # Buscar chave da variável de ambiente se não fornecida
        self.api_key = api_key if api_key is not None else os.environ.get("GROQ_API_KEY", "")
        self.model = model
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        self.keyword_dict = {}  # Inicializar o dicionário de palavras-chave
    
    def process_user_text(self, text: str) -> Dict[str, Any]:
        """
        Processa o texto do usuário e extrai palavras-chave via Groq.
        """
        # Adicionar ao contexto da conversa
        self.conversation_context.append({"role": "user", "content": text})
        
        # Construir prompt para o Groq
        prompt = self.groq_api.build_prompt(text, KEYWORDS_DICT)
        
        # Enviar para o Groq
        response = self.groq_api.send_request(prompt)
        
        # Extrair palavras-chave identificadas
        keywords = response.get("identified_keywords", {})
        missing = response.get("missing_information", [])
        questions = response.get("follow_up_questions", [])
        
        # Verificar se há informações críticas faltando
        critical_fields = ["action_type"]
        missing_critical = any(field in missing for field in critical_fields)
        
        if missing_critical:
            # Se faltar informação crítica, retornar status incompleto
            return {
                "status": "incomplete",
                "identified_keywords": keywords,
                "missing_fields": missing,
                "questions": questions,
                "facts": self._extract_facts_from_keywords(keywords)
            }
        
        # Se tivermos informações suficientes, criar fatos e classificar
        facts = self._extract_facts_from_keywords(keywords)
        classifications = classify_by_mapping(facts)
        
        return {
            "status": "complete",
            "identified_keywords": keywords,
            "facts": facts,
            "classifications": classifications
        }
    
    def _extract_facts_from_keywords(self, keywords: Dict) -> Dict:
        """
        Converte palavras-chave identificadas em fatos para o motor de inferência.
        """
        facts = {}
        
        # Para cada categoria, seleciona a primeira palavra-chave como fato
        for category, values in keywords.items():
            if values:  # Se há palavras-chave identificadas
                facts[category] = values[0]  # Usa a primeira palavra-chave
        
        return facts
    
    def _process_followup(self, follow_up_text: str, previous_keywords: Dict, missing_fields: List[str]) -> Dict[str, Any]:
        """
        Processa a resposta do usuário para perguntas complementares.
        """
        # Adicionar ao contexto da conversa
        self.conversation_context.append({"role": "user", "content": follow_up_text})
        
        # Construir prompt específico para follow-up
        prompt = self.groq_api.build_prompt(
            follow_up_text, 
            KEYWORDS_DICT, 
            is_follow_up=True, 
            missing_fields=missing_fields
        )
        
        # Enviar para o Groq
        response = self.groq_api.send_request(prompt)
        
        # Combinar palavras-chave anteriores com as novas
        combined_keywords = self._combine_keywords(previous_keywords, response.get("identified_keywords", {}))
        
        # Extrair fatos das palavras-chave combinadas
        facts = self._extract_facts_from_keywords(combined_keywords)
        
        # Verificar se ainda faltam informações críticas
        missing = response.get("missing_information", [])
        questions = response.get("follow_up_questions", [])
        critical_fields = ["action_type"]
        missing_critical = any(field in missing for field in critical_fields)
        
        if missing_critical:
            return {
                "status": "incomplete",
                "identified_keywords": combined_keywords,
                "missing_fields": missing,
                "questions": questions,
                "facts": facts
            }
        
        # Se tivermos informações suficientes, classificar
        classifications = classify_by_mapping(facts)
        
        return {
            "status": "complete",
            "identified_keywords": combined_keywords,
            "facts": facts,
            "classifications": classifications
        }

    def _combine_keywords(self, previous: Dict, new: Dict) -> Dict:
        """
        Combina palavras-chave anteriores com novas.
        """
        result = previous.copy()
        
        for category, values in new.items():
            if category not in result:
                result[category] = values
            else:
                # Combinar e remover duplicatas
                result[category] = list(set(result[category] + values))
        
        return result