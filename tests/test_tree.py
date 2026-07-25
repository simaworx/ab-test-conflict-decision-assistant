from decision_engine import get_node, serialise_tree


def test_starting_node_exists():
    node = get_node("intro")

    assert node.node_type == "statement"
    assert node.options == {"Start": "significance"}


def test_significance_has_two_branches():
    node = get_node("significance")

    assert node.node_type == "question"
    assert node.options is not None
    assert node.options["YES"] == "drop_magnitude"
    assert node.options["NO"] == "treat_as_noise"


def test_tree_can_be_serialised():
    tree = serialise_tree()

    assert "intro" in tree
    assert "significance" in tree
    assert tree["intro"]["node_type"] == "statement"