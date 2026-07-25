import pytest

from decision_engine import (
    ExperimentInputs,
    Recommendation,
    evaluate_experiment,
)


def test_non_significant_drop_allows_monitored_rollout():
    result = evaluate_experiment(
        ExperimentInputs(
            statistically_significant=False,
            conversion_drop_percent=2.5,
        )
    )

    assert result.recommendation == Recommendation.ROLLOUT_AND_MONITOR
    assert result.monitoring_required is True


def test_drop_greater_than_five_percent_does_not_launch():
    result = evaluate_experiment(
        ExperimentInputs(
            statistically_significant=True,
            conversion_drop_percent=5.1,
        )
    )

    assert result.recommendation == Recommendation.DO_NOT_LAUNCH


def test_fixable_segment_issue_returns_fix_and_monitor():
    result = evaluate_experiment(
        ExperimentInputs(
            statistically_significant=True,
            conversion_drop_percent=4,
            segment_concentrated=True,
            qualitative_friction=False,
            issue_fixable=True,
        )
    )

    assert result.recommendation == Recommendation.FIX_AND_MONITOR


def test_negative_drop_raises_error():
    with pytest.raises(ValueError):
        evaluate_experiment(
            ExperimentInputs(
                statistically_significant=True,
                conversion_drop_percent=-1,
            )
        )