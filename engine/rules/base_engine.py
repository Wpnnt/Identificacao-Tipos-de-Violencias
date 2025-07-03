import inspect
from experta.engine import KnowledgeEngine
from experta import Fact
from experta.rule import Rule
from experta.deffacts import DefFacts
from experta import TEST, AS, OR, NOT, AND
from typing import Dict, List, Any, Optional

from ..facts import (
    TextRelato, KeywordFact, ViolenceBehavior, ContextFact, FrequencyFact,
    TargetFact, RelationshipFact, ImpactFact, ViolenceClassification,
    AnalysisResult, ProcessingPhase
)

from knowledge_base.violence_types import VIOLENCE_TYPES


class BaseViolenceEngine(KnowledgeEngine):
    """
    Classe base para o motor de regras de identificação de tipos de violência.
    Contém métodos comuns e infraestrutura básica.
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
