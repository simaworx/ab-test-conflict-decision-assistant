"use strict";

const treeContainer = document.getElementById("tree");
const restartButton = document.getElementById("restartTree");

let treeData = null;


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
        Object.keys(node.options || {}).length
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
async function loadTree() {
    try {
        const response = await fetch("/api/tree");

        if (!response.ok) {
            throw new Error(
                `Server returned status ${response.status}.`
            );
        }

        treeData = await response.json();

        renderTree();

    } catch (error) {
        console.error(error);

        showError(
            "The decision tree could not be loaded. " +
            "Check that the Flask server is running."
        );
    }
}


restartButton.addEventListener("click", restartTree);


loadTree();