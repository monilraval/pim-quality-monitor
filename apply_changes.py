#!/usr/bin/env python3
"""
PIM Quality Monitor — Repository Cleanup Script
================================================

Run this ONCE inside your pim-quality-monitor folder.

What it does:
  1. Replaces README.md with the new version
  2. Applies UI label fixes to all six HTML files
  3. Prints a summary of changes

Usage:
  cd pim-quality-monitor
  python3 apply_changes.py

Then commit and push:
  git add -A
  git commit -m "docs: rewrite README; chore: replace prototype labels"
  git push

Safe to run: only modifies specific known strings. Will not touch
any data, layout, CSS, or JavaScript logic.
"""

import os
import sys
from pathlib import Path

# ============================================================
# THE NEW README CONTENT
# ============================================================

NEW_README = """# PIM Quality Monitor

A browser-based dashboard for surfacing data quality patterns across multi-region B2B product catalogues. Built to demonstrate the measurement framework, data model, and UI structure I keep wishing existed alongside enterprise PIM systems.

**Live demo:** https://monilraval.github.io/pim-quality-monitor/

---

## Why this exists

After several years working with enterprise B2B platforms — where product data is consistently the single largest source of release failures, distributor complaints, and silent compliance gaps — I kept reaching for a tool that didn't quite exist in the shape I wanted.

Most organisations running Akeneo, Stibo STEP, Informatica, or comparable systems already have completeness rules built in. Those rules do their job at write time. What's typically missing is the layer *above* the PIM: a cross-market, cross-category view that surfaces which gaps actually matter, where they're concentrated, and how they're trending — before they reach a channel, a distributor, or a customs officer.

This repository is a working sketch of that layer. The measurement logic, the data model, and the dashboard structure are real. The data is synthetic but realistic. The visual design is borrowed from the Bloomberg-terminal-meets-control-panel aesthetic that suits operational dashboards better than the usual SaaS palette.

---

## What this is

A static-HTML dashboard prototype that demonstrates six views of product information quality across a simulated industrial B2B catalogue:

- **Executive dashboard** — Overall quality score, critical issues blocking publication, market health at a glance, and a 30-day trend line
- **Data completeness** — Fill rate breakdown by product family and field type
- **Market coverage** — Per-market quality score, SKU count, translation coverage, and open gap count
- **Attribute governance** — Coverage rate and recommended action per attribute, separating schema mandate from actual fill rate
- **Anomaly detection** — Quality incidents with severity, root cause, and ownership (the silent-failure pattern: bulk field wipes from broken imports, translation drops after migrations, compliance flag gaps)
- **System architecture** — Diagram of where the quality monitor sits in the wider PIM/ERP/channel stack

## What this is not

This is **not a PIM system.** It does not create, edit, or delete product data. It is a visualisation and measurement framework that sits beside a PIM and reads from it.

This is **not production-ready software.** The current build is a prototype with synthetic data hardcoded into the HTML files. To run against a real PIM you'd need to (a) extract the data layer into a separate module, (b) replace the static data with API calls, (c) add authentication, and (d) connect the anomaly module to your actual ticketing setup.

This is **not a replacement for the completeness rules inside your PIM.** Those rules enforce quality at write time. This tool surfaces patterns across markets, categories, and time that individual rules cannot see.

---

## Demo data profile

The synthetic dataset reflects a realistic industrial B2B catalogue scenario:

- **102,847** active SKUs across 18 product families (cutting tools, indexable inserts, carbide rods, wear parts, milling tools, drilling solutions, threading tools, tool holders, PCD tools, CBN inserts, special tools, legacy components, and others)
- **12** sample markets shown on the dashboard, representing **~50 locale combinations** across 4 regions (DACH, Americas, APAC, rest of Europe)
- **~340** governed attributes per family, split across mandatory, optional, and regional types
- **Source systems modelled:** SAP S/4HANA (material master), Salesforce CRM, Bynder DAM, legacy AS/400
- **PIM modelled:** Akeneo Enterprise Edition
- **Channels modelled:** B2B eCommerce portal, distributor feeds (BMEcat/ETIM), print catalogue, marketplace APIs

The data is hand-curated to look like what you'd actually find in a mature industrial catalogue: realistic SKU distributions, a long tail of underperforming categories, a few markets in genuine trouble, and the kind of compliance gaps that tend to surface late.

---

## Technical approach

The entire dashboard runs from a folder of static HTML files. Each file contains its own inlined CSS, JavaScript, and demo data. There is no build step, no framework, no bundler, no package manager.

This is a deliberate choice for a prototype of this kind:

- **Zero install friction.** Clone, open `index.html` in a browser, and it works. No `npm install`, no environment variables, no compatibility surprises.
- **Embeddable anywhere.** Drops into a SharePoint page, an internal wiki, or a stakeholder demo machine without any infrastructure conversation.
- **Charts drawn with native SVG.** No Chart.js, no D3. Faster cold start, no library version conflicts, and the chart code is readable in the source.

The trade-off is that the data layer, styles, and rendering logic are duplicated across the six HTML files rather than shared. For a prototype this is acceptable. For an actual product, the first refactor would be to extract these into shared modules — that's the next milestone on the roadmap below.

---

## File structure

```
pim-quality-monitor/
├── index.html              # Executive dashboard
├── completeness.html       # Data completeness by category
├── markets.html            # Market coverage detail
├── attributes.html         # Attribute governance register
├── anomalies.html          # Anomaly detection and incident log
├── architecture.html       # System architecture diagram
├── LICENSE                 # MIT
└── README.md
```

Each HTML file is self-contained: CSS, JavaScript, and demo data are all inlined. The shared design language (colour palette, typography, spacing system) is consistent across files through repeated CSS variables.

---

## Running it

Clone and open in a browser:

```bash
git clone https://github.com/monilraval/pim-quality-monitor
cd pim-quality-monitor
open index.html
```

Or via a local server if you prefer:

```bash
python3 -m http.server 8080
# then open http://localhost:8080
```

Or just visit the live demo: https://monilraval.github.io/pim-quality-monitor/

---

## Roadmap

This is a prototype I plan to develop. The honest order of next work:

**Near-term (the next refactor)**

- Extract inlined CSS, JS, and demo data into a shared `assets/` folder so the six HTML files stop duplicating common code
- Add a thin data adapter layer so the demo data and a real PIM connector can swap without touching the rendering code
- Write a basic test suite for the data transformation functions

**Medium-term (proof of real connection)**

- Build a reference Akeneo REST connector that pulls real completeness and locale data
- Add pagination, rate-limit handling, and an auth layer
- Wire the anomaly module to a real ticketing target (Jira, Linear, or email)

**Longer-term (the question this would have to answer to be a real product)**

- Define the anomaly taxonomy as a configurable rule set rather than a hardcoded list
- Add historical persistence so trend lines reflect real data over real time, not synthetic curves
- Build the "what changed since last week" diff view, which is the question every data steward actually asks on Monday morning

---

## Notes on the design choices

A few specific things in here that came from actual problems I've watched play out, rather than from theory:

**The attribute governance module** separates *schema mandate* from *actual fill rate* because the "mandatory" designation in a PIM schema does not always reflect business reality. Organisations end up with hundreds of attributes marked mandatory in the schema, half of which are widely ignored in practice. Remediation effort then gets spent in the wrong places. This module makes the gap visible.

**The anomaly module** focuses on the silent failure pattern. A Hazmat flag cleared by a broken overnight import does not break anything immediately. It becomes a problem when that SKU hits a market where the field is required for customs compliance, by which point the root cause is weeks old and cold. The anomaly log captures these events at source with enough metadata to reconstruct what happened.

**The market coverage view** is structured so a regional data steward can see their own situation without having to wade through a global report. Per-market scores are also more useful for the people accountable for them than aggregate global numbers, which tend to flatter and conceal.

**The "Bloomberg terminal" aesthetic** is a deliberate choice for an operational dashboard. Quality monitoring is a job, not a marketing surface. The dense layout, monospaced typography, and restrained colour palette match how the audience actually reads operational data.

---

## Built by

Monil Raval — Product Owner with background in B2B digital platforms, PIM ownership, and ERP/eCommerce integration across European industrial markets.

If you work in this space and the framing here resonates (or doesn't), I'd genuinely value the conversation.

- [LinkedIn](https://www.linkedin.com/in/monil-raval)
- [Portfolio](https://monilraval.github.io)

## License

MIT — use, fork, adapt, and ship.
"""

# ============================================================
# THE FIND/REPLACE OPERATIONS FOR HTML FILES
# ============================================================
# Each tuple: (description, find_string, replace_string)

REPLACEMENTS = [
    (
        "Sidebar logo subtitle (v2.4.1 Production → v0.1 Prototype)",
        '<span class="logo-sub">v2.4.1 — Production</span>',
        '<span class="logo-sub">v0.1 — Prototype</span>',
    ),
    (
        "Sidebar live sync status (Live → Demo data)",
        '<span class="live-sync">Live — Last sync 0s ago</span>',
        '<span class="live-sync">Demo data — synthetic catalogue</span>',
    ),
    (
        "Sidebar footer market count (50 markets → 12 markets · 50 locales)",
        '<div class="sys-meta">50 markets · 102,847 SKUs</div>',
        '<div class="sys-meta">12 markets · 50 locales · 102,847 SKUs</div>',
    ),
    (
        "Topbar Live badge → Demo badge",
        '<span class="live-badge">Live</span>',
        '<span class="live-badge">Demo</span>',
    ),
    (
        "Dashboard panel Streaming badge → Demo Loop",
        '<span class="live-badge" style="font-size:8px">Streaming</span>',
        '<span class="live-badge" style="font-size:8px">Demo Loop</span>',
    ),
]

HTML_FILES = [
    "index.html",
    "completeness.html",
    "markets.html",
    "attributes.html",
    "anomalies.html",
    "architecture.html",
]


# ============================================================
# EXECUTION
# ============================================================

def main():
    # Confirm we're in the right directory
    cwd = Path.cwd()
    print(f"Running in: {cwd}")
    print()

    # Check we're actually in the repo
    if not (cwd / "index.html").exists():
        print("ERROR: index.html not found in current directory.")
        print("Make sure you're running this script from inside the")
        print("pim-quality-monitor folder.")
        sys.exit(1)

    # ── 1. Replace README.md ──────────────────────────────
    readme_path = cwd / "README.md"
    print("─" * 60)
    print("STEP 1: Writing new README.md")
    print("─" * 60)
    readme_path.write_text(NEW_README, encoding="utf-8")
    print(f"  ✓ Wrote {len(NEW_README)} characters to README.md")
    print()

    # ── 2. Apply UI label fixes to HTML files ────────────
    print("─" * 60)
    print("STEP 2: Applying UI label fixes to HTML files")
    print("─" * 60)

    total_files_changed = 0
    total_replacements = 0

    for filename in HTML_FILES:
        filepath = cwd / filename
        if not filepath.exists():
            print(f"  ⚠ Skipping {filename} (not found)")
            continue

        original = filepath.read_text(encoding="utf-8")
        modified = original
        file_changes = []

        for description, find_str, replace_str in REPLACEMENTS:
            if find_str in modified:
                modified = modified.replace(find_str, replace_str)
                file_changes.append(description)
                total_replacements += 1

        if file_changes:
            filepath.write_text(modified, encoding="utf-8")
            total_files_changed += 1
            print(f"\n  ✓ {filename} — {len(file_changes)} change(s):")
            for change in file_changes:
                print(f"      • {change}")
        else:
            print(f"\n  · {filename} — no matches (already clean or different version)")

    print()

    # ── 3. Summary ─────────────────────────────────────────
    print("─" * 60)
    print("SUMMARY")
    print("─" * 60)
    print(f"  README.md           : replaced")
    print(f"  HTML files changed  : {total_files_changed} of {len(HTML_FILES)}")
    print(f"  Total replacements  : {total_replacements}")
    print()
    print("Next steps:")
    print("  1. Review the changes:    git diff")
    print("  2. Stage everything:      git add -A")
    print("  3. Commit:                git commit -m \"docs: rewrite README; chore: replace prototype labels\"")
    print("  4. Push:                  git push")
    print()
    print("Then enable GitHub Pages:")
    print("  → Repo Settings → Pages → Source: main / root → Save")
    print()
    print("Then update the About description on GitHub to:")
    print("  → B2B PIM Data Quality Intelligence Dashboard — 100k SKUs, 12 markets, 50 locales")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
