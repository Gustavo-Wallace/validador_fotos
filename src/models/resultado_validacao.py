from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class ResultadoValidacao:
    arquivo: str
    status: str
    validacoes: Dict[str, bool]
    detalhes: Dict[str, Optional[float]]
    mensagens: List[str] = field(default_factory=list)