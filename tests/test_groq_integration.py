import sys
import os
import json
from io import StringIO

# Adicionar o diretório raiz ao path para permitir as importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from knowledge_base.violence_types import VIOLENCE_TYPES
from knowledge_base.confidence_levels import CONCEPT_MAPPING
from knowledge_base.keywords_dictionary import KEYWORDS_DICT
from utils.groq_integration import GroqAPI
from typing import Dict, List

def test_groq_keywords_match():
    """
    Testa se o Groq retorna APENAS palavras-chave que existem no KEYWORDS_DICT.
    """
    print("\n=== TESTANDO SE O GROQ RETORNA APENAS PALAVRAS-CHAVE DO SISTEMA ===\n")
    
    # Inicializar API do Groq
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("⚠️ API_KEY do Groq não encontrada. Configure a variável de ambiente GROQ_API_KEY.")
        return False
        
    groq_api = GroqAPI(api_key)
    
    # Textos de teste com situações variadas
    test_cases = [
        {
            "name": "Caso 1: Microagressões em sala de aula",
            "text": "O professor me interrompe constantemente durante minhas apresentações em sala de aula, sempre questionando minhas capacidades. Isso acontece repetidamente há semanas e acredito que seja por causa do meu gênero."
        },
        {
            "name": "Caso 2: Assédio sexual e perseguição",
            "text": "Um colega tem me seguido pelo campus, fazendo comentários de natureza sexual não consentidos e me deixando constrangida. Já aconteceu várias vezes e estou com medo."
        },
        {
            "name": "Caso 3: Discriminação religiosa",
            "text": "Durante uma aula, o professor zombou da minha religião e fez piadas sobre minhas crenças. Todos riram e me senti humilhada e discriminada."
        },
        {
            "name": "Caso 4: Violência física e estupro",
            "text": "Eu estava tendo relações com meu namorado, até aí tudo bem. Porém quando eu disse para parar ele não parou."
        }
    ]
    
    # Resultados totais
    total_keywords = 0
    valid_keywords = 0
    invalid_keywords = []
    
    # Dicionário para armazenar detalhes dos casos
    case_results = {}
    
    # Buffer para coletar saída dos casos individuais
    case_outputs = []
    
    # Testar cada caso
    for idx, case in enumerate(test_cases):
        case_id = f"caso_{idx+1}"
        case_results[case_id] = {
            "name": case["name"],
            "keywords_found": {},
            "valid_count": 0,
            "invalid_count": 0
        }
        
        output = StringIO()
        output.write(f"\n{case['name']}\n")
        
        try:
            # Construir o prompt e enviar para o Groq
            prompt = groq_api.build_prompt(case['text'], KEYWORDS_DICT)
            response = groq_api.send_request(prompt)
            
            # Verificar se há palavras-chave identificadas
            if "identified_keywords" in response:
                output.write("\nPalavras-chave identificadas:\n")
                
                for category, keywords in response["identified_keywords"].items():
                    # Armazenar resultados para este caso
                    case_results[case_id]["keywords_found"][category] = keywords
                    
                    # Mostrar palavras-chave encontradas
                    output.write(f"- {category}: {', '.join(keywords)}\n")
                    
                    # Validar cada palavra-chave
                    for keyword in keywords:
                        total_keywords += 1
                        
                        # Verificar se a palavra-chave está no dicionário para esta categoria
                        if category in KEYWORDS_DICT and keyword in KEYWORDS_DICT[category]:
                            valid_keywords += 1
                            case_results[case_id]["valid_count"] += 1
                        else:
                            invalid_keywords.append((category, keyword, case_id))
                            case_results[case_id]["invalid_count"] += 1
            else:
                output.write("Nenhuma palavra-chave identificada.\n")
        except Exception as e:
            output.write(f"⚠️ Erro ao processar caso: {str(e)}\n")
        
        # Armazenar a saída deste caso
        case_outputs.append(output.getvalue())
    
    # Agora imprimir os resultados de cada caso uma única vez
    for output in case_outputs:
        print(output)
    
    # Calcular a taxa de precisão
    accuracy = (valid_keywords / total_keywords * 100) if total_keywords > 0 else 0
    
    # Exibir resultados finais uma única vez
    divider = "=" * 60
    print(f"\n{divider}")
    print("=== RESULTADOS FINAIS DO TESTE ===")
    print(divider)
    
    print(f"\nTotal de palavras-chave identificadas: {total_keywords}")
    print(f"Palavras-chave válidas: {valid_keywords}")
    print(f"Taxa de precisão: {accuracy:.2f}%")
    
    # Resumo por caso
    print("\nResumo por caso:")
    for case_id, result in sorted(case_results.items()):
        valid_percent = 100 * result["valid_count"] / (result["valid_count"] + result["invalid_count"]) if (result["valid_count"] + result["invalid_count"]) > 0 else 0
        print(f"- {result['name']}: {result['valid_count']} válidas, {result['invalid_count']} inválidas ({valid_percent:.1f}% precisão)")
    
    # Mostrar palavras-chave inválidas se houver
    if invalid_keywords:
        print("\nPalavras-chave inválidas encontradas:")
        for category, keyword, case_id in invalid_keywords:
            case_name = next((c["name"] for c_id, c in case_results.items() if c_id == case_id), "Caso desconhecido")
            print(f"- [{case_name}] {category}: {keyword}")
    else:
        print("\n✅ TODAS as palavras-chave retornadas pelo Groq estão no dicionário do sistema!")
    
    # Conclusão final
    print(f"\n{divider}")
    if accuracy >= 95:
        print("🎉 SUCESSO! O Groq está retornando palavras-chave exatamente como definidas no sistema.")
    elif accuracy >= 80:
        print("⚠️ ATENÇÃO: O Groq está retornando a maioria das palavras-chave corretamente, mas há algumas inconsistências.")
    else:
        print("❌ FALHA: O Groq está retornando muitas palavras-chave que não existem no sistema.")
    
    return accuracy >= 95

def test_groq_integration():
    """
    Função original para testar a integração com o Groq.
    Mantida para compatibilidade.
    """
    print("Esta função foi substituída por test_groq_keywords_match().")
    return test_groq_keywords_match()

if __name__ == "__main__":
    # Executar o teste de correspondência de palavras-chave
    test_groq_keywords_match()