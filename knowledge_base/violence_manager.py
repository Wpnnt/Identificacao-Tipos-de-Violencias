"""
Gerenciador central de tipos de violência.
Este módulo substitui o arquivo violence_types.py original com uma estrutura mais organizada.
"""
from typing import Dict, List, Optional
from .models.violence_type import ViolenceType, ViolenceSubtype, Severity, ReportChannel
from .models.criteria import CriterionWeights
from .factories.violence_factory import ViolenceTypeFactory


class ViolenceTypeManager:
    """Gerenciador central para todos os tipos de violência."""
    
    def __init__(self):
        self._violence_types: Dict[str, ViolenceType] = {}
        self._report_channels: Dict[str, ReportChannel] = {}
        self._initialize_violence_types()
        self._initialize_report_channels()
    
    def _initialize_violence_types(self):
        """Inicializa todos os tipos de violência."""
        factory = ViolenceTypeFactory()
        
        # Adiciona todos os tipos de violência
        self._violence_types["microagressoes"] = factory.create_microagressoes()
        self._violence_types["perseguicao"] = factory.create_perseguicao()
        self._violence_types["violencia_sexual"] = factory.create_violencia_sexual()
        self._violence_types["discriminacao_genero"] = factory.create_discriminacao_genero()
        self._violence_types["abuso_psicologico"] = factory.create_abuso_psicologico()
        self._violence_types["assedio_moral_genero"] = factory.create_assedio_moral_genero()
        self._violence_types["gordofobia"] = factory.create_gordofobia()
        self._violence_types["capacitismo"] = factory.create_capacitismo()
        self._violence_types["violencia_digital"] = factory.create_violencia_digital()
        self._violence_types["discriminacao_religiosa"] = factory.create_discriminacao_religiosa()
        self._violence_types["xenofobia"] = factory.create_xenofobia()
        self._violence_types["discriminacao_racial"] = factory.create_discriminacao_racial()
    
    def _initialize_report_channels(self):
        """Inicializa os canais de denúncia."""
        self._report_channels = {
            "Ouvidoria": ReportChannel(
                name="Ouvidoria",
                description="Órgão responsável por receber denúncias e encaminhá-las.",
                contact="ouvidoria@ufape.edu.br",
                procedure="Enviar e-mail ou comparecer pessoalmente."
            ),
            "Comissao_Etica": ReportChannel(
                name="Comissão de Ética",
                description="Responsável por analisar casos de violação ética.",
                contact="etica@ufape.edu.br",
                procedure="Enviar denúncia formal por escrito."
            ),
            "Policia": ReportChannel(
                name="Polícia",
                description="Autoridade responsável por investigar crimes.",
                contact="190 (emergência)",
                procedure="Registrar Boletim de Ocorrência."
            ),
            "Seguranca_Campus": ReportChannel(
                name="Segurança do Campus",
                description="Equipe responsável pela segurança no campus.",
                procedure="Acionar em situações de emergência no campus."
            ),
            "Servico_Psicologico": ReportChannel(
                name="Serviço Psicológico",
                description="Atendimento psicológico especializado.",
                procedure="Buscar atendimento no serviço de psicologia da instituição."
            ),
            "Nucleo_Acessibilidade": ReportChannel(
                name="Núcleo de Acessibilidade",
                description="Responsável por questões de acessibilidade e inclusão.",
                procedure="Entrar em contato para adequações necessárias."
            ),
            "Plataformas_Digitais": ReportChannel(
                name="Plataformas Digitais",
                description="Canais de denúncia das próprias plataformas digitais.",
                procedure="Reportar conteúdo diretamente nas plataformas."
            ),
            "Delegacia_Mulher": ReportChannel(
                name="Delegacia da Mulher",
                description="Delegacia especializada no atendimento à mulher.",
                contact="180 (central)",
                procedure="Registrar Boletim de Ocorrência especializado."
            ),
            "Delegacia_Crimes_Digitais": ReportChannel(
                name="Delegacia de Crimes Digitais",
                description="Especializada em crimes cibernéticos.",
                procedure="Registrar BO para crimes digitais."
            ),
            "Nucleo_Direitos_Humanos": ReportChannel(
                name="Núcleo de Direitos Humanos",
                description="Setor responsável por questões de direitos humanos.",
                procedure="Procurar orientação sobre direitos fundamentais."
            ),
            "Coordenacao_Curso": ReportChannel(
                name="Coordenação de Curso",
                description="Coordenação do curso/departamento.",
                procedure="Comunicar à coordenação do curso."
            )
        }
    
    def get_violence_type(self, name: str) -> Optional[ViolenceType]:
        """Retorna um tipo de violência específico."""
        return self._violence_types.get(name)
    
    def get_all_violence_types(self) -> Dict[str, ViolenceType]:
        """Retorna todos os tipos de violência."""
        return self._violence_types.copy()
    
    def get_violence_subtype(self, violence_type: str, subtype_name: str) -> Optional[ViolenceSubtype]:
        """Retorna um subtipo específico de violência."""
        vtype = self.get_violence_type(violence_type)
        return vtype.get_subtype(subtype_name) if vtype else None
    
    def get_report_channel(self, name: str) -> Optional[ReportChannel]:
        """Retorna um canal de denúncia específico."""
        return self._report_channels.get(name)
    
    def get_all_report_channels(self) -> Dict[str, ReportChannel]:
        """Retorna todos os canais de denúncia."""
        return self._report_channels.copy()
    
    def get_severity_score(self, violence_type: str, subtype_name: str = None) -> int:
        """Retorna o score de gravidade para um tipo/subtipo de violência."""
        vtype = self.get_violence_type(violence_type)
        if not vtype:
            return 0
        return vtype.get_severity_score(subtype_name)
    
    def search_by_keywords(self, keywords: List[str]) -> List[tuple]:
        """
        Busca tipos de violência por palavras-chave.
        Retorna lista de tuplas (violence_type, subtype, relevance_score).
        """
        results = []
        keywords_lower = [k.lower() for k in keywords]
        
        for vtype_name, vtype in self._violence_types.items():
            # Verifica palavras-chave do tipo principal
            vtype_keywords = [k.lower() for k in vtype.keywords]
            main_matches = sum(1 for k in keywords_lower if any(k in vk for vk in vtype_keywords))
            
            if main_matches > 0:
                results.append((vtype_name, None, main_matches))
            
            # Verifica palavras-chave dos subtipos
            for subtype_name, subtype in vtype.subtypes.items():
                subtype_keywords = [k.lower() for k in subtype.keywords]
                sub_matches = sum(1 for k in keywords_lower if any(k in sk for sk in subtype_keywords))
                
                if sub_matches > 0:
                    results.append((vtype_name, subtype_name, sub_matches))
        
        # Ordena por relevância (mais matches primeiro)
        results.sort(key=lambda x: x[2], reverse=True)
        return results
    
    def get_recommendations(self, violence_type: str, subtype_name: str = None) -> List[str]:
        """Retorna recomendações para um tipo/subtipo de violência."""
        vtype = self.get_violence_type(violence_type)
        if not vtype:
            return []
        
        if subtype_name:
            subtype = vtype.get_subtype(subtype_name)
            if subtype and subtype.recommendations:
                return subtype.recommendations
        
        return vtype.recommendations
    
    def get_report_channels_for_violence(self, violence_type: str, subtype_name: str = None) -> List[ReportChannel]:
        """Retorna os canais de denúncia para um tipo/subtipo de violência."""
        vtype = self.get_violence_type(violence_type)
        if not vtype:
            return []
        
        channel_names = []
        if subtype_name:
            subtype = vtype.get_subtype(subtype_name)
            if subtype and subtype.report_channels:
                channel_names = subtype.report_channels
        
        if not channel_names:
            channel_names = vtype.report_channels
        
        return [self._report_channels[name] for name in channel_names if name in self._report_channels]

    def to_dict_format(self) -> Dict:
        """Converte para o formato de dicionário compatível com o código existente."""
        result = {}
        
        for vtype_name, vtype in self._violence_types.items():
            vtype_dict = {
                "nome": vtype_name.replace('_', ' ').title(),  # Adiciona campo nome esperado
                "definicao": vtype.definition,
                "gravidade": vtype.severity.value,
                "palavras_chave": vtype.keywords,
                "canais_denuncia": vtype.report_channels,
                "recomendacoes": vtype.recommendations
            }
            
            if hasattr(vtype, 'common_targets') and vtype.common_targets:
                vtype_dict["alvos_comuns"] = vtype.common_targets
            
            if vtype.subtypes:
                vtype_dict["subtipos"] = {}
                for subtype_name, subtype in vtype.subtypes.items():
                    subtype_dict = {
                        "definicao": subtype.definition,
                        "palavras_chave": subtype.keywords,
                    }
                    if subtype.behaviors:
                        subtype_dict["comportamentos"] = subtype.behaviors
                    if subtype.severity:
                        subtype_dict["gravidade"] = subtype.severity.value
                    if subtype.report_channels:
                        subtype_dict["canais_denuncia"] = subtype.report_channels
                    if subtype.recommendations:
                        subtype_dict["recomendacoes"] = subtype.recommendations
                    
                    vtype_dict["subtipos"][subtype_name] = subtype_dict
            
            result[vtype_name] = vtype_dict
        
        return result


# Instância global para compatibilidade com o código existente
_violence_manager = ViolenceTypeManager()

# Funções para compatibilidade com o código existente
def get_severity(vtype: str, subtype: str = None) -> int:
    """Função de compatibilidade para obter gravidade."""
    return _violence_manager.get_severity_score(vtype, subtype)

def get_violence_types() -> Dict[str, Dict]:
    """Função de compatibilidade para obter todos os tipos."""
    return _violence_manager.to_dict_format()

def get_criterion_weights() -> Dict[str, Dict[str, int]]:
    """Função de compatibilidade para obter pesos dos critérios."""
    return CriterionWeights.get_all_weights()

# Exports para compatibilidade
VIOLENCE_TYPES = _violence_manager.to_dict_format()
CRITERION_WEIGHTS = CriterionWeights.get_all_weights()

# Conversão dos canais de denúncia para o formato esperado
REPORT_CONTACT = {}
for name, channel in _violence_manager.get_all_report_channels().items():
    REPORT_CONTACT[name] = {
        "descricao": channel.description,
        "contato": channel.contact,
        "procedimento": channel.procedure
    }

# Mapeamento de gravidade para compatibilidade
SEVERITY_LEVEL = {
    "baixa": "Comportamento inadequado que requer atenção e orientação.",
    "baixa_cumulativa": "Comportamentos que individualmente são de baixa gravidade, mas podem causar danos significativos quando repetidos.",
    "media_baixa": "Violação que requer intervenção e possível advertência.",
    "media": "Violação que requer intervenção institucional e possíveis medidas disciplinares.",
    "media_alta": "Violação séria que pode resultar em medidas disciplinares mais severas.",
    "alta": "Violação grave que requer ações imediatas de proteção.",
    "gravissima": "Violação extremamente grave que constitui crime passível de expulsão."
}

# Ranking de gravidade para compatibilidade
SEVERITY_RANKING = {}
for vtype_name, vtype in _violence_manager.get_all_violence_types().items():
    if vtype.subtypes:
        SEVERITY_RANKING[vtype_name] = {
            subtype_name: subtype.severity_score 
            for subtype_name, subtype in vtype.subtypes.items()
        }
    else:
        SEVERITY_RANKING[vtype_name] = vtype.severity_score
