from experta.engine import KnowledgeEngine
from experta import Fact
from experta.rule import Rule
from experta.deffacts import DefFacts
from experta import TEST, AS, OR, NOT, AND
from typing import Dict, List, Any, Optional
import json

# Importações dos fatos necessários para o motor de regras
from .facts import (
    TextRelato, KeywordFact, ViolenceBehavior, ContextFact, FrequencyFact,
    TargetFact, RelationshipFact, ImpactFact, ViolenceClassification,
    AnalysisResult, create_facts_from_groq_response, calculate_confidence
)
from knowledge_base.confidence_levels import *
from knowledge_base.violence_types import VIOLENCE_TYPES

class ViolenceRules(KnowledgeEngine):
    """
    Motor de regras para identificação de tipos de violência.
    
    Este motor utiliza a biblioteca Experta para implementar um sistema
    baseado em regras que classifica fatos estruturados em tipos de violência
    conforme definidos na base de conhecimento.
    """
    
    def __init__(self):
        """Inicializa o motor de regras."""
        super().__init__()
        self.explanations = {}  # Armazena explicações para cada classificação
    
    @DefFacts()
    def initial_facts(self):
        yield Fact(engine_ready=True)
    
    # REGRAS PARA MICROAGRESSÕES
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="interrupcao"),
            KeywordFact(category="action_type", keyword="interrupcao")
        ),
        OR(
            FrequencyFact(value="repetidamente"),
            FrequencyFact(value="continuamente"),
            KeywordFact(category="frequency", keyword="repetidamente"),
            KeywordFact(category="frequency", keyword="continuamente")
        )
    )
    def detect_interrupcoes_constantes(self):
        """Detecta microagressões do tipo interrupções constantes."""
        self.add_score("microagressoes", "interrupcoes_constantes", 15, [
            "Identificado comportamento de interrupção",
            "Ocorre repetidamente ou continuamente"
        ])
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="questionamento_capacidade"),
            KeywordFact(category="action_type", keyword="questionamento_capacidade")
        ),
        OR(
            TargetFact(characteristic="genero"),
            KeywordFact(category="target", keyword="genero")
        )
    )
    def detect_questionar_julgamento(self):
        """Detecta microagressões do tipo questionamento de capacidade."""
        self.add_score("microagressoes", "questionar_julgamento", 14, [
            "Identificado comportamento de questionar capacidade",
            "Direcionado a características de gênero"
        ])
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="comentarios_saude_mental"),
            KeywordFact(category="action_type", keyword="comentarios_saude_mental")
        )
    )
    def detect_comentarios_saude_mental(self):
        """Detecta microagressões relacionadas a comentários sobre saúde mental."""
        self.add_score("microagressoes", "comentarios_saude_mental", 10, [
            "Identificados comentários relacionados à saúde mental"
        ])
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="piadas_estereotipos"),
            KeywordFact(category="action_type", keyword="piadas_estereotipos")
        )
    )
    def detect_estereotipos(self):
        """Detecta microagressões baseadas em estereótipos."""
        self.add_score("microagressoes", "estereotipos", 12, [
            "Identificadas piadas ou comentários baseados em estereótipos"
        ])
    
    # REGRAS PARA PERSEGUIÇÃO
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="perseguicao"),
            ViolenceBehavior(behavior_type="vigilancia"),
            KeywordFact(category="action_type", keyword="perseguicao"),
            KeywordFact(category="action_type", keyword="vigilancia"),
            KeywordFact(category="action_type", keyword="stalking")
        )
    )
    def detect_perseguicao(self):
        """Detecta comportamento de perseguição."""
        self.add_score("perseguicao", None, 15, [
            "Identificado comportamento de perseguição ou vigilância constante"
        ])
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="perseguicao"),
            KeywordFact(category="action_type", keyword="perseguicao")
        ),
        OR(
            ImpactFact(type="medo_inseguranca"),
            KeywordFact(category="impact", keyword="medo_inseguranca"),
            KeywordFact(category="impact", keyword="medo"),
            KeywordFact(category="impact", keyword="inseguranca")
        )
    )
    def detect_perseguicao_com_medo(self):
        """Detecta perseguição que causa medo/insegurança."""
        self.add_score("perseguicao", None, 20, [
            "Identificado comportamento de perseguição",
            "Causa medo ou insegurança na vítima"
        ])
    
    # REGRAS PARA DISCRIMINAÇÃO DE GÊNERO
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="exclusao"),
            KeywordFact(category="action_type", keyword="exclusao")
        ),
        OR(
            TargetFact(characteristic="genero"),
            TargetFact(characteristic="orientacao_sexual"),
            KeywordFact(category="target", keyword="genero"),
            KeywordFact(category="target", keyword="orientacao_sexual")
        )
    )
    def detect_discriminacao_flagrante(self):
        """Detecta discriminação flagrante baseada em gênero."""
        self.add_score("discriminacao_genero", "discriminacao_flagrante", 15, [
            "Identificado comportamento de exclusão",
            "Direcionado a características de gênero ou orientação sexual"
        ])
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="questionamento_capacidade"),
            KeywordFact(category="action_type", keyword="questionamento_capacidade")
        ),
        OR(
            TargetFact(characteristic="genero"),
            KeywordFact(category="target", keyword="genero")
        ),
        OR(
            FrequencyFact(value="repetidamente"),
            FrequencyFact(value="continuamente"),
            KeywordFact(category="frequency", keyword="repetidamente"),
            KeywordFact(category="frequency", keyword="continuamente")
        )
    )
    def detect_discriminacao_sutil(self):
        """Detecta discriminação sutil baseada em gênero."""
        self.add_score("discriminacao_genero", "discriminacao_sutil", 17, [
            "Identificado comportamento de questionamento de capacidade",
            "Direcionado a características de gênero",
            "Ocorre repetidamente ou continuamente"
        ])
    
    # REGRAS PARA ABUSO PSICOLÓGICO
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="ameaca"),
            ViolenceBehavior(behavior_type="humilhacao"),
            ViolenceBehavior(behavior_type="constrangimento"),
            KeywordFact(category="action_type", keyword="ameaca"),
            KeywordFact(category="action_type", keyword="humilhacao"),
            KeywordFact(category="action_type", keyword="constrangimento")
        )
    )
    def detect_abuso_psicologico(self):
        """Detecta abuso psicológico."""
        self.add_score("abuso_psicologico", None, 16, [
            "Identificado comportamento de ameaça, humilhação ou constrangimento"
        ])
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="ameaca"),
            ViolenceBehavior(behavior_type="humilhacao"),
            KeywordFact(category="action_type", keyword="ameaca"),
            KeywordFact(category="action_type", keyword="humilhacao")
        ),
        OR(
            RelationshipFact(type="superior_hierarquico"),
            KeywordFact(category="relationship", keyword="superior_hierarquico")
        )
    )
    def detect_abuso_psicologico_hierarquico(self):
        """Detecta abuso psicológico com relação hierárquica."""
        self.add_score("abuso_psicologico", None, 20, [
            "Identificado comportamento de ameaça ou humilhação",
            "Praticado por superior hierárquico"
        ])
    
    # REGRAS PARA ASSÉDIO MORAL DE GÊNERO
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="pressao_tarefas"),
            KeywordFact(category="action_type", keyword="pressao_tarefas")
        ),
        OR(
            TargetFact(characteristic="genero"),
            KeywordFact(category="target", keyword="genero")
        ),
        OR(
            ContextFact(location="local_trabalho"),
            KeywordFact(category="context", keyword="local_trabalho")
        )
    )
    def detect_assedio_moral_genero(self):
        """Detecta assédio moral baseado em gênero."""
        self.add_score("assedio_moral_genero", None, 20, [
            "Identificado comportamento de pressão excessiva com tarefas",
            "Direcionado a características de gênero",
            "Ocorre em local de trabalho"
        ])
    
    # REGRAS PARA VIOLÊNCIA SEXUAL
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="natureza_sexual_nao_consentido"),
            KeywordFact(category="action_type", keyword="natureza_sexual_nao_consentido")
        )
    )
    def detect_assedio_sexual(self):
        """Detecta assédio sexual."""
        self.add_score("violencia_sexual", "assedio_sexual", 10, [
            "Identificado comportamento de natureza sexual não consentido"
        ])
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="contato_fisico_nao_consentido"),
            ViolenceBehavior(behavior_type="ato_obsceno"),
            KeywordFact(category="action_type", keyword="contato_fisico_nao_consentido"),
            KeywordFact(category="action_type", keyword="ato_obsceno")
        )
    )
    def detect_importunacao_sexual(self):
        """Detecta importunação sexual."""
        self.add_score("violencia_sexual", "importunacao_sexual", 10, [
            "Identificado contato físico não consentido ou ato obsceno"
        ])
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="coercao_sexual"),
            KeywordFact(category="action_type", keyword="coercao_sexual"),
            KeywordFact(category="action_type", keyword="estupro"),
            KeywordFact(category="action_type", keyword="abuso")
        )
    )
    def detect_estupro(self):
        """Detecta estupro."""
        self.add_score("violencia_sexual", "estupro", 10, [
            "Identificado comportamento de coerção sexual ou relação não consentida"
        ])
    
    # REGRAS PARA GORDOFOBIA
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="comentarios_sobre_peso"),
            ViolenceBehavior(behavior_type="piadas_sobre_peso"),
            KeywordFact(category="action_type", keyword="comentarios_sobre_peso"),
            KeywordFact(category="action_type", keyword="piadas_sobre_peso")
        )
    )
    def detect_gordofobia_direta(self):
        """Detecta discriminação direta por gordofobia."""
        self.add_score("gordofobia", "discriminacao_direta", 12, [
            "Identificados comentários ou piadas sobre peso/corpo"
        ])
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="exclusao_por_peso"),
            KeywordFact(category="action_type", keyword="exclusao_por_peso")
        )
    )
    def detect_gordofobia_estrutural(self):
        """Detecta discriminação estrutural por gordofobia."""
        self.add_score("gordofobia", "discriminacao_estrutural", 15, [
            "Identificada exclusão baseada em peso/aparência física"
        ])
    
    # REGRAS PARA CAPACITISMO
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="negacao_acessibilidade"),
            KeywordFact(category="action_type", keyword="negacao_acessibilidade")
        )
    )
    def detect_barreiras_fisicas(self):
        """Detecta barreiras físicas de acessibilidade."""
        self.add_score("capacitismo", "barreiras_fisicas", 12, [
            "Identificada negação de acessibilidade ou barreiras físicas"
        ])
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="infantilizacao"),
            KeywordFact(category="action_type", keyword="infantilizacao")
        ),
        OR(
            TargetFact(characteristic="deficiencia"),
            KeywordFact(category="target", keyword="deficiencia")
        )
    )
    def detect_barreiras_atitudinais(self):
        """Detecta barreiras atitudinais de acessibilidade."""
        self.add_score("capacitismo", "barreiras_atitudinais", 14, [
            "Identificado comportamento de infantilização",
            "Direcionado a pessoa com deficiência"
        ])
    
    # REGRAS PARA VIOLÊNCIA DIGITAL
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="cyberbullying"),
            ViolenceBehavior(behavior_type="mensagens_ofensivas"),
            KeywordFact(category="action_type", keyword="cyberbullying"),
            KeywordFact(category="action_type", keyword="mensagens_ofensivas")
        )
    )
    def detect_cyberbullying(self):
        """Detecta cyberbullying."""
        self.add_score("violencia_digital", "cyberbullying", 14, [
            "Identificado comportamento de cyberbullying ou mensagens ofensivas"
        ])
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="exposicao_conteudo"),
            KeywordFact(category="action_type", keyword="exposicao_conteudo")
        )
    )
    def detect_exposicao_nao_consentida(self):
        """Detecta exposição não consentida."""
        self.add_score("violencia_digital", "exposicao_nao_consentida", 8, [
            "Identificada exposição não consentida de conteúdo pessoal"
        ])
    
    # REGRAS PARA DISCRIMINAÇÃO RELIGIOSA
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="zombaria_religiao"),
            KeywordFact(category="action_type", keyword="zombaria_religiao")
        ),
        OR(
            TargetFact(characteristic="religiao"),
            KeywordFact(category="target", keyword="religiao")
        )
    )
    def detect_ofensa_religiosa_direta(self):
        """Detecta ofensa religiosa direta."""
        self.add_score("discriminacao_religiosa", "ofensa_direta", 12, [
            "Identificada zombaria ou piadas sobre religião",
            "Direcionada a características religiosas da vítima"
        ])
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="impedimento_pratica_religiosa"),
            KeywordFact(category="action_type", keyword="impedimento_pratica_religiosa")
        )
    )
    def detect_discriminacao_religiosa_institucional(self):
        """Detecta discriminação religiosa institucional."""
        self.add_score("discriminacao_religiosa", "discriminacao_institucional", 16, [
            "Identificado impedimento de práticas religiosas"
        ])
    
    # REGRAS PARA XENOFOBIA
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="piada_sotaque"),
            KeywordFact(category="action_type", keyword="piada_sotaque")
        ),
        OR(
            TargetFact(characteristic="origem_regional"),
            KeywordFact(category="target", keyword="origem_regional")
        )
    )
    def detect_discriminacao_regional(self):
        """Detecta discriminação regional."""
        self.add_score("xenofobia", "discriminacao_regional", 14, [
            "Identificadas piadas ou comentários sobre sotaque",
            "Direcionados à origem regional da vítima"
        ])
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="discriminacao_origem"),
            KeywordFact(category="action_type", keyword="discriminacao_origem")
        ),
        OR(
            TargetFact(characteristic="origem_estrangeira"),
            KeywordFact(category="target", keyword="origem_estrangeira")
        )
    )
    def detect_xenofobia_internacional(self):
        """Detecta xenofobia internacional."""
        self.add_score("xenofobia", "xenofobia_internacional", 12, [
            "Identificada discriminação baseada em origem",
            "Direcionada à origem estrangeira da vítima"
        ])
    
    # REGRA PARA CONSOLIDAR RESULTADOS
    
    def consolidate_results(self):
        """
        Consolida os resultados de todas as classificações.
        
        Esta regra é disparada após todas as classificações individuais
        terem sido processadas. Ela resolve ambiguidades e cria um resultado
        final de análise.
        """

        all_classifications = []
        for fact_id in self.get_matching_facts(ViolenceClassification):
            fact = self.facts[fact_id]
            all_classifications.append({
                "violence_type": fact["violence_type"],
                "subtype": fact["subtype"],
                "score": fact["score"],
                "confidence": fact["confidence_level"],
                "explanation": self.get_explanation(fact["violence_type"], fact["subtype"])
            })
        
        if not all_classifications:
            print("⚠️ Nenhuma classificação identificada")
            return

        report_multiple, ambiguity_level = should_report_multiple(all_classifications)
        primary_result = resolve_ambiguity(all_classifications)

        self.declare(
            AnalysisResult(
                classifications=all_classifications,
                primary_result=primary_result,
                multiple_types=report_multiple,
                ambiguity_level=ambiguity_level
            )
        )

        print("\n✅ Análise consolidada:")
        print(f"- Resultado principal: {primary_result['violence_type']}{' - ' + primary_result['subtype'] if primary_result.get('subtype') else ''}")
        print(f"- Confiança: {primary_result['confidence']:.2f}")
        print(f"- Reportar múltiplos: {report_multiple}")
        if report_multiple:
            print(f"- Nível de ambiguidade: {ambiguity_level:.2f}")
            print(f"- Todas as classificações: {len(all_classifications)}")
            for c in all_classifications:
                print(f"  • {c['violence_type']}{' - ' + c['subtype'] if c.get('subtype') else ''} ({c['confidence']:.2f})")
    
    # MÉTODOS AUXILIARES
    
    def add_score(self, violence_type, subtype, score, explanations=None):
        """
        Adiciona pontuação a um tipo/subtipo de violência.
        
        Args:
            violence_type: Tipo principal de violência
            subtype: Subtipo (se aplicável)
            score: Pontuação a adicionar
            explanations: Lista de explicações sobre por que a pontuação foi adicionada
        """
        # Gerar chave única para este tipo/subtipo
        key = f"{violence_type}_{subtype}" if subtype else violence_type
        
        # Verificar se já existe uma classificação para este tipo/subtipo
        existing = None
        for fact_id in self.get_matching_facts(ViolenceClassification):
            fact = self.facts[fact_id]
            if fact["violence_type"] == violence_type and fact["subtype"] == subtype:
                existing = fact_id
                break
        
        # Armazenar explicações
        if explanations:
            if key not in self.explanations:
                self.explanations[key] = []
            self.explanations[key].extend(explanations)
        
        # Limiar e pontuação máxima para calcular confiança
        threshold = get_threshold(violence_type, subtype)
        max_score = get_max_score(violence_type, subtype)
        
        if existing:
            # Atualizar classificação existente
            fact = self.facts[existing]
            new_score = fact["score"] + score
            confidence = calculate_confidence(new_score, threshold, max_score)
            self.modify(existing, score=new_score, confidence_level=confidence)
            print(f"📊 Atualizado {key}: score={new_score}, confiança={confidence:.2f}")
        else:
            # Criar nova classificação
            confidence = calculate_confidence(score, threshold, max_score)
            self.declare(
                ViolenceClassification(
                    violence_type=violence_type,
                    subtype=subtype,
                    score=score,
                    confidence_level=confidence
                )
            )
            print(f"📊 Criado {key}: score={score}, confiança={confidence:.2f}")
    
    def get_explanation(self, violence_type, subtype=None):
        """
        Recupera explicações armazenadas para um tipo/subtipo.
        
        Args:
            violence_type: Tipo principal de violência
            subtype: Subtipo (se aplicável)
            
        Returns:
            List: Lista de explicações ou lista vazia se não houver
        """
        key = f"{violence_type}_{subtype}" if subtype else violence_type
        return self.explanations.get(key, [])