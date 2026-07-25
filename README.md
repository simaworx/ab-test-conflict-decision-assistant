# A/B Test Conflict Decision Assistant

An interactive decision-tree tool for evaluating A/B tests where the primary metric improves while conversion rate declines.

## Demo

![A/B Test Conflict Decision Assistant](static/images/demo.png)

## Features

- Interactive branching decision flow
- Ordered answer branches
- Responsive desktop and mobile layout
- Clear recommendation outcomes
- Restart controls at page level and inside final recommendations
- No server or database required for the live version

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
├── static/
│   ├── css/
│   │   └── style.css
│   ├── images/
│   │   ├── decision-tree.png
│   │   └── demo.png
│   └── js/
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

## Author

**Simona Sukyte**

Product Data Analyst focused on product analytics, A/B testing, reporting, data visualisation, and workflow automation.
