# DMV Prep public pages

Static English/Spanish support and privacy pages for DMV Prep.

Site: https://muhammetdemirci.github.io/dmv-prep-pages/

No build tools, tracking scripts or runtime dependencies are required. Publish the root of the main branch with GitHub Pages.

## Official information sources

`sources.html` and `sources-es.html` list every public source URL used by DMV Prep 0.4.0 / Android 6, including all 50 states, shared references and exam requirements. `sources.json` contains only public source metadata exported from the application with `scripts/export-play-sources.ts`; it contains no question banks or account data.

After replacing the inventory with a fresh application export, run `python3 generate-sources.py`. The renderer checks coverage of every source reference in both languages. `source-overrides.json` records current official alternatives for unavailable original addresses; alternatives are explicitly labeled on the pages. The inventory date is not a new factual review of the cited government publications.
