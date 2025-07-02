from knowledge_base.violence_types import *
from knowledge_base.confidence_levels import *
from typing import Dict, Any, List, Tuple

class TextClassifier:
    def __init__(self, groq_api=None):
        """
        Inicializa o classificador de texto.
        
        Args:
            groq_api: API Groq para extração de fatos do texto
        """
        self.groq_api = groq_api
    
    def classify_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Classifica um texto livre usando Groq para extração de fatos e
        o sistema de pontuação baseado em conceitos.
        
        Args:
            text (str): Texto do relato do usuário
            
        Returns:
            List[Dict]: Lista de classificações identificadas
        """
        print("\n📥 [DEBUG] Processando texto:", text[:100] + "..." if len(text) > 100 else text)
        
        # 1. Extrair fatos estruturados do texto usando Groq
        extracted_facts = self._extract_facts_from_text(text)
        print("\n🔍 Fatos extraídos:", extracted_facts)
        
        # 2. Pontuar com base no CONCEPT_MAPPING
        classifications = self._score_extracted_facts(extracted_facts)
        print("\n📊 Classificações acumuladas:", classifications)
        
        # 3. Aplicar limiares e calcular confiança
        results = self._apply_thresholds(classifications)
        print("\n✅ Resultados finais:", results)
        
        return results
    
    def _extract_facts_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extrai fatos estruturados do texto usando o Groq.
        
        Args:
            text (str): Texto do relato
            
        Returns:
            Dict: Fatos estruturados por categoria
        """
        if not self.groq_api:
            # Fallback simples para teste sem o Groq
            print("⚠️ Groq API não configurada, usando extração simplificada")
            return self._basic_fact_extraction(text)
        
        # Sistema de prompt para o Groq
        system_prompt = """
        Você é um assistente especializado em identificar FATOS em relatos de violência.
        Extraia APENAS fatos estruturados do texto, sem interpretação ou conclusões.

        Para cada relato, retorne um JSON com as seguintes categorias:
        - comportamentos: lista de comportamentos identificados, cada um com 'tipo', 'alvo' e 'intensidade'
        - contexto: informações sobre 'local', 'ambiente' e outras circunstâncias
        - frequencia: informações sobre 'valor' (unica_vez, algumas_vezes, repetidamente, continuamente)
        - caracteristicas_alvo: lista de características da pessoa alvo (genero, raca_etnia, etc.)
        - relacionamento: informações sobre o relacionamento entre as partes
        - impacto: lista de impactos relatados pela vítima

        Use APENAS os seguintes valores para os tipos de comportamento:
        interrupcao, questionamento_capacidade, comentarios_saude_mental, piadas_estereotipos,
        perseguicao, vigilancia, exclusao, ameaca, constrangimento, humilhacao, pressao_tarefas,
        natureza_sexual_nao_consentido, contato_fisico_nao_consentido, ato_obsceno, coercao_sexual,
        comentarios_sobre_peso, piadas_sobre_peso, exclusao_por_peso, negacao_acessibilidade,
        infantilizacao, cyberbullying, mensagens_ofensivas, exposicao_conteudo, zombaria_religiao,
        impedimento_pratica_religiosa, discriminacao_origem, piada_sotaque
        """
        
        # Chamar a API do Groq
        response = self.groq_api.extract_facts(text, system_prompt)
        
        # Processar e validar a resposta
        return self._validate_facts(response)
    
    def _basic_fact_extraction(self, text: str) -> Dict[str, Any]:
        """
        Extração básica de fatos para testes sem Groq.
        """
        import re
        
        facts = {
            "comportamentos": [],
            "contexto": {},
            "frequencia": {},
            "caracteristicas_alvo": [],
            "relacionamento": {},
            "impacto": []
        }
        
        # Detectar comportamentos
        behavior_patterns = {
            r"interromp": "interrupcao",
            r"persegui": "perseguicao",
            r"segui": "perseguicao",
            r"ameaç": "ameaca",
            r"constrang": "constrangimento",
            r"humilh": "humilhacao",
            r"peso|gord": "comentarios_sobre_peso",
            r"deficiência|deficiente|acessibilidade": "negacao_acessibilidade",
            r"online|internet|digital|mensag": "cyberbullying",
            r"religi": "zombaria_religiao",
            r"sotaque|região|regional|estrangeiro": "discriminacao_origem"
        }
        
        for pattern, behavior_type in behavior_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                facts["comportamentos"].append({
                    "tipo": behavior_type,
                    "intensidade": "media"
                })
        
        # Detectar frequência
        if re.search(r"várias vezes|frequentemente|repetidamente", text, re.IGNORECASE):
            facts["frequencia"] = {"valor": "repetidamente"}
        elif re.search(r"uma vez|única", text, re.IGNORECASE):
            facts["frequencia"] = {"valor": "unica_vez"}
        elif re.search(r"sempre|todo dia|continuamente", text, re.IGNORECASE):
            facts["frequencia"] = {"valor": "continuamente"}
        else:
            facts["frequencia"] = {"valor": "algumas_vezes"}
        
        # Detectar contexto
        context_patterns = {
            r"sala de aula|aula": "sala_aula",
            r"online|internet|digital|virtual": "ambiente_online",
            r"trabalh|estágio|empresa": "local_trabalho",
            r"campus|universidade|faculdade": "espaco_publico_campus"
        }
        
        for pattern, context_type in context_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                facts["contexto"]["local"] = context_type
                break
        
        # Detectar características alvo
        target_patterns = {
            r"mulher|gênero|feminino|masculino": "genero",
            r"gay|lésbica|orientação sexual": "orientacao_sexual",
            r"negro|preto|branco|raça|cor": "raca_etnia",
            r"deficiente|deficiência": "deficiencia",
            r"gordo|magro|peso|obesidade": "peso_corporal",
            r"sotaque|região|nordestino|nortista|sulista": "origem_regional",
            r"religião|religioso|crença": "religiao"
        }
        
        for pattern, target_type in target_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                if target_type not in facts["caracteristicas_alvo"]:
                    facts["caracteristicas_alvo"].append(target_type)
        
        # Detectar impacto
        impact_patterns = {
            r"constrangimento|constrangido|vergonha": "constrangimento",
            r"triste|depressão|trauma|angústia|ansiedade": "danos_emocionais",
            r"medo|insegurança|receio": "medo_inseguranca",
            r"exposição|exposto|privacy|privacidade": "exposicao_indesejada"
        }
        
        for pattern, impact_type in impact_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                facts["impacto"].append(impact_type)
        
        return facts
    
    def _validate_facts(self, facts: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida e normaliza os fatos extraídos para garantir compatibilidade.
        """
        validated = {
            "comportamentos": [],
            "contexto": {},
            "frequencia": {},
            "caracteristicas_alvo": [],
            "relacionamento": {},
            "impacto": []
        }
        
        # Validar comportamentos
        valid_behavior_types = set(CONCEPT_MAPPING["comportamentos"].keys())
        for behavior in facts.get("comportamentos", []):
            if isinstance(behavior, dict) and "tipo" in behavior:
                if behavior["tipo"] in valid_behavior_types:
                    validated["comportamentos"].append(behavior)
        
        # Validar frequência
        valid_frequencies = set(CONCEPT_MAPPING["frequencia"].keys())
        freq_data = facts.get("frequencia", {})
        if isinstance(freq_data, dict) and "valor" in freq_data:
            if freq_data["valor"] in valid_frequencies:
                validated["frequencia"] = freq_data
        
        # Validar contexto
        valid_contexts = set(CONCEPT_MAPPING["contexto"].keys())
        context_data = facts.get("contexto", {})
        if isinstance(context_data, dict) and "local" in context_data:
            if context_data["local"] in valid_contexts:
                validated["contexto"] = context_data
        
        # Validar características alvo
        valid_targets = set(CONCEPT_MAPPING["caracteristicas_alvo"].keys())
        for target in facts.get("caracteristicas_alvo", []):
            if target in valid_targets:
                validated["caracteristicas_alvo"].append(target)
        
        # Validar relacionamento
        valid_relationships = set(CONCEPT_MAPPING["relacionamento"].keys())
        rel_data = facts.get("relacionamento", {})
        if isinstance(rel_data, dict) and "tipo" in rel_data:
            if rel_data["tipo"] in valid_relationships:
                validated["relacionamento"] = rel_data
        
        # Validar impacto
        valid_impacts = set(CONCEPT_MAPPING["impacto"].keys())
        for impact in facts.get("impacto", []):
            if impact in valid_impacts:
                validated["impacto"].append(impact)
        
        return validated
    
    def _score_extracted_facts(self, facts: Dict[str, Any]) -> Dict[Tuple[str, str], int]:
        """
        Pontua os tipos de violência com base nos fatos extraídos usando o CONCEPT_MAPPING.
        
        Args:
            facts: Dicionário de fatos extraídos do texto
            
        Returns:
            Dict[Tuple[str, str], int]: Dicionário de pontuações por (tipo, subtipo)
        """
        classifications = {}
        
        # Processar comportamentos
        for behavior in facts.get("comportamentos", []):
            behavior_type = behavior.get("tipo")
            if behavior_type in CONCEPT_MAPPING["comportamentos"]:
                mapping = CONCEPT_MAPPING["comportamentos"][behavior_type]
                self._apply_mapping(classifications, mapping)
        
        # Processar frequência
        freq = facts.get("frequencia", {}).get("valor")
        if freq and freq in CONCEPT_MAPPING["frequencia"]:
            mapping = CONCEPT_MAPPING["frequencia"][freq]
            self._apply_mapping(classifications, mapping)
        
        # Processar contexto
        context = facts.get("contexto", {}).get("local")
        if context and context in CONCEPT_MAPPING["contexto"]:
            mapping = CONCEPT_MAPPING["contexto"][context]
            self._apply_mapping(classifications, mapping)
        
        # Processar características alvo
        for target in facts.get("caracteristicas_alvo", []):
            if target in CONCEPT_MAPPING["caracteristicas_alvo"]:
                mapping = CONCEPT_MAPPING["caracteristicas_alvo"][target]
                self._apply_mapping(classifications, mapping)
        
        # Processar relacionamento
        rel_type = facts.get("relacionamento", {}).get("tipo")
        if rel_type and rel_type in CONCEPT_MAPPING["relacionamento"]:
            mapping = CONCEPT_MAPPING["relacionamento"][rel_type]
            self._apply_mapping(classifications, mapping)
        
        # Processar impacto
        for impact in facts.get("impacto", []):
            if impact in CONCEPT_MAPPING["impacto"]:
                mapping = CONCEPT_MAPPING["impacto"][impact]
                self._apply_mapping(classifications, mapping)
        
        return classifications
    
    def _apply_mapping(self, classifications: Dict[Tuple[str, str], int], mapping: Dict):
        """
        Aplica um mapeamento ao dicionário de classificações.
        """
        for violence_type, subtype_data in mapping.items():
            if isinstance(subtype_data, dict):
                for subtype, weight in subtype_data.items():
                    key = (violence_type, subtype)
                    classifications.setdefault(key, 0)
                    classifications[key] += weight
                    print(f"📌 Adicionando peso: ({violence_type}, {subtype}) += {weight}")
            elif isinstance(subtype_data, int):  # Tipo sem subtipo
                key = (violence_type, None)
                classifications.setdefault(key, 0)
                classifications[key] += subtype_data
                print(f"📌 Adicionando peso: ({violence_type}, None) += {subtype_data}")
    
    def _apply_thresholds(self, classifications: Dict[Tuple[str, str], int]) -> List[Dict[str, Any]]:
        """
        Aplica limiares e calcula confiança para cada classificação.
        
        Args:
            classifications: Dicionário de pontuações por (tipo, subtipo)
            
        Returns:
            List[Dict]: Lista de resultados de classificação
        """
        results = []
        for (vtype, subtype), score in classifications.items():
            threshold = get_threshold(vtype, subtype)
            max_score = get_max_score(vtype, subtype)
            print(f"\n📈 Avaliando ({vtype}, {subtype}) → score={score}, threshold={threshold}, max={max_score}")

            if score >= threshold:
                confidence = min(score / max_score, 1.0) if max_score else 0.0
                label = get_confidence_level_label(confidence)
                print(f"✅ Resultado aceito com confiança: {confidence:.2f} ({label})")

                results.append({
                    "violence_type": vtype,
                    "subtype": subtype,
                    "score": score,
                    "threshold": threshold,
                    "confidence": confidence,
                    "confidence_label": label,
                    "definition": self._get_definition(vtype, subtype),
                    "recommendations": self._get_recommendations(vtype, subtype),
                    "channels": self._get_channels(vtype, subtype)
                })
            else:
                print(f"❌ Ignorado: score abaixo do threshold")
        
        return results
    
    # Funções auxiliares para extrair do VIOLENCE_TYPES
    def _get_definition(self, vtype, subtype=None):
        vt_data = VIOLENCE_TYPES.get(vtype, {})
        if subtype:
            return vt_data.get("subtipos", {}).get(subtype, {}).get("definicao", vt_data.get("definicao", ""))
        return vt_data.get("definicao", "")

    def _get_recommendations(self, vtype, subtype=None):
        vt_data = VIOLENCE_TYPES.get(vtype, {})
        return vt_data.get("recomendacoes", [])

    def _get_channels(self, vtype, subtype=None):
        vt_data = VIOLENCE_TYPES.get(vtype, {})
        return vt_data.get("canais_denuncia", [])

# Função wrapper para compatibilidade com código existente
def classify_text(text, groq_api=None):
    """
    Função wrapper para classificação de texto, mantendo compatibilidade.
    """
    classifier = TextClassifier(groq_api)
    return classifier.classify_text(text)