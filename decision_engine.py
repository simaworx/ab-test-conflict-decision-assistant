from dataclasses import dataclass
from enum import Enum


class Recommendation(str, Enum):
    ROLLOUT = "Proceed with rollout"
    ROLLOUT_AND_MONITOR = "Proceed with rollout and monitor performance"
    INVESTIGATE = "Investigate further"
    FIX_AND_MONITOR = "Fix the identified issue and consider a monitored rollout"
    PRIORITISE_CONVERSION = "Prioritise overall conversion"
    SCRAP_VARIANT = "Consider scrapping the variant"
    DO_NOT_LAUNCH = "Do not launch"


@dataclass(frozen=True)
class ExperimentInputs:
    statistically_significant: bool
    conversion_drop_percent: float

    segment_concentrated: bool | None = None
    qualitative_friction: bool | None = None
    issue_fixable: bool | None = None
    primary_metric_valuable: bool | None = None
    longer_term_redesign: bool | None = None


@dataclass(frozen=True)
class DecisionResult:
    recommendation: Recommendation
    explanation: str
    monitoring_required: bool = False


def evaluate_experiment(inputs: ExperimentInputs) -> DecisionResult:
    """
    Evaluate an A/B test where the primary metric improved
    but conversion rate declined.
    """

    if inputs.conversion_drop_percent < 0:
        raise ValueError("Conversion drop must be zero or greater.")

    if not inputs.statistically_significant:
        return DecisionResult(
            recommendation=Recommendation.ROLLOUT_AND_MONITOR,
            explanation=(
                "The conversion decline is not statistically significant. "
                "Treat it as possible noise, but monitor conversion after rollout "
                "to confirm that performance remains stable."
            ),
            monitoring_required=True,
        )

    if inputs.conversion_drop_percent > 5:
        return DecisionResult(
            recommendation=Recommendation.DO_NOT_LAUNCH,
            explanation=(
                "The conversion decline is statistically significant and greater "
                "than 5%. The risk to overall conversion outweighs the observed "
                "gain in the primary metric."
            ),
        )

    if inputs.conversion_drop_percent >= 3:
        if inputs.segment_concentrated or inputs.qualitative_friction:
            if inputs.issue_fixable:
                return DecisionResult(
                    recommendation=Recommendation.FIX_AND_MONITOR,
                    explanation=(
                        "The decline is meaningful, but the analysis suggests a "
                        "specific and potentially fixable cause. Address the issue "
                        "before considering a monitored rollout."
                    ),
                    monitoring_required=True,
                )

            return DecisionResult(
                recommendation=Recommendation.SCRAP_VARIANT,
                explanation=(
                    "The conversion decline appears linked to a specific customer "
                    "segment or qualitative issue, but the problem is not currently "
                    "fixable."
                ),
            )

        return DecisionResult(
            recommendation=Recommendation.INVESTIGATE,
            explanation=(
                "The conversion decline is between 3% and 5%. More segmentation "
                "and qualitative analysis are required before making a rollout "
                "decision."
            ),
        )

    if inputs.primary_metric_valuable:
        return DecisionResult(
            recommendation=Recommendation.ROLLOUT_AND_MONITOR,
            explanation=(
                "The conversion decline is below 3%, and the primary metric "
                "supports a valuable business objective. A monitored rollout may "
                "be justified."
            ),
            monitoring_required=True,
        )

    if inputs.longer_term_redesign:
        return DecisionResult(
            recommendation=Recommendation.INVESTIGATE,
            explanation=(
                "The primary-metric gain is not sufficient on its own, but the "
                "test forms part of a longer-term redesign. Continue investigating "
                "before committing to rollout."
            ),
        )

    return DecisionResult(
        recommendation=Recommendation.PRIORITISE_CONVERSION,
        explanation=(
            "The primary-metric improvement does not justify the conversion loss. "
            "Prioritise overall conversion and do not roll out the current variant."
        ),
    )