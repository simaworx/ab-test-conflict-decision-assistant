"use strict";

const treeContainer = document.getElementById("tree");
const restartButton = document.getElementById("restartTree");

const treeData = {
    intro: { 
        id: "intro", 
        node_type: "statement", 
        text: "Primary metric is up, but conversion rate is down.", 
        options: [
            {
                label: "Start", next: "significance" 
            }
        ] 
    },
    significance: { 
        id: "significance", 
        node_type: "question", 
        text: "Is the drop in conversion rate statistically significant?", 
        options: [
            { 
                label: "YES", 
                next: "drop_magnitude" 
            }, 
            { 
                label: "NO", 
                next: "treat_as_noise" 
            }
        ] 
    },
    treat_as_noise: {
        id: "treat_as_noise", 
        node_type: "result", 
        text: "Treat the decline as noise. Proceed with rollout and monitor conversion after launch to confirm stability.", 
        options: null },
    drop_magnitude: { 
        id: "drop_magnitude", 
        node_type: "question", 
        text: "What is the magnitude of the conversion rate drop?", 
        options: [
            { 
                label: "Less than 3%", 
                next: "primary_metric_value" 
            }, 
            { 
                label: "Between 3% and 5%", 
                next: "segment_concentration" 
            }, 
            { 
                label: "Greater than 5%", 
                next: "do_not_launch" 
            }
        ] 
    },
    primary_metric_value: {
        id: "primary_metric_value", 
        node_type: "question", 
        text: "Is the gain in the primary metric a valuable business goal?", 
        options: [
            { 
                label: "YES", 
                next: "launch_with_monitoring" 
            }, 
            { 
                label: "NO", 
                next: "long_term_redesign" 
            }
        ] 
    },
    long_term_redesign: {
        id: "long_term_redesign", 
        node_type: "question", 
        text: "Is this test part of a longer-term redesign?", 
        options: [
            { 
                label: "YES", 
                next: "launch_with_monitoring" 
            }, 
            { 
                label: "NO", 
                next: "prioritise_conversion" 
            }
        ] 
    },
    segment_concentration: { 
        id: "segment_concentration", 
        node_type: "question", 
        text: "Is the decline concentrated in a specific segment, such as mobile users or returning customers?", 
        options: [
            { 
                label: "YES", 
                next: "qualitative_issue" 
            }, 
            { 
                label: "NO", 
                next: "primary_metric_value" 
            }
        ] 
    },
    qualitative_issue: { 
        id: "qualitative_issue", 
        node_type: "question", 
        text: "Is there added friction, confusing copy, or a loss of trust?", 
        options: [
            { 
                label: "YES", 
                next: "issue_fixable" 
            }, 
            { 
                label: "NO", 
                next: "primary_metric_value" 
            }
        ] 
    },
    issue_fixable: { 
        id: "issue_fixable", 
        node_type: "question", 
        text: "Is the identified issue fixable?", 
        options: [
            { 
                label: "YES", 
                next: "fix_and_monitor" 
            }, 
            { 
                label: "NO", 
                next: "prioritise_conversion" 
            }
        ] 
    },
    launch_with_monitoring: { 
        id: "launch_with_monitoring", 
        node_type: "result", 
        text: "Consider launching with post-launch monitoring.", 
        options: null 
    },
    fix_and_monitor: { 
        id: "fix_and_monitor", 
        node_type: "result", 
        text: "Fix the identified issue and re-run the experiment.", 
        options: null 
    },
    prioritise_conversion: { 
        id: "prioritise_conversion", 
        node_type: "result", 
        text: "Do not launch. Prioritise overall conversion instead.", 
        options: null 
    },
    do_not_launch: { 
        id: "do_not_launch", 
        node_type: "result", 
        text: "Do not launch. Capture the learnings and design a new approach.", 
        options: null 
    }
};

/**
 * Creates one visible tree node.
 */
function createNode(node) {
    const nodeElement = document.createElement("article");

    nodeElement.className =
        `tree-node tree-node-${node.node_type} tree-node-${node.id}`;
    
    nodeElement.dataset.nodeId = node.id;

    const typeLabel = document.createElement("span");
    typeLabel.className = "node-type";

    if (node.node_type === "statement") {
        typeLabel.textContent = "Starting scenario";
    } else if (node.node_type === "question") {
        typeLabel.textContent = "Decision";
    } else {
        typeLabel.textContent = "Recommendation";
    }

    const text = document.createElement("p");
    text.className = "node-text";
    text.textContent = node.text;

    nodeElement.append(typeLabel, text);

    if (node.node_type === "result") {
        const restartTreeButton = document.createElement("button");

        restartTreeButton.type = "button";
        restartTreeButton.className = "result-restart-button";
        restartTreeButton.textContent = "Restart tree";

        restartTreeButton.addEventListener("click", restartTree);

        nodeElement.appendChild(restartTreeButton);
    }

    return nodeElement;
}


/**
 * Creates the option branches below a question.
 */
function createBranches(node) {
    const branches = document.createElement("div");
    branches.className = "tree-branches";

    branches.style.setProperty(
        "--branch-count",
        (node.options || []).length
    );

    (node.options || []).forEach(
        (option) => {

            const optionLabel = option.label;
            const nextNodeId = option.next;
            const branch = document.createElement("div");
            branch.className = "tree-branch";

            const connector = document.createElement("div");
            connector.className = "branch-connector";
            connector.setAttribute("aria-hidden", "true");

            const optionButton = document.createElement("button");
            optionButton.type = "button";
            optionButton.className = "branch-button";
            optionButton.textContent = optionLabel;

            const childContainer = document.createElement("div");
            childContainer.className = "branch-child";

            optionButton.addEventListener("click", () => {
                chooseBranch(
                    branches,
                    branch,
                    optionButton,
                    childContainer,
                    nextNodeId
                );
            });

            branch.append(
                connector,
                optionButton,
                childContainer
            );

            branches.appendChild(branch);
        }
    );

    return branches;
}


/**
 * Handles a branch selection and grows the tree downward.
 */
function chooseBranch(
    branches,
    selectedBranch,
    selectedButton,
    childContainer,
    nextNodeId
) {
    if (branches.dataset.answered === "true") {
        return;
    }

    branches.dataset.answered = "true";

    branches
        .querySelectorAll(".tree-branch")
        .forEach((branch) => {
            const button = branch.querySelector(".branch-button");

            button.disabled = true;

            if (branch === selectedBranch) {
                branch.classList.add("selected");
                button.classList.add("selected");
            } else {
                branch.classList.add("not-selected");
            }
        });

    selectedButton.setAttribute("aria-pressed", "true");

    const nextNode = treeData[nextNodeId];

    if (!nextNode) {
        showError(`Tree node "${nextNodeId}" could not be found.`);
        return;
    }

    const nextLevel = document.createElement("div");
    nextLevel.className = "tree-level";

    const nodeElement = createNode(nextNode);
    nextLevel.appendChild(nodeElement);

    if (
        nextNode.node_type !== "result" &&
        nextNode.options
    ) {
        nextLevel.appendChild(
            createBranches(nextNode)
        );
    }

    childContainer.appendChild(nextLevel);

    requestAnimationFrame(() => {
        nextLevel.classList.add("visible");

        nextLevel.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });
    });

    restartButton.hidden = false;
}


/**
 * Draws the first tree node.
 */
function renderTree() {
    treeContainer.innerHTML = "";

    const startNode = treeData.intro;

    if (!startNode) {
        showError("The starting node could not be found.");
        return;
    }

    const firstLevel = document.createElement("div");
    firstLevel.className = "tree-level visible";

    firstLevel.appendChild(
        createNode(startNode)
    );

    if (startNode.options) {
        firstLevel.appendChild(
            createBranches(startNode)
        );
    }

    treeContainer.appendChild(firstLevel);
}


/**
 * Shows an application error.
 */
function showError(message) {
    treeContainer.innerHTML = "";

    const error = document.createElement("p");
    error.className = "error-message";
    error.textContent = message;

    treeContainer.appendChild(error);
}

/** shared restart function
 */

function restartTree() {
    restartButton.hidden = true;
    renderTree();

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

/**
 * Loads the Python tree from Flask.
 */

restartButton.addEventListener("click", restartTree);

renderTree();
