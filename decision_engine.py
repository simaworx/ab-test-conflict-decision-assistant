from dataclasses import asdict, dataclass
from typing import Final


@dataclass(frozen=True)
class TreeNode:
    id: str
    node_type: str
    text: str
    from typing import Any

    options: list[dict[str, Any]] | None = None


TREE: Final[dict[str, TreeNode]] = {

    "intro": TreeNode(
        id="intro",
        node_type="statement",
        text="Primary metric is up, but conversion rate is down.",
        options=[
            {
                "label": "Start",
                "next": "significance"
            }
        ],
    ),

    "significance": TreeNode(
        id="significance",
        node_type="question",
        text="Is the drop in conversion rate statistically significant?",
        options=[
            {
                "label": "YES",
                "next": "drop_magnitude"
            },
            {
                "label": "NO",
                "next": "treat_as_noise"
            }
        ],
    ),

    "treat_as_noise": TreeNode(
        id="treat_as_noise",
        node_type="result",
        text=(
            "Treat the decline as noise. Proceed with rollout and monitor "
            "conversion after launch to confirm stability."
        ),
    ),

    "drop_magnitude": TreeNode(
        id="drop_magnitude",
        node_type="question",
        text="What is the magnitude of the conversion rate drop?",
        options=[
            {
                "label": "Less than 3%",
                "next": "primary_metric_value"
            },
            {
                "label": "Between 3% and 5%",
                "next": "segment_concentration"
            },
            {
                "label": "Greater than 5%",
                "next": "do_not_launch"
            }
        ],
    ),

    "primary_metric_value": TreeNode(
        id="primary_metric_value",
        node_type="question",
        text="Is the gain in the primary metric a valuable business goal?",
        options=[
            {
                "label": "YES",
                "next": "launch_with_monitoring"
            },
            {
                "label": "NO",
                "next": "long_term_redesign"
            }
        ],
    ),

    "long_term_redesign": TreeNode(
        id="long_term_redesign",
        node_type="question",
        text="Is this test part of a longer-term redesign?",
        options=[
            {
                "label": "YES",
                "next": "launch_with_monitoring"
            },
            {
                "label": "NO",
                "next": "prioritise_conversion"
            }
        ],
    ),

    "segment_concentration": TreeNode(
        id="segment_concentration",
        node_type="question",
        text=(
            "Is the decline concentrated in a specific segment, such as "
            "mobile users or returning customers?"
        ),
        options=[
            {
                "label": "YES",
                "next": "qualitative_issue"
            },
            {
                "label": "NO",
                "next": "primary_metric_value"
            }
        ],
    ),

    "qualitative_issue": TreeNode(
        id="qualitative_issue",
        node_type="question",
        text="Is there added friction, confusing copy, or a loss of trust?",
        options=[
            {
                "label": "YES",
                "next": "issue_fixable"
            },
            {
                "label": "NO",
                "next": "primary_metric_value"
            }
        ],
    ),

    "issue_fixable": TreeNode(
        id="issue_fixable",
        node_type="question",
        text="Is the identified issue fixable?",
        options=[
            {
                "label": "YES",
                "next": "fix_and_monitor"
            },
            {
                "label": "NO",
                "next": "prioritise_conversion"
            }
        ],
    ),

    "launch_with_monitoring": TreeNode(
        id="launch_with_monitoring",
        node_type="result",
        text="Consider launching with post-launch monitoring.",
    ),

    "fix_and_monitor": TreeNode(
        id="fix_and_monitor",
        node_type="result",
        text="Fix the identified issue and re-run the experiment.",
    ),

    "investigate_further": TreeNode(
        id="investigate_further",
        node_type="result",
        text="Investigate further before making a rollout decision.",
    ),

    "prioritise_conversion": TreeNode(
        id="prioritise_conversion",
        node_type="result",
        text="Do not launch. Prioritise overall conversion instead.",
    ),

    "do_not_launch": TreeNode(
        id="do_not_launch",
        node_type="result",
        text=(
            "Do not launch. Capture the learnings and design a new approach."
        ),
    ),
}

def get_node(node_id: str) -> TreeNode:
    """Return a decision-tree node by ID."""
    try:
        return TREE[node_id]
    except KeyError as exc:
        raise ValueError(f"Unknown tree node: {node_id}") from exc


def serialise_tree() -> dict[str, dict]:
    """Convert the decision tree into JSON-compatible dictionaries."""
    return {
        node_id: asdict(node)
        for node_id, node in TREE.items()
    }