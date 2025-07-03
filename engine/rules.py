import inspect  # Adicionar esta importação
from experta.engine import KnowledgeEngine
from experta import Fact
from experta.rule import Rule
from experta.deffacts import DefFacts
from experta import TEST, AS, OR, NOT, AND
from typing import Dict, List, Any, Optional

from .facts import (
    TextRelato, KeywordFact, ViolenceBehavior, ContextFact, FrequencyFact,
    TargetFact, RelationshipFact, ImpactFact, ViolenceClassification,
    AnalysisResult, ProcessingPhase
)

from knowledge_base.violence_types import VIOLENCE_TYPES

class ViolenceRules(KnowledgeEngine):
    """
    Motor de regras para identificação de tipos de violência.
    """

    def __init__(self):
        super().__init__()
        self.explanations = {}

    @DefFacts()
    def initial_facts(self):
        """Define os fatos iniciais, incluindo a fase inicial de coleta."""
        yield Fact(engine_ready=True)
        yield ProcessingPhase(phase="collection")  # Fase inicial: coleta de fatos

    @Rule(ProcessingPhase(phase="collection"))
    def start_analysis_phase(self):
        """
        Transição da fase de coleta para a fase de análise.
        Esta regra dispara após todos os fatos serem declarados.
        """
        print("🔄 Transitando para fase de análise...")
        # Remover a fase de coleta
        for fact_id in self.get_matching_facts(ProcessingPhase):
            self.retract(fact_id)
        # Declarar a fase de análise
        self.declare(ProcessingPhase(phase="analysis"))

    @Rule(Fact(engine_ready=True))
    def rule_diagnostic(self):
        print("✅ DIAGNÓSTICO: Motor de regras funcionando!")

    # MICROAGRESSÕES

    @Rule(
        ProcessingPhase(phase="analysis"),
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
        # Coletar os fatos que dispararam esta regra
        facts_used = {}
        
        # Verificar comportamentos identificados
        behaviors = []
        for fact_id in self.get_matching_facts(ViolenceBehavior):
            behavior = self.facts[fact_id]["behavior_type"]
            if behavior == "interrupcao":
                behaviors.append(behavior)
        
        if behaviors:
            facts_used["behavior"] = behaviors
            
        # Verificar frequências identificadas
        frequencies = []
        for fact_id in self.get_matching_facts(FrequencyFact):
            freq = self.facts[fact_id]["value"]
            if freq in ["repetidamente", "continuamente"]:
                frequencies.append(freq)
        
        if frequencies:
            facts_used["frequency"] = frequencies
            
        # Raciocínio específico para esta regra
        reasoning = "A interrupção sistemática e repetida de falas é uma forma sutil mas danosa de microagressão, que pode silenciar vozes e diminuir a participação de determinados grupos em ambientes acadêmicos ou profissionais."
        
        # Criar classificação com explicações detalhadas
        self.create_classification(
            "microagressoes", 
            "interrupcoes_constantes", 
            facts_used=facts_used,
            reasoning=reasoning
        )

    @Rule(
        ProcessingPhase(phase="analysis"),
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
        facts_used = {}
        
        # Verificar comportamentos identificados
        behaviors = []
        for fact_id in self.get_matching_facts(ViolenceBehavior):
            behavior = self.facts[fact_id]["behavior_type"]
            if behavior == "questionamento_capacidade":
                behaviors.append(behavior)
        
        if behaviors:
            facts_used["behavior"] = behaviors
            
        # Verificar características do alvo
        targets = []
        for fact_id in self.get_matching_facts(TargetFact):
            target = self.facts[fact_id]["characteristic"]
            if target == "genero":
                targets.append(target)
        
        if targets:
            facts_used["target"] = targets
            
        reasoning = "O questionamento recorrente da capacidade baseado em gênero é uma forma de discriminação que afeta a confiança da vítima e reforça estereótipos prejudiciais no ambiente acadêmico ou profissional."
        
        self.create_classification(
            "microagressoes", 
            "questionar_julgamento", 
            facts_used=facts_used,
            reasoning=reasoning
        )

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="comentarios_saude_mental"),
            KeywordFact(category="action_type", keyword="comentarios_saude_mental")
        )
    )
    def detect_comentarios_saude_mental(self):
        self.create_classification("microagressoes", "comentarios_saude_mental", [
            "Identificados comentários relacionados à saúde mental"
        ])

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="piadas_estereotipos"),
            KeywordFact(category="action_type", keyword="piadas_estereotipos")
        )
    )
    def detect_estereotipos(self):
        self.create_classification("microagressoes", "estereotipos", [
            "Identificadas piadas ou comentários baseados em estereótipos"
        ])

    # PERSEGUIÇÃO

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="perseguicao"),
            KeywordFact(category="action_type", keyword="perseguicao")
        )
    )
    def detect_perseguicao(self):
        facts_used = {}
        
        # Verificar comportamentos identificados
        behaviors = []
        for fact_id in self.get_matching_facts(ViolenceBehavior):
            behavior = self.facts[fact_id]["behavior_type"]
            if behavior == "perseguicao":
                behaviors.append(behavior)
        
        if behaviors:
            facts_used["behavior"] = behaviors
        
        reasoning = "A perseguição é uma forma de violência que viola a privacidade e gera insegurança para a vítima, podendo evoluir para formas mais graves de violência se não for contida a tempo."
        
        self.create_classification(
            "perseguicao", 
            None, 
            facts_used=facts_used,
            reasoning=reasoning
        )

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="perseguicao"),
            KeywordFact(category="action_type", keyword="perseguicao")
        ),
        OR(
            ImpactFact(type="medo_inseguranca"),
            KeywordFact(category="impact", keyword="medo_inseguranca")
        )
    )
    def detect_perseguicao_com_medo(self):
        facts_used = {}
        
        # Verificar comportamentos identificados
        behaviors = []
        for fact_id in self.get_matching_facts(ViolenceBehavior):
            behavior = self.facts[fact_id]["behavior_type"]
            if behavior == "perseguicao":
                behaviors.append(behavior)
        
        if behaviors:
            facts_used["behavior"] = behaviors
        
        # Verificar impactos identificados
        impacts = []
        for fact_id in self.get_matching_facts(ImpactFact):
            impact = self.facts[fact_id]["type"]
            if impact == "medo_inseguranca":
                impacts.append(impact)
        
        if impacts:
            facts_used["impact"] = impacts
            
        reasoning = "A perseguição que causa medo e insegurança configura uma violação grave da liberdade e bem-estar psicológico da vítima, constituindo situação de alto risco que pode requerer intervenção policial."
        
        self.create_classification(
            "perseguicao", 
            None, 
            facts_used=facts_used,
            reasoning=reasoning
        )

    # DISCRIMINAÇÃO DE GÊNERO

    @Rule(
        ProcessingPhase(phase="analysis"),
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
        self.create_classification("discriminacao_genero", "discriminacao_flagrante", [
            "Identificado comportamento de exclusão",
            "Direcionado a características de gênero ou orientação sexual"
        ])

    @Rule(
        ProcessingPhase(phase="analysis"),
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
        self.create_classification("discriminacao_genero", "discriminacao_sutil", [
            "Identificado comportamento de questionamento de capacidade",
            "Direcionado a características de gênero",
            "Ocorre repetidamente ou continuamente"
        ])

    # ABUSO PSICOLÓGICO

    @Rule(
        ProcessingPhase(phase="analysis"),
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
        self.create_classification("abuso_psicologico", None, [
            "Identificado comportamento de ameaça, humilhação ou constrangimento"
        ])

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="ameaca"),
            ViolenceBehavior(behavior_type="humilhacao"),
            KeywordFact(category="action_type", keyword="ameaca"),
            KeywordFact(category="action_type", keyword="humilhacao")
        ),
        OR(
            RelationshipFact(type="relacao_hierarquica"),
        )
    )
    def detect_abuso_psicologico_hierarquico(self):
        facts_used = {}
        
        # Verificar comportamentos identificados
        behaviors = []
        for fact_id in self.get_matching_facts(ViolenceBehavior):
            behavior = self.facts[fact_id]["behavior_type"]
            if behavior in ["ameaca", "humilhacao"]:
                behaviors.append(behavior)
        
        if behaviors:
            facts_used["behavior"] = behaviors
            
        # Verificar relacionamentos identificados
        relationships = []
        for fact_id in self.get_matching_facts(RelationshipFact):
            rel = self.facts[fact_id]["type"]
            if rel == "relacao_hierarquica":
                relationships.append(rel)
        
        if relationships:
            facts_used["relationship"] = relationships
            
        reasoning = "O abuso psicológico em relações hierárquicas é particularmente grave, pois envolve desequilíbrio de poder que dificulta a defesa da vítima e pode comprometer sua situação acadêmica ou profissional."
        
        self.create_classification(
            "abuso_psicologico", 
            None, 
            facts_used=facts_used,
            reasoning=reasoning
        )

    # ASSÉDIO MORAL DE GÊNERO

    @Rule(
        ProcessingPhase(phase="analysis"),
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
        facts_used = {}
        
        # Verificar comportamentos identificados
        behaviors = []
        for fact_id in self.get_matching_facts(ViolenceBehavior):
            behavior = self.facts[fact_id]["behavior_type"]
            if behavior == "pressao_tarefas":
                behaviors.append(behavior)
        
        if behaviors:
            facts_used["behavior"] = behaviors
            
        # Verificar características do alvo
        targets = []
        for fact_id in self.get_matching_facts(TargetFact):
            target = self.facts[fact_id]["characteristic"]
            if target == "genero":
                targets.append(target)
        
        if targets:
            facts_used["target"] = targets
            
        # Verificar contexto identificado
        contexts = []
        for fact_id in self.get_matching_facts(ContextFact):
            context = self.facts[fact_id]["location"]
            if context == "local_trabalho":
                contexts.append(context)
        
        if contexts:
            facts_used["context"] = contexts
            
        reasoning = "O assédio moral baseado em gênero no ambiente de trabalho constitui uma forma de discriminação institucionalizada que prejudica o desenvolvimento profissional da vítima e viola seus direitos trabalhistas."
        
        self.create_classification(
            "assedio_moral_genero", 
            None, 
            facts_used=facts_used,
            reasoning=reasoning
        )

    # VIOLÊNCIA SEXUAL

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="natureza_sexual_nao_consentido"),
            KeywordFact(category="action_type", keyword="natureza_sexual_nao_consentido")
        )
    )
    def detect_assedio_sexual(self):
        facts_used = {}
        
        # Verificar comportamentos identificados
        behaviors = []
        for fact_id in self.get_matching_facts(ViolenceBehavior):
            behavior = self.facts[fact_id]["behavior_type"]
            if behavior == "natureza_sexual_nao_consentido":
                behaviors.append(behavior)
        
        if behaviors:
            facts_used["behavior"] = behaviors
            
        reasoning = "O assédio sexual viola a dignidade e liberdade sexual da vítima, criando um ambiente hostil e constrangedor, podendo configurar crime conforme a Lei nº 10.224/2001."
        
        self.create_classification(
            "violencia_sexual", 
            "assedio_sexual", 
            facts_used=facts_used,
            reasoning=reasoning
        )

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="contato_fisico_nao_consentido"),
            ViolenceBehavior(behavior_type="ato_obsceno"),
            KeywordFact(category="action_type", keyword="contato_fisico_nao_consentido"),
            KeywordFact(category="action_type", keyword="ato_obsceno")
        )
    )
    def detect_importunacao_sexual(self):
        facts_used = {}
        
        # Verificar comportamentos identificados
        behaviors = []
        for fact_id in self.get_matching_facts(ViolenceBehavior):
            behavior = self.facts[fact_id]["behavior_type"]
            if behavior in ["contato_fisico_nao_consentido", "ato_obsceno"]:
                behaviors.append(behavior)
        
        if behaviors:
            facts_used["behavior"] = behaviors
        
        # Verificar contexto, se presente
        contexts = []
        for fact_id in self.get_matching_facts(ContextFact):
            contexts.append(self.facts[fact_id]["location"])
        
        if contexts:
            facts_used["context"] = contexts
        
        # Verificar relacionamento, se presente
        relationships = []
        for fact_id in self.get_matching_facts(RelationshipFact):
            relationships.append(self.facts[fact_id]["type"])
        
        if relationships:
            facts_used["relationship"] = relationships
        
        reasoning = "A importunação sexual constitui crime previsto no artigo 215-A do Código Penal, incluindo toques corporais não consentidos e atos libidinosos em ambiente público, com pena de reclusão de 1 a 5 anos."
        
        self.create_classification(
            "violencia_sexual", 
            "importunacao_sexual", 
            facts_used=facts_used,
            reasoning=reasoning
        )

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="coercao_sexual"),
            KeywordFact(category="action_type", keyword="coercao_sexual")
        ),
        OR(
            ImpactFact(type="medo_inseguranca"),
            KeywordFact(category="impact", keyword="medo_inseguranca")
        )
    )
    def detect_estupro(self):
        facts_used = {}
        
        # Verificar comportamentos identificados
        behaviors = []
        for fact_id in self.get_matching_facts(ViolenceBehavior):
            behavior = self.facts[fact_id]["behavior_type"]
            if behavior == "coercao_sexual":
                behaviors.append(behavior)
        
        if behaviors:
            facts_used["behavior"] = behaviors
            
        # Verificar impactos identificados
        impacts = []
        for fact_id in self.get_matching_facts(ImpactFact):
            impact = self.facts[fact_id]["type"]
            if impact == "medo_inseguranca":
                impacts.append(impact)
        
        if impacts:
            facts_used["impact"] = impacts
            
        reasoning = "A coerção sexual que gera medo e insegurança pode configurar estupro (art. 213 do Código Penal), crime hediondo que requer denúncia imediata às autoridades e atendimento especializado à vítima."
        
        self.create_classification(
            "violencia_sexual", 
            "estupro", 
            facts_used=facts_used,
            reasoning=reasoning
        )

    # GORDOFOBIA

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="comentarios_sobre_peso"),
            ViolenceBehavior(behavior_type="piadas_sobre_peso"),
            KeywordFact(category="action_type", keyword="comentarios_sobre_peso"),
            KeywordFact(category="action_type", keyword="piadas_sobre_peso")
        )
    )
    def detect_gordofobia_direta(self):
        self.create_classification("gordofobia", "discriminacao_direta", [
            "Identificados comentários ou piadas sobre peso/corpo"
        ])

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="exclusao_por_peso"),
            KeywordFact(category="action_type", keyword="exclusao_por_peso")
        )
    )
    def detect_gordofobia_estrutural(self):
        self.create_classification("gordofobia", "discriminacao_estrutural", [
            "Identificada exclusão baseada em peso/aparência física"
        ])

    # CAPACITISMO

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="negacao_acessibilidade"),
            KeywordFact(category="action_type", keyword="negacao_acessibilidade")
        )
    )
    def detect_barreiras_fisicas(self):
        self.create_classification("capacitismo", "barreiras_fisicas", [
            "Identificada negação de acessibilidade ou barreiras físicas"
        ])

    @Rule(
        ProcessingPhase(phase="analysis"),
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
        self.create_classification("capacitismo", "barreiras_atitudinais", [
            "Identificado comportamento de infantilização",
            "Direcionado a pessoa com deficiência"
        ])

    # VIOLÊNCIA DIGITAL

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="cyberbullying"),
            KeywordFact(category="action_type", keyword="cyberbullying")
        )
    )
    def detect_cyberbullying(self):
        self.create_classification("violencia_digital", "cyberbullying", [
            "Identificado comportamento de cyberbullying"
        ])

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="exposicao_conteudo"),
            KeywordFact(category="action_type", keyword="exposicao_conteudo")
        )
    )
    def detect_exposicao_nao_consentida(self):
        facts_used = {}
        
        # Verificar comportamentos identificados
        behaviors = []
        for fact_id in self.get_matching_facts(ViolenceBehavior):
            behavior = self.facts[fact_id]["behavior_type"]
            if behavior == "exposicao_conteudo":
                behaviors.append(behavior)
        
        if behaviors:
            facts_used["behavior"] = behaviors
            
        reasoning = "A exposição não consentida de conteúdo íntimo configura crime conforme a Lei nº 13.718/2018, com pena de reclusão de 1 a 5 anos, requerendo registro de Boletim de Ocorrência em Delegacia Especializada de Crimes Digitais."
        
        self.create_classification(
            "violencia_digital", 
            "exposicao_nao_consentida", 
            facts_used=facts_used,
            reasoning=reasoning
        )

    # DISCRIMINAÇÃO RELIGIOSA

    @Rule(
        ProcessingPhase(phase="analysis"),
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
        self.create_classification("discriminacao_religiosa", "ofensa_direta", [
            "Identificada zombaria ou piadas sobre religião",
            "Direcionada a características religiosas da vítima"
        ])

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="impedimento_pratica_religiosa"),
            KeywordFact(category="action_type", keyword="impedimento_pratica_religiosa")
        )
    )
    def detect_discriminacao_religiosa_institucional(self):
        self.create_classification("discriminacao_religiosa", "discriminacao_institucional", [
            "Identificado impedimento de práticas religiosas"
        ])

    # XENOFOBIA

    @Rule(
        ProcessingPhase(phase="analysis"),
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
        self.create_classification("xenofobia", "discriminacao_regional", [
            "Identificadas piadas ou comentários sobre sotaque",
            "Direcionados à origem regional da vítima"
        ])

    @Rule(
        ProcessingPhase(phase="analysis"),
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
        self.create_classification("xenofobia", "xenofobia_internacional", [
            "Identificada discriminação baseada em origem",
            "Direcionada à origem estrangeira da vítima"
        ])

    # DISCRIMINAÇÃO RACIAL

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="insulto"),
            ViolenceBehavior(behavior_type="piadas_estereotipos"),
            KeywordFact(category="action_type", keyword="insulto"),
            KeywordFact(category="action_type", keyword="piadas_estereotipos")
        ),
        OR(
            TargetFact(characteristic="raca_etnia"),
            KeywordFact(category="target", keyword="raca_etnia")
        )
    )
    def detect_discriminacao_racial_direta(self):
        facts_used = {}
        
        # Verificar comportamentos identificados
        behaviors = []
        for fact_id in self.get_matching_facts(ViolenceBehavior):
            behavior = self.facts[fact_id]["behavior_type"]
            if behavior in ["insulto", "piadas_estereotipos"]:
                behaviors.append(behavior)
        
        if behaviors:
            facts_used["behavior"] = behaviors
            
        # Verificar características do alvo
        targets = []
        for fact_id in self.get_matching_facts(TargetFact):
            target = self.facts[fact_id]["characteristic"]
            if target == "raca_etnia":
                targets.append(target)
        
        if targets:
            facts_used["target"] = targets
            
        reasoning = "A discriminação racial direta por meio de insultos ou estereótipos configura crime de racismo ou injúria racial, conforme a Lei 7.716/89 e art. 140 do Código Penal, sendo inafiançável e imprescritível."
        
        self.create_classification(
            "discriminacao_racial", 
            "ofensa_direta", 
            facts_used=facts_used,
            reasoning=reasoning
        )

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            KeywordFact(category="action_type", keyword="insulto_racial")
        ),
        OR(
            TargetFact(characteristic="raca_etnia"),
            KeywordFact(category="target", keyword="raca_etnia")
        )
    )
    def detect_discriminacao_racial_ofensa(self):
        self.create_classification("discriminacao_racial", "ofensa_direta", [
            "Identificada ofensa verbal de natureza racial",
            "Direcionada à raça/etnia da vítima"
        ])

    @Rule(
        ProcessingPhase(phase="analysis"),
        KeywordFact(category="action_type", keyword="insulto_racial"),
        TargetFact(characteristic="raca_etnia")
    )
    def detect_discriminacao_racial_direta_insulto(self):
        self.create_classification("discriminacao_racial", "ofensa_direta", [
            "Identificada ofensa verbal explícita de natureza racial",
            "Direcionada especificamente à raça/etnia da vítima"
        ])

    @Rule(
        ProcessingPhase(phase="analysis"),
        ViolenceBehavior(behavior_type="insulto_racial"),
        OR(
            TargetFact(characteristic="raca_etnia"),
            KeywordFact(category="target", keyword="raca_etnia")
        )
    )
    def detect_discriminacao_racial_comportamento(self):
        self.create_classification("discriminacao_racial", "ofensa_direta", [
            "Identificado comportamento de insulto racial",
            "Direcionado à raça/etnia da vítima"
        ])

    @Rule(
        ProcessingPhase(phase="analysis"),
        KeywordFact(category="action_type", keyword="insulto_racial")
    )
    def detect_insulto_racial_simples(self):
        self.create_classification("discriminacao_racial", "ofensa_direta", [
            "Identificada menção a insulto racial"
        ])

    # Método para criar classificações
    def create_classification(self, violence_type, subtype=None, explanations=None, facts_used=None, reasoning=None):
        """
        Cria uma classificação de violência com explicações detalhadas.
        
        Args:
            violence_type: Tipo principal de violência
            subtype: Subtipo de violência (opcional)
            explanations: Lista de explicações básicas (opcional)
            facts_used: Dicionário dos fatos que dispararam a regra (opcional)
            reasoning: Explicação adicional do raciocínio (opcional)
        """
        # Garantir que subtype nunca seja None para consistência
        subtype = subtype or ""
        
        # Verificar se já existe uma classificação para este tipo/subtipo
        for fact_id in self.get_matching_facts(ViolenceClassification):
            fact = self.facts[fact_id]
            if fact["violence_type"] == violence_type and fact["subtype"] == subtype:
                # Já existe, não precisamos criar outra
                return
        
        # Armazenar explicações, evitando duplicações
        key = f"{violence_type}_{subtype}" if subtype else violence_type
        
        # Se temos fatos usados, gerar explicação detalhada
        if facts_used:
            rule_name = inspect.currentframe().f_back.f_code.co_name
            conclusion = f"{violence_type}" + (f" do tipo {subtype}" if subtype else "")
            detailed_explanations = self.format_detailed_explanation(rule_name, facts_used, conclusion, reasoning)
            
            if key not in self.explanations:
                self.explanations[key] = []
                
            # Adicionar explicações detalhadas
            for explanation in detailed_explanations:
                if explanation not in self.explanations[key]:
                    self.explanations[key].append(explanation)
        # Caso contrário, usar explicações simples fornecidas
        elif explanations:
            if key not in self.explanations:
                self.explanations[key] = []
                
            # Adicionar explicações simples
            for explanation in explanations:
                if explanation not in self.explanations[key]:
                    self.explanations[key].append(explanation)
        
        # Criar nova classificação
        self.declare(
            ViolenceClassification(
                violence_type=violence_type,
                subtype=subtype,
                explanation=self.explanations.get(key, []).copy()  # Usar a lista completa e atual
            )
        )
        print(f"📊 Criado {key}")
    
    def run(self, steps=None):
        """
        Executa o motor em modo controlado por fases.
        """
        print("🚀 Iniciando motor de inferência com controle de fases")
        steps_value = -1 if steps is None else steps
        
        # Limitar o número máximo de iterações para evitar loops infinitos
        max_iterations = 100
        iteration = 0
        
        # Executar até que não haja mais regras para disparar ou atingir limite
        while self.agenda and iteration < max_iterations:
            super().run(1)  # Executar apenas uma regra por vez
            iteration += 1
            
            # Sair se não houver mais regras para acionar
            if not self.agenda:
                break
        
        print("\n🔄 Consolidando resultados...")
        self.consolidate_results()

    def consolidate_results(self):
        """
        Consolida os resultados de todas as classificações.
        """
        all_classifications = []
        for fact_id in self.get_matching_facts(ViolenceClassification):
            fact = self.facts[fact_id]
            all_classifications.append({
                "violence_type": fact["violence_type"],
                "subtype": fact["subtype"] or "",
                "explanation": self.get_explanation(fact["violence_type"], fact["subtype"])
            })
        
        if not all_classifications:
            print("⚠️ Nenhuma classificação identificada, criando resultado vazio")
            self.declare(
                AnalysisResult(
                    classifications=[],
                    primary_result={"violence_type": "", "subtype": ""},
                    multiple_types=False
                )
            )
            return
        
        # Reportar múltiplos se houver mais de um
        report_multiple = len(all_classifications) > 1
        
        # Primeiro resultado como principal
        primary_result = all_classifications[0]

        self.declare(
            AnalysisResult(
                classifications=all_classifications,
                primary_result=primary_result,
                multiple_types=report_multiple
            )
        )

        print("\n✅ Análise consolidada:")
        print(f"- Resultado principal: {primary_result['violence_type']}{' - ' + primary_result['subtype'] if primary_result.get('subtype') else ''}")
        print(f"- Reportar múltiplos: {report_multiple}")
        
    def get_explanation(self, violence_type, subtype=None):
        """
        Recupera explicações armazenadas para um tipo/subtipo.
        """
        key = f"{violence_type}_{subtype}" if subtype else violence_type
        return self.explanations.get(key, [])
    
    def get_matching_facts(self, fact_type):
        """
        Retorna os IDs dos fatos que correspondem ao tipo especificado.
        """
        return [fact_id for fact_id, fact in self.facts.items() 
                if isinstance(fact, fact_type)]
    
    def debug_facts(self):
        """
        Exibe os fatos presentes para diagnóstico.
        """
        print("\n=== DEBUG: Fatos presentes no motor ===")
        for fact_id, fact in self.facts.items():
            print(f"- {fact_id}: {fact}")

    def reset(self):
        """
        Reinicia completamente o motor, limpando todos os fatos e explicações.
        """
        # Limpar explicações
        self.explanations = {}
        
        # Chamar o reset original
        super().reset()
        print("🔄 Motor de regras reiniciado completamente")

    def format_detailed_explanation(self, rule_name, facts_used, conclusion, reasoning=None):
        """
        Gera uma explicação detalhada em linguagem natural baseada nos fatos que ativaram a regra.
        
        Args:
            rule_name: Nome da regra ativada
            facts_used: Dicionário dos fatos relevantes que ativaram a regra
            conclusion: A conclusão alcançada pela regra
            reasoning: Explicação adicional do raciocínio (opcional)
        """
        basic_explanation = []
        detailed_explanation = []
        
        # Criar explicação básica
        basic_explanation.append(f"Identificado: {conclusion}")
        
        # Construir uma explicação detalhada baseada nos fatos utilizados
        detailed_explanation.append(f"**Como chegamos a esta conclusão:**")
        
        # Explicar os comportamentos identificados
        if 'behavior' in facts_used:
            behaviors = facts_used['behavior']
            behavior_text = ", ".join(behaviors) if len(behaviors) > 1 else behaviors[0]
            detailed_explanation.append(f"- Identificamos em seu relato comportamentos de {behavior_text}")
        
        # Explicar o contexto, se houver
        if 'context' in facts_used:
            contexts = facts_used['context']
            context_text = ", ".join(contexts) if len(contexts) > 1 else contexts[0]
            detailed_explanation.append(f"- O incidente ocorreu em um contexto de {context_text}")
        
        # Explicar a frequência, se houver
        if 'frequency' in facts_used:
            frequencies = facts_used['frequency']
            freq_text = ", ".join(frequencies) if len(frequencies) > 1 else frequencies[0]
            detailed_explanation.append(f"- O comportamento ocorre {freq_text}")
        
        # Explicar as características do alvo, se houver
        if 'target' in facts_used:
            targets = facts_used['target']
            target_text = ", ".join(targets) if len(targets) > 1 else targets[0]
            detailed_explanation.append(f"- O comportamento foi direcionado com base em {target_text}")
        
        # Explicar o relacionamento, se houver
        if 'relationship' in facts_used:
            relationships = facts_used['relationship']
            rel_text = ", ".join(relationships) if len(relationships) > 1 else relationships[0]
            detailed_explanation.append(f"- Existe uma relação de {rel_text} entre as partes envolvidas")
        
        # Explicar o impacto, se houver
        if 'impact' in facts_used:
            impacts = facts_used['impact']
            impact_text = ", ".join(impacts) if len(impacts) > 1 else impacts[0]
            detailed_explanation.append(f"- O comportamento causou {impact_text}")
        
        # Adicionar raciocínio específico se fornecido
        if reasoning:
            detailed_explanation.append(f"\n**Por que isso é importante:** {reasoning}")
        
        return basic_explanation + detailed_explanation