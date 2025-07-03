from experta.engine import KnowledgeEngine
from experta import Fact
from experta.rule import Rule
from experta.deffacts import DefFacts
from experta import TEST, AS, OR, NOT, AND
from typing import Dict, List, Any, Optional

# Importações dos fatos necessários para o motor de regras
from .facts import (
    TextRelato, KeywordFact, ViolenceBehavior, ContextFact, FrequencyFact,
    TargetFact, RelationshipFact, ImpactFact, ViolenceClassification,
    AnalysisResult
)
from knowledge_base.violence_types import VIOLENCE_TYPES

class ViolenceRules(KnowledgeEngine):
    """
    Motor de regras para identificação de tipos de violência.
    """
    
    def __init__(self):
        """Inicializa o motor de regras."""
        super().__init__()
        self.explanations = {}  # Armazena explicações para cada classificação
    
    @DefFacts()
    def initial_facts(self):
        yield Fact(engine_ready=True)
    
    @Rule(Fact(engine_ready=True))
    def rule_diagnostic(self):
        """Regra de diagnóstico para verificar o funcionamento do motor."""
        print("✅ DIAGNÓSTICO: Motor de regras funcionando!")
        
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
        self.create_classification("microagressoes", "interrupcoes_constantes", [
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
        self.create_classification("microagressoes", "questionar_julgamento", [
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
        self.create_classification("microagressoes", "comentarios_saude_mental", [
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
        self.create_classification("microagressoes", "estereotipos", [
            "Identificadas piadas ou comentários baseados em estereótipos"
        ])
    
    # REGRAS PARA PERSEGUIÇÃO
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="perseguicao"),
            KeywordFact(category="action_type", keyword="perseguicao")
        )
    )
    def detect_perseguicao(self):
        """Detecta comportamento de perseguição."""
        self.create_classification("perseguicao", None, [
            "Identificado comportamento de perseguição"
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
        self.create_classification("perseguicao", None, [
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
        self.create_classification("discriminacao_genero", "discriminacao_flagrante", [
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
        self.create_classification("discriminacao_genero", "discriminacao_sutil", [
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
        self.create_classification("abuso_psicologico", None, [
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
            RelationshipFact(type="relacao_hierarquica"),
        )
    )
    def detect_abuso_psicologico_hierarquico(self):
        """Detecta abuso psicológico com relação hierárquica."""
        self.create_classification("abuso_psicologico", None, [
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
        self.create_classification("assedio_moral_genero", None, [
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
        self.create_classification("violencia_sexual", "assedio_sexual", [
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
        self.create_classification("violencia_sexual", "importunacao_sexual", [
            "Identificado contato físico não consentido ou ato obsceno"
        ])
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="coercao_sexual"),
            KeywordFact(category="action_type", keyword="coercao_sexual")
        )
    )
    def detect_estupro(self):
        """Detecta estupro."""
        self.create_classification("violencia_sexual", "estupro", [
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
        self.create_classification("gordofobia", "discriminacao_direta", [
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
        self.create_classification("gordofobia", "discriminacao_estrutural", [
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
        self.create_classification("capacitismo", "barreiras_fisicas", [
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
        self.create_classification("capacitismo", "barreiras_atitudinais", [
            "Identificado comportamento de infantilização",
            "Direcionado a pessoa com deficiência"
        ])
    
    # REGRAS PARA VIOLÊNCIA DIGITAL
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="cyberbullying"),
            KeywordFact(category="action_type", keyword="cyberbullying")
        )
    )
    def detect_cyberbullying(self):
        """Detecta cyberbullying."""
        self.create_classification("violencia_digital", "cyberbullying", [
            "Identificado comportamento de cyberbullying"
        ])
    
    @Rule(
        OR(
            ViolenceBehavior(behavior_type="exposicao_conteudo"),
            KeywordFact(category="action_type", keyword="exposicao_conteudo")
        )
    )
    def detect_exposicao_nao_consentida(self):
        """Detecta exposição não consentida."""
        self.create_classification("violencia_digital", "exposicao_nao_consentida", [
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
        self.create_classification("discriminacao_religiosa", "ofensa_direta", [
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
        self.create_classification("discriminacao_religiosa", "discriminacao_institucional", [
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
        self.create_classification("xenofobia", "discriminacao_regional", [
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
        self.create_classification("xenofobia", "xenofobia_internacional", [
            "Identificada discriminação baseada em origem",
            "Direcionada à origem estrangeira da vítima"
        ])

    # REGRAS PARA DISCRIMINAÇÃO RACIAL

    @Rule(
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
        self.create_classification("discriminacao_racial", "ofensa_direta", [
            "Identificado insulto ou comentário pejorativo",
            "Direcionado à raça/etnia da vítima"
        ])


    @Rule(
        OR(
            KeywordFact(category="action_type", keyword="insulto_racial")
        ),
        OR(
            TargetFact(characteristic="raca_etnia"),
            KeywordFact(category="target", keyword="raca_etnia")
        )
    )
    def detect_discriminacao_racial_ofensa(self):
        """Detecta discriminação racial por ofensa direta."""
        self.create_classification("discriminacao_racial", "ofensa_direta", [
            "Identificada ofensa verbal de natureza racial",
            "Direcionada à raça/etnia da vítima"
        ])
        
    # Método simplificado para criar classificações
    def create_classification(self, violence_type, subtype=None, explanations=None):
        """
        Cria uma classificação de violência.
        
        Args:
            violence_type: Tipo principal de violência
            subtype: Subtipo de violência (opcional)
            explanations: Lista de explicações sobre a classificação (opcional)
        """
        # Garantir que subtype nunca seja None para consistência
        subtype = subtype or ""
        
        # Verificar se já existe uma classificação para este tipo/subtipo
        for fact_id in self.get_matching_facts(ViolenceClassification):
            fact = self.facts[fact_id]
            if fact["violence_type"] == violence_type and fact["subtype"] == subtype:
                # Já existe, não precisamos criar outra
                return
        
        # Armazenar explicações
        key = f"{violence_type}_{subtype}" if subtype else violence_type
        if explanations:
            if key not in self.explanations:
                self.explanations[key] = []
            self.explanations[key].extend(explanations)
        
        # Criar nova classificação (sem score ou confidence)
        self.declare(
            ViolenceClassification(
                violence_type=violence_type,
                subtype=subtype,
                explanation=explanations or []
            )
        )
        print(f"📊 Criado {key}")
    
    def run(self, steps=None):
        """
        Executa o motor e consolida os resultados automaticamente.
        """
        steps_value = -1 if steps is None else steps
        super().run(steps_value)
        print("\n🔄 Consolidando resultados automaticamente...")
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