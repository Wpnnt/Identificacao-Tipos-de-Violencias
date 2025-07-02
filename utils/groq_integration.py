import json
import requests
from typing import Dict, List, Any, Optional
import os

class GroqAPI:
    """
    Classe para comunicação com a API do Groq.
    Gerencia a construção de prompts e o processamento das respostas.
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
    
    def build_prompt(self, user_text: str, keywords_dict: Dict, 
                    is_follow_up: bool = False,
                    missing_fields: List[str] = None) -> Dict[str, str]:
        """
        Constrói o prompt para o Groq com instruções claras sobre as palavras-chave.
        """
        # Armazenar o dicionário para uso na validação
        self.keyword_dict = keywords_dict

        # Instruções do sistema
        system_prompt = """
        Você é um assistente especializado em identificar indicadores de violência em relatos.
        Sua função é APENAS identificar quais palavras-chave da lista fornecida estão presentes
        no relato do usuário.
        
        IMPORTANTE:
        1. Retorne APENAS um objeto JSON válido com as palavras-chave identificadas
        2. NUNCA invente ou adicione palavras que não estejam na lista fornecida
        3. Identifique APENAS palavras ou conceitos que estejam explicitamente mencionados no relato
        4. Se necessário, sugira perguntas específicas para obter informações faltantes
        5. NÃO PERGUNTE sobre informações que o usuário já forneceu ou disse explicitamente não saber
        6. Se o usuário indicar desconhecimento sobre algum aspecto (como "não vi quem era", "não sei quem fez", "não sei o nome da pessoa"), 
            NÃO formule perguntas tentando identificar essa informação
        7. NÃO modifique nem parafraseie as palavras-chave - use-as exatamente como estão na lista
        LISTA DE PALAVRAS-CHAVE POR CATEGORIA:
        """
        
        # Adicionar todas as palavras-chave organizadas por categoria
        for category, keywords in keywords_dict.items():
            system_prompt += f"\n{category.upper()}:\n"
            system_prompt += ", ".join(f'"{kw}"' for kw in keywords)
        
        # Instruções para follow-up (se aplicável)
        if is_follow_up and missing_fields:
            system_prompt += "\n\nInformações importantes faltando: " + ", ".join(missing_fields)
            system_prompt += "\nFormule perguntas específicas para obter estas informações."
            system_prompt += "\nLembre-se: não pergunte sobre informações já fornecidas ou que o usuário já indicou desconhecer."
            system_prompt += "\nNão pergunte sobre informações que o usuário já disse não saber, como nomes ou detalhes que ele não viu."
            system_prompt += "\nNão invente nada, apenas identifique palavras-chave do relato que forem claramente aceitáveis."

        # Formato de resposta obrigatório
        system_prompt += """
        
        FORMATO DE RESPOSTA (JSON):
        {
            "identified_keywords": {
                "action_type": ["palavra1", "palavra2"],
                "frequency": ["palavra3"],
                "context": ["palavra4"],
                "target": ["palavra5"],
                "relationship": ["palavra6"],
                "impact": ["palavra7"]
            },
            "missing_information": ["campo1", "campo2"],
            "follow_up_questions": ["pergunta específica 1?", "pergunta específica 2?"]
        }
        
        Só inclua categorias que tenham palavras-chave identificadas.
        Para "relationship", se o relato indicar que o agressor é desconhecido, NÃO solicite mais informações sobre identidade.
        Certifique-se de que suas perguntas complementares são relevantes e não contradizem o que já foi compartilhado.
        """
        
        return {
            "system": system_prompt,
            "user": f"RELATO: {user_text}"
        }
    
    def send_request(self, prompt: Dict[str, str]) -> Dict[str, Any]:
        """
        Envia requisição para a API do Groq e processa a resposta.
        """
        try:
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]}
                ],
                "temperature": 0.1,  # temperatura baixa para respostas mais previsíveis
                "response_format": {"type": "json_object"}  # forçar resposta em JSON
            }
            
            response = requests.post(self.endpoint, headers=self.headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            parsed_content = json.loads(result["choices"][0]["message"]["content"])
            
            # Aplicar validação para garantir que só retorna palavras-chave válidas
            return self.validate_response(parsed_content)
        
        except Exception as e:
            print(f"Erro na comunicação com Groq: {e}")
            # Resposta de fallback em caso de erro
            return {
                "identified_keywords": {},
                "missing_information": ["action_type"],
                "follow_up_questions": ["Poderia descrever melhor o que aconteceu?"]
            }
    
    def validate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida a resposta do Groq para garantir que só contém palavras-chave válidas.
        """
        valid_response = {
            "identified_keywords": {},
            "missing_information": response.get("missing_information", []),
            "follow_up_questions": response.get("follow_up_questions", [])[:3]  # Limitar a 3 perguntas
        }
        
        # Filtrar apenas palavras-chave válidas
        if "identified_keywords" in response:
            for category, keywords in response["identified_keywords"].items():
                if category not in self.keyword_dict:
                    continue  # Pular categorias não reconhecidas
                    
                valid_keywords = []
                for kw in keywords:
                    # Primeiro verificar correspondência exata
                    if kw in self.keyword_dict[category]:
                        valid_keywords.append(kw)
                    else:
                        # Tentar correspondência case-insensitive
                        kw_lower = kw.lower()
                        for valid_kw in self.keyword_dict[category]:
                            if valid_kw.lower() == kw_lower:
                                valid_keywords.append(valid_kw)  # Usar a versão correta do catálogo
                                break
                
                if valid_keywords:  # Só adicionar se houver palavras-chave válidas
                    valid_response["identified_keywords"][category] = valid_keywords
                
        return valid_response