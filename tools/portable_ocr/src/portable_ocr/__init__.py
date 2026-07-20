"""Provider-neutral OCR evidence collection and human review."""

from .comparison import compare_candidates, compare_text
from .conversation import ConversationReviewer
from .routing import route_third_engine

__all__ = ["ConversationReviewer", "compare_candidates", "compare_text", "route_third_engine"]
__version__ = "0.1.0"
