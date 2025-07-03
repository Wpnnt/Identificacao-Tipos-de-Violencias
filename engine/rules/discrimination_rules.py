from experta.rule import Rule
from experta import OR
from .base_engine import BaseViolenceEngine
from ..facts import (
    ViolenceBehavior, KeywordFact, TargetFact, FrequencyFact, ProcessingPhase
)


class DiscriminationRulesMixin:
    """
    Mixin contendo regras específicas para identificação de diferentes tipos de discriminação.
    """

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
        """Detecta discriminação flagrante baseada em gênero ou orientação sexual."""
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
        """Detecta discriminação sutil baseada em gênero."""
        self.create_classification("discriminacao_genero", "discriminacao_sutil", [
            "Identificado comportamento de questionamento de capacidade",
            "Direcionado a características de gênero",
            "Ocorre repetidamente ou continuamente"
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
        """Detecta discriminação racial direta."""
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
        """Detecta ofensa racial."""
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
        """Detecta insulto racial direto."""
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
        """Detecta comportamento de insulto racial."""
        self.create_classification("discriminacao_racial", "ofensa_direta", [
            "Identificado comportamento de insulto racial",
            "Direcionado à raça/etnia da vítima"
        ])

    @Rule(
        ProcessingPhase(phase="analysis"),
        KeywordFact(category="action_type", keyword="insulto_racial")
    )
    def detect_insulto_racial_simples(self):
        """Detecta menção simples a insulto racial."""
        self.create_classification("discriminacao_racial", "ofensa_direta", [
            "Identificada menção a insulto racial"
        ])

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
        """Detecta ofensa religiosa direta."""
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
        """Detecta discriminação religiosa institucional."""
        self.create_classification("discriminacao_religiosa", "discriminacao_institucional", [
            "Identificado impedimento de práticas religiosas"
        ])

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
        """Detecta gordofobia direta."""
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
        """Detecta gordofobia estrutural."""
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
        """Detecta capacitismo por barreiras físicas."""
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
        """Detecta capacitismo por barreiras atitudinais."""
        self.create_classification("capacitismo", "barreiras_atitudinais", [
            "Identificado comportamento de infantilização",
            "Direcionado a pessoa com deficiência"
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
        """Detecta discriminação regional."""
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
        """Detecta xenofobia internacional."""
        self.create_classification("xenofobia", "xenofobia_internacional", [
            "Identificada discriminação baseada em origem",
            "Direcionada à origem estrangeira da vítima"
        ])
