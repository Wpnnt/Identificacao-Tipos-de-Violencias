from typing import Dict, List, Any
from knowledge_base.violence_types import VIOLENCE_TYPES


class ExplanationSystem:
    """
    Sistema responsável por gerar explicações detalhadas sobre as classificações de violência.
    """
    
    @staticmethod
    def get_violence_definition(violence_type: str, subtype: str = None) -> str:
        """
        Retorna a definição de um tipo/subtipo de violência.
        """
        info = VIOLENCE_TYPES.get(violence_type, {})
        
        if subtype and 'subtipos' in info and subtype in info['subtipos']:
            return info['subtipos'][subtype].get('definicao', '')
        
        return info.get('definicao', '')
    
    @staticmethod
    def get_legal_context(violence_type: str, subtype: str = None) -> str:
        """
        Retorna o contexto legal para um tipo/subtipo de violência.
        """
        info = VIOLENCE_TYPES.get(violence_type, {})
        
        if subtype and 'subtipos' in info and subtype in info['subtipos']:
            subtype_info = info['subtipos'][subtype]
            return subtype_info.get('contexto_legal', info.get('contexto_legal', ''))
        
        return info.get('contexto_legal', '')
    
    @staticmethod
    def get_severity_level(violence_type: str, subtype: str = None) -> str:
        """
        Retorna o nível de gravidade de um tipo/subtipo de violência.
        """
        info = VIOLENCE_TYPES.get(violence_type, {})
        
        if subtype and 'subtipos' in info and subtype in info['subtipos']:
            subtype_info = info['subtipos'][subtype]
            return subtype_info.get('gravidade', info.get('gravidade', ''))
        
        return info.get('gravidade', '')
    
    @staticmethod
    def get_recommendations(violence_type: str, subtype: str = None) -> List[str]:
        """
        Retorna as recomendações para um tipo/subtipo de violência.
        """
        info = VIOLENCE_TYPES.get(violence_type, {})
        
        if subtype and 'subtipos' in info and subtype in info['subtipos']:
            subtype_info = info['subtipos'][subtype]
            return subtype_info.get('recomendacoes', info.get('recomendacoes', []))
        
        return info.get('recomendacoes', [])
    
    @staticmethod
    def get_reporting_channels(violence_type: str, subtype: str = None) -> List[str]:
        """
        Retorna os canais de denúncia para um tipo/subtipo de violência.
        """
        info = VIOLENCE_TYPES.get(violence_type, {})
        
        if subtype and 'subtipos' in info and subtype in info['subtipos']:
            subtype_info = info['subtipos'][subtype]
            return subtype_info.get('canais_denuncia', info.get('canais_denuncia', []))
        
        return info.get('canais_denuncia', [])
    
    @staticmethod
    def format_complete_explanation(violence_type: str, subtype: str = None, 
                                    facts_used: Dict = None, reasoning: str = None) -> Dict[str, Any]:
        """
        Formata uma explicação completa incluindo definição, contexto legal, 
        recomendações e análise dos fatos.
        """
        explanation = {
            'type': violence_type,
            'subtype': subtype or '',
            'definition': ExplanationSystem.get_violence_definition(violence_type, subtype),
            'legal_context': ExplanationSystem.get_legal_context(violence_type, subtype),
            'severity': ExplanationSystem.get_severity_level(violence_type, subtype),
            'recommendations': ExplanationSystem.get_recommendations(violence_type, subtype),
            'reporting_channels': ExplanationSystem.get_reporting_channels(violence_type, subtype),
            'analysis': ExplanationSystem.format_fact_analysis(facts_used) if facts_used else [],
            'reasoning': reasoning or ''
        }
        
        return explanation
    
    @staticmethod
    def format_fact_analysis(facts_used: Dict) -> List[str]:
        """
        Formata a análise dos fatos utilizados na classificação.
        """
        analysis = []
        
        if 'behavior' in facts_used:
            behaviors = facts_used['behavior']
            behavior_text = ", ".join(behaviors) if len(behaviors) > 1 else behaviors[0]
            analysis.append(f"Comportamentos identificados: {behavior_text}")
        
        if 'context' in facts_used:
            contexts = facts_used['context']
            context_text = ", ".join(contexts) if len(contexts) > 1 else contexts[0]
            analysis.append(f"Contexto: {context_text}")
        
        if 'frequency' in facts_used:
            frequencies = facts_used['frequency']
            freq_text = ", ".join(frequencies) if len(frequencies) > 1 else frequencies[0]
            analysis.append(f"Frequência: {freq_text}")
        
        if 'target' in facts_used:
            targets = facts_used['target']
            target_text = ", ".join(targets) if len(targets) > 1 else targets[0]
            analysis.append(f"Características visadas: {target_text}")
        
        if 'relationship' in facts_used:
            relationships = facts_used['relationship']
            rel_text = ", ".join(relationships) if len(relationships) > 1 else relationships[0]
            analysis.append(f"Tipo de relacionamento: {rel_text}")
        
        if 'impact' in facts_used:
            impacts = facts_used['impact']
            impact_text = ", ".join(impacts) if len(impacts) > 1 else impacts[0]
            analysis.append(f"Impactos observados: {impact_text}")
        
        return analysis
