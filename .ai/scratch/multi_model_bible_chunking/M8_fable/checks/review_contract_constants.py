"""Shared machine-readable M8 review-contract constants (same frozen contract as M7 method)."""
from __future__ import annotations


INDEPENDENCE_SCOPE = {
    "independent_from_sibling_model_maps": True,
    "primaries_blind_to_each_other_artifacts": True,
    "roles_separated": True,
    "shared_model_substrate": True,
    "counts_as_cross_model_independent_votes": False,
    "independent_model_or_human_evidence_required_at_convergence": True,
    "reviewer_count_is_not_authority": True,
    "correlated_mesh_weight_at_convergence": "one_model_voice",
}
