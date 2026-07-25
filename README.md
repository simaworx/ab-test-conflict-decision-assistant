# A/B Test Conflict Decision Assistant

An interactive Flask application that transforms an A/B testing decisionframework into a guided branching decision tree.

The tool helps product teams evaluate situations where the primary experiment metric improves, but conversion rate declines, and provides a structured recommendation based on the answers selected.

## Demo

![A/B Test Conflict Decision Assistant](static/images/demo.png)

## Overview

A/B testing decisions are not always straightforward.

An experiment may show:

- Improvement in the primary success metric
- A decline in conversion rate

This creates a decision conflict:

- Should the experiment launch?
- Is the conversion decline meaningful?
- Does the impact affect a specific customer segment?
- Is there a usability or trust issue?
- Should the experiment be redesigned?

This project recreates that decision-making process as an interactivetree, guiding users through each question until reaching a finalrecommendation.

## Features

- Interactive A/B test conflict decision flow
- Guides decision-making when primary metrics improve but conversion rate declines
- Ordered branching logic based on experiment evaluation criteria
- Clear rollout recommendations and next-step actions
- Responsive desktop and mobile interface
- Restart functionality for exploring different scenarios
- Fully client-side implementation with no database required

## Live Project

Try the interactive decision tree here:

[Open A/B Test Conflict Decision Assistant](https://simaworx.github.io/ab-test-conflict-decision-assistant/)

## Tech Stack

- HTML
- CSS
- JavaScript

Logic: Rule-based decision tree engine

## How it works

The deployed version is fully static:

- `index.html` provides the page structure
- `static/css/style.css` controls the interface
- `static/js/tree.js` contains the tree data and interaction logic

## Project Structure

```text
ab-test-conflict-decision-assistant/
├── index.html
├── README.md
├── LICENSE
├── .gitignore
│
└──  static/
    ├── css/
    │   └── style.css
    ├── images/
    │   ├── decision-tree.png
    │   └── demo.png
    └── js/
        └── tree.js
```

## Run the static version locally

```bash
python -m http.server 8000
```

Open `http://127.0.0.1:8000`.

## Embed into a page

```html
<iframe
    src="YOUR_GITHUB_PAGES_URL"
    title="A/B Test Conflict Decision Tree"
    width="100%"
    height="950"
    loading="lazy"
></iframe>
```

## Why I Built This

In product analytics, experiment results often require judgement rather than a simple winner/loser decision.

This project explores how analytical frameworks and experimentation principles can be converted into practical tools that help teams make more consistent and informed decisions.

## Author

**Simona Sukyte**

Product Data Analyst focused on product analytics, A/B testing, reporting, data visualisation, and workflow automation.