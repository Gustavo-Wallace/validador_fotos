from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class ResultadoValidacao:
    arquivo: str
    status: str
    validacoes: Dict[str, bool]
    detalhes: Dict[str, Any]
    mensagens: List[str] = field(default_factory=list)