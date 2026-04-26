# PIM Quality Monitor

A browser-based dashboard for monitoring product information quality across multi-region B2B catalogues. Built from years of working with enterprise PIM systems and the data governance problems that come with them.

---

## Background

After spending years on B2B digital platforms where product data was the single biggest source of release failures and customer complaints, I got tired of discovering problems at the wrong time — during UAT, after a market go-live, or via a support ticket.

Most organisations running Akeneo, Stibo STEP, or similar PIM systems have completeness rules built in. What they typically don't have is a cross-market, cross-category view that surfaces *which* problems matter most and *where* — before they reach the channel.

This dashboard is the tool I kept wanting to have. It pulls from the PIM's existing quality signals and presents them in a way that a Product Owner, a data steward, or a commercial director can actually act on.

---

## What It Covers

**Dashboard** — Executive-level overview. Quality score by category, regional market health at a glance, critical issues blocking publication, 30-day trend line, and the attributes most frequently missing across the catalogue.

**Data Completeness** — Fill rate breakdown by product family and field type (mandatory, optional, regional). Sortable and filterable. Shows the gap between where you are and where you need to be before a market go-live.

**Market Coverage** — Per-market quality score, SKU count, translation coverage, and open gap count. Useful when you have regional data stewards who need to see their own situation without wading through global reports.

**Attribute Governance** — Full attribute register with coverage rates, field type classification, missing SKU counts, and a recommended action per attribute. The "priority action" column is what stops people doing the right things in the wrong order.

**Anomaly Detection** — Active quality incidents with severity, description, metadata, and assignment workflow. The kinds of things that break silently: bulk field wipes from failed imports, translation coverage drops after catalogue migrations, duplicate identifiers, missing compliance flags.

**System Architecture** — A diagram of the full data flow from source systems through PIM to channel, showing where the quality monitor sits and what it does and doesn't control.

---

## Data Profile (Demo)

The demo data reflects a realistic industrial B2B catalogue scenario:

- 102,847 active SKUs across 18 product families
- 50 active market locales (DACH, Americas, APAC, rest of Europe)
- ~340 governed attributes per family (mandatory + optional + regional)
- Source systems: SAP S/4HANA (material master), Salesforce CRM, Bynder DAM, legacy AS/400
- PIM: Akeneo Enterprise Edition
- Channels: B2B eCommerce portal, distributor feeds (BMEcat/ETIM), print catalogue, marketplace APIs

---

## Technical Decisions

No build step. No framework. No bundler. The whole thing runs from a folder of static HTML files — open `index.html` in a browser and it works.

This is deliberate. In enterprise environments, dashboards often need to be shared with stakeholders on internal networks, embedded in SharePoint, or demoed on machines without Node installed. A vanilla HTML/CSS/JS approach means there's nothing to install and nothing to break.

The data layer (`assets/data.js`) is a single JavaScript object. In production, this would be replaced by fetch calls to the PIM API endpoint. The rendering logic is in `assets/dashboard.js`. Keeping them separate means the data source can change without touching the UI, which matters when you're connecting to a real system with API rate limits and auth requirements.

Charts are drawn with native SVG — no Chart.js, no D3. This keeps the footprint minimal and means the charts render instantly without a library cold-start.

---

## File Structure

```
pim-quality-monitor/
├── index.html              # Executive dashboard
├── completeness.html       # Data completeness by category
├── markets.html            # Market coverage detail
├── attributes.html         # Attribute governance register
├── anomalies.html          # Anomaly detection and incident log
├── architecture.html       # System architecture diagram
├── assets/
│   ├── style.css           # All styles — single file, CSS variables throughout
│   ├── data.js             # Shared data layer (replaces API in production)
│   └── dashboard.js        # Dashboard chart and table rendering
└── README.md
```

---

## Running It

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

No npm install. No environment variables. No config files.

---

## What This Is Not

This is not a PIM system. It does not create, edit, or delete product data. It reads quality signals and makes them visible.

It is not a replacement for the completeness rules inside the PIM. Those rules enforce quality at write time. This tool surfaces patterns across markets and categories that individual rules cannot see.

It is not production-ready as-is. The data layer needs to be replaced with real API calls, authentication needs to be added, and the alerting module needs to connect to your actual Jira/email setup. But the measurement logic, the data model, and the UI structure are the hard part — and they're here.

---

## Connecting to a Real PIM

To connect to Akeneo, replace the contents of `assets/data.js` with a fetch to the REST API:

```javascript
async function loadPIMData() {
  const response = await fetch('https://your-akeneo-instance.com/api/rest/v1/products', {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  const data = await response.json();
  // transform to PIM_DATA shape and trigger renders
}
```

The Akeneo REST API returns completeness per product per channel per locale, which maps directly to the data structures used here.

---

## Notes on Scope

The attribute governance module reflects a real problem I encountered repeatedly: organisations that have hundreds of attributes in their PIM but no single view of which ones are actually well-populated and which are being ignored in practice. The "mandatory" designation in the PIM schema doesn't always reflect business reality. This module separates schema mandate from actual fill rate so decisions about remediation effort can be made with real data.

The anomaly detection module reflects another pattern: data quality problems that are invisible until they cause a downstream failure. A Hazmat flag cleared by a failed import doesn't break anything immediately — it only becomes a problem when that product hits a market where the field is required for customs compliance. By the time that happens, the root cause is weeks old. The anomaly log captures these events at source.

---

## Built by

Monil Raval — Product Owner with background in B2B digital platforms, PIM ownership, and ERP/eCommerce integration across European industrial markets.

[LinkedIn](https://linkedin.com/in/monil-raval) · [Portfolio](https://monilraval.github.io)
