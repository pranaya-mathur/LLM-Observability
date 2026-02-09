from .domain.domain_mismatch import DomainMismatchSignal
from .grounding.missing_grounding import MissingGroundingSignal
from .confidence.overconfidence import OverconfidenceSignal
from .domain.fabricated_concept import FabricatedConceptSignal


ALL_SIGNALS = [
    DomainMismatchSignal(),
    MissingGroundingSignal(),
    OverconfidenceSignal(),
    FabricatedConceptSignal(),
]
