from decision_engine import get_node, serialise_tree


def test_starting_node_exists():
    node = get_node("intro")

    assert node.node_type == "statement"
    assert node.options == [
        {
            "label": "Start",
            "next": "significance",
        }
    ]


def test_significance_has_two_branches():
    node = get_node("significance")

    assert node.node_type == "question"
    assert node.options is not None

    assert node.options == [
        {
            "label": "YES",
            "next": "drop_magnitude",
        },
        {
            "label": "NO",
            "next": "treat_as_noise",
        },
    ]


def test_tree_can_be_serialised():
    tree = serialise_tree()

    assert "intro" in tree
    assert "significance" in tree
    assert tree["intro"]["node_type"] == "statement"

    assert tree["drop_magnitude"]["options"] == [
        {
            "label": "Less than 3%",
            "next": "primary_metric_value",
        },
        {
            "label": "Between 3% and 5%",
            "next": "segment_concentration",
        },
        {
            "label": "Greater than 5%",
            "next": "do_not_launch",
        },
    ]