# DPWH Contract Dashboard

An interactive explorer for Department of Public Works and Highways (DPWH) contract data. The dashboard renders regional datasets, lets you filter by contractor and status, and visualises investment impact summaries directly in the browser.

## Features
- **Rich filtering**: Filter contracts by contractor name, status, and effectivity month across individual regions or the consolidated dataset.
- **Responsive summaries**: Summary cards highlight project counts, total contract value, and flood-control specific metrics, updating instantly with every filter.
- **Flood insights**: Clicking the flood control figures toggles filters and opens a modal explaining billion-peso impacts, timelines for family spending equivalents, and alternative investment equivalents (schools, health facilities, food packs, etc.).
- **Dataset caching**: JSON payloads are cached in `localStorage` for quicker repeat visits, with a manual **Reload Data** button to refresh from source files on demand.
- **Skeleton loading states**: Graceful skeleton placeholders keep the UI polished while data loads asynchronously.

## Data Sources
- All datasets live in regional JSON files such as `region1-2025_1802.json`, `car-2025_737.json`, and the aggregated `all.json`.
- Raw records originate from the DPWH Infra Projects portal: <https://apps2.dpwh.gov.ph/infra_projects/default.aspx>
- Utility scripts:
  - `extract_contracts.py` parses raw exports into structured JSON.
  - `combine_json.py` merges regional outputs into the `all.json` dataset.

## Getting Started
1. Clone the repository and install dependencies (only required for development scripts):
   ```bash
   git clone https://github.com/gabconcepcionph/dpwh-contracts-dashboard.git
   cd dpwh-contracts-dashboard
   npm install
   ```
2. Serve the static site. Any static HTTP server works; for example:
   ```bash
   npx http-server .
   ```
   Then open `http://localhost:8080/index.html`, or simply double-click `index.html` to open it directly in a browser.
3. Select a dataset from the dropdown to load contracts. Use filters and summary controls to explore.

## Development Notes
- **Dependencies**: The UI relies on CDN-hosted Tailwind CSS and jQuery; no local build step is required for the dashboard itself.
- **Modal experience**: The "How much is a billion?" link opens a modal (`#billion-modal`) with contextual spending timelines and investment equivalents based on current flood-control totals.
- **Reload behaviour**: `localStorage` caching lasts up to one year; the **Reload Data** button fetches fresh JSON and refreshes the cache immediately.
- **Data updates**: Place updated JSON files in the repository root (matching existing filenames) and reload the page to reflect new numbers.

## Contributing
Issues and improvements are welcome. Please follow existing code style, keep changes scoped, and update documentation when introducing new user-facing functionality.
