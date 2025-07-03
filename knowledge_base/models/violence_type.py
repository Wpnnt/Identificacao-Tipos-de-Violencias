"""
Modelos de dados para tipos de violência.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
from enum import Enum


class Severity(Enum):
    """Níveis de gravidade das violências."""
    BAIXA = "baixa"
    BAIXA_CUMULATIVA = "baixa_cumulativa"
    MEDIA_BAIXA = "media_baixa"
    MEDIA = "media"
    MEDIA_ALTA = "media_alta"
    ALTA = "alta"
    GRAVISSIMA = "gravissima"


@dataclass
class ViolenceSubtype:
    """Representa um subtipo de violência."""
    name: str
    definition: str
    keywords: List[str] = field(default_factory=list)
    behaviors: List[str] = field(default_factory=list)
    severity: Optional[Severity] = None
    report_channels: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    severity_score: int = 0


@dataclass
class ViolenceType:
    """Representa um tipo principal de violência."""
    name: str
    definition: str
    severity: Severity
    keywords: List[str] = field(default_factory=list)
    common_targets: List[str] = field(default_factory=list)
    report_channels: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    subtypes: Dict[str, ViolenceSubtype] = field(default_factory=dict)
    severity_score: int = 0

    def add_subtype(self, subtype: ViolenceSubtype) -> None:
        """Adiciona um subtipo a este tipo de violência."""
        self.subtypes[subtype.name] = subtype

    def get_subtype(self, name: str) -> Optional[ViolenceSubtype]:
        """Retorna um subtipo específico."""
        return self.subtypes.get(name)

    def get_all_keywords(self) -> List[str]:
        """Retorna todas as palavras-chave do tipo e seus subtipos."""
        all_keywords = self.keywords.copy()
        for subtype in self.subtypes.values():
            all_keywords.extend(subtype.keywords)
        return list(set(all_keywords))

    def get_severity_score(self, subtype_name: str = None) -> int:
        """Retorna o score de gravidade do tipo ou subtipo."""
        if subtype_name and subtype_name in self.subtypes:
            return self.subtypes[subtype_name].severity_score
        return self.severity_score


@dataclass
class ReportChannel:
    """Canal de denúncia."""
    name: str
    description: str
    contact: str = ""
    procedure: str = ""
