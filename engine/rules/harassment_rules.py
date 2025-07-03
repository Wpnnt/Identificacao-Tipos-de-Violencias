from experta.rule import Rule
from experta import OR
from .base_engine import BaseViolenceEngine
from ..facts import (
    ViolenceBehavior, KeywordFact, ImpactFact, TargetFact, ContextFact,
    RelationshipFact, ProcessingPhase
)


class HarassmentRulesMixin:
    """
    Mixin contendo regras específicas para identificação de assédio e perseguição.
    """

    # PERSEGUIÇÃO
    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="perseguicao"),
            KeywordFact(category="action_type", keyword="perseguicao")
        )
    )
    def detect_perseguicao(self):
        """Detecta perseguição."""
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
        """Detecta perseguição que causa medo e insegurança."""
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
        """Detecta abuso psicológico."""
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
        """Detecta abuso psicológico em relação hierárquica."""
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
        """Detecta assédio moral baseado em gênero no ambiente de trabalho."""
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
