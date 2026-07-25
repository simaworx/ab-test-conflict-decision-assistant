from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class Option:
    label: str
    value: str
    next_step: str


@dataclass(frozen=True)
class QuestionNode:
    question: str
    help_text: str
    options: tuple[Option, ...]


@dataclass(frozen=True)
class ResultNode:
    title: str
    explanation: str
    status: str


QUESTIONS: Final[dict[str, QuestionNode]] = {
    "significance": QuestionNode(
        question="Is the conversion-rate decline statistically significant?",
        help_text=(
            "Consider the p-value, confidence interval, sample size, "
            "and whether the test had sufficient power."
        ),
        options=(
            Option(
                label="Yes",
                value="yes",
                next_step="drop_size",
            ),
            Option(
                label="No",
                value="no",
                next_step="rollout_monitor",
            ),
        ),
    ),

    "drop_size": QuestionNode(
        question="How large is the conversion-rate decline?",
        help_text=(
            "Select the relative decline observed between the control "
            "and variant conversion rates."
        ),
        options=(
            Option(
                label="Less than 3%",
                value="under_3",
                next_step="primary_value",
            ),
            Option(
                label="Between 3% and 5%",
                value="between_3_5",
                next_step="segment_concentration",
            ),
            Option(
                label="More than 5%",
                value="over_5",
                next_step="do_not_launch",
            ),
        ),
    ),

    "segment_concentration": QuestionNode(
        question="Is the decline concentrated in a particular user segment?",
        help_text=(
            "Review device, channel, customer type, geography, "
            "new versus returning users, and other relevant segments."
        ),
        options=(
            Option(
                label="Yes",
                value="yes",
                next_step="qualitative_friction",
            ),
            Option(
                label="No",
                value="no",
                next_step="investigate_further",
            ),
            Option(
                label="Not yet investigated",
                value="unknown",
                next_step="investigate_further",
            ),
        ),
    ),

    "qualitative_friction": QuestionNode(
        question="Is there evidence of customer friction or reduced trust?",
        help_text=(
            "Consider user feedback, session recordings, support contacts, "
            "confusing content, and unexpected behaviour."
        ),
        options=(
            Option(
                label="Yes",
                value="yes",
                next_step="issue_fixable",
            ),
            Option(
                label="No",
                value="no",
                next_step="investigate_further",
            ),
            Option(
                label="Not yet investigated",
                value="unknown",
                next_step="investigate_further",
            ),
        ),
    ),

    "issue_fixable": QuestionNode(
        question="Can the identified issue be fixed without losing the benefit?",
        help_text=(
            "Consider whether the problematic element can be changed "
            "while preserving the improvement in the primary metric."
        ),
        options=(
            Option(
                label="Yes",
                value="yes",
                next_step="fix_and_monitor",
            ),
            Option(
                label="No",
                value="no",
                next_step="scrap_variant",
            ),
        ),
    ),

    "primary_value": QuestionNode(
        question="Does the primary metric represent a valuable business outcome?",
        help_text=(
            "The metric should represent meaningful customer or commercial "
            "value rather than an isolated engagement increase."
        ),
        options=(
            Option(
                label="Yes",
                value="yes",
                next_step="rollout_monitor",
            ),
            Option(
                label="No",
                value="no",
                next_step="long_term_redesign",
            ),
        ),
    ),

    "long_term_redesign": QuestionNode(
        question="Is this experiment part of a longer-term product redesign?",
        help_text=(
            "A temporary decline may require further investigation if the test "
            "supports a larger strategic change."
        ),
        options=(
            Option(
                label="Yes",
                value="yes",
                next_step="investigate_further",
            ),
            Option(
                label="No",
                value="no",
                next_step="prioritise_conversion",
            ),
        ),
    ),
}


RESULTS: Final[dict[str, ResultNode]] = {
    "rollout_monitor": ResultNode(
        title="Proceed with a monitored rollout",
        explanation=(
            "The evidence does not currently justify rejecting the variant. "
            "Proceed carefully and monitor conversion, the primary metric, "
            "and relevant guardrail metrics after launch."
        ),
        status="proceed",
    ),

    "investigate_further": ResultNode(
        title="Investigate further before making a decision",
        explanation=(
            "The current evidence is not sufficient for a confident rollout "
            "decision. Complete additional segmentation, qualitative analysis, "
            "or follow-up experimentation."
        ),
        status="investigate",
    ),

    "fix_and_monitor": ResultNode(
        title="Fix the issue, then consider a monitored rollout",
        explanation=(
            "The conversion decline appears to have an identifiable and "
            "potentially fixable cause. Address the issue before launching "
            "and validate the revised experience."
        ),
        status="revise",
    ),

    "scrap_variant": ResultNode(
        title="Consider scrapping the variant",
        explanation=(
            "The conversion impact is linked to an issue that cannot currently "
            "be resolved without losing the benefit of the variant."
        ),
        status="stop",
    ),

    "do_not_launch": ResultNode(
        title="Do not launch the variant",
        explanation=(
            "The statistically significant conversion decline is greater than "
            "5%. The risk to overall performance outweighs the observed benefit."
        ),
        status="stop",
    ),

    "prioritise_conversion": ResultNode(
        title="Prioritise overall conversion",
        explanation=(
            "The primary-metric gain does not represent sufficient strategic "
            "value to justify the conversion decline."
        ),
        status="stop",
    ),
}


def get_question(node_id: str) -> QuestionNode:
    """Return a question node by its identifier."""
    try:
        return QUESTIONS[node_id]
    except KeyError as exc:
        raise ValueError(f"Unknown question node: {node_id}") from exc


def get_result(result_id: str) -> ResultNode:
    """Return a result node by its identifier."""
    try:
        return RESULTS[result_id]
    except KeyError as exc:
        raise ValueError(f"Unknown result node: {result_id}") from exc


def follow_branch(node_id: str, answer: str) -> str:
    """Return the next question or result for the selected answer."""
    question = get_question(node_id)

    for option in question.options:
        if option.value == answer:
            return option.next_step

    raise ValueError(
        f"Answer '{answer}' is not valid for question '{node_id}'."
    )


def is_result(node_id: str) -> bool:
    """Return True when the supplied node represents a final result."""
    return node_id in RESULTS