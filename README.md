# A/B Test Conflict Decision Assistant

A rule-based Flask application for evaluating conflicting A/B test results.

## The problem

A/B test results can produce conflicting signals. A variant may improve
the primary metric while reducing conversion rate, creating uncertainty
about whether the variant should be launched.

This project provides a structured process for evaluating that trade-off.

## What the framework evaluates

- Statistical significance
- Magnitude of the conversion-rate decline
- Impact on specific user segments
- Customer friction and qualitative feedback
- Whether the issue is fixable
- Long-term business value
- Rollout and monitoring options

## Possible outcomes

- Proceed with rollout
- Launch with post-launch monitoring
- Investigate further
- Redesign the variant
- Prioritise overall conversion
- Do not launch

## Tools and methods

- A/B testing principles
- Statistical significance
- Metric trade-off analysis
- User segmentation
- Qualitative analysis
- Decision-tree modelling
- HTML
- CSS

## Live project

Add the GitHub Pages link here after deployment.

## Project image

![A/B Test Conflict Decision Tree](static/decision-tree.png)

## Author

Created by Simona Šukytė.