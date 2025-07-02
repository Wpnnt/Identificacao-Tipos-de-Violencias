import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.groq_integration import GroqAPI
from knowledge_base.keywords_dictionary import KEYWORDS_DICT

def test_groq_integration():
    """Testa a integração básica com o Groq API."""
    print("Iniciando teste de integração com Groq...")
    
    # Inicializar API usando variável de ambiente
    groq_api = GroqAPI()  # Não passa a chave explicitamente, usa a variável de ambiente
    
    # Texto de teste
    test_text = "Estava andando na rua e alguém assobiou para mim, depois disso um grupo de pessoas desconhecidas começou a me seguir. Eu me senti muito inseguro e com medo, pois não sabia o que poderiam fazer. Isso aconteceu várias vezes ao longo da semana, sempre no mesmo horário e local. Eu gostaria de entender melhor o que está acontecendo e como posso lidar com isso."
    
    # Construir prompt
    prompt = groq_api.build_prompt(test_text, KEYWORDS_DICT)
    
    # Enviar requisição
    print("Enviando requisição para o Groq...")
    response = groq_api.send_request(prompt)
    
    # Mostrar resultado
    print("\nResposta do Groq:")
    print("Palavras-chave identificadas:")
    for category, keywords in response.get("identified_keywords", {}).items():
        print(f"- {category}: {keywords}")

    print("\nInformações faltantes:")
    print(response.get("missing_information", []))

    print("\nPerguntas complementares:")
    for question in response.get("follow_up_questions", []):
        print(f"- {question}")
    
    return response

if __name__ == "__main__":
    test_groq_integration()