# Sources for historical_disasters.csv

Every row is a real, documented Indian disaster. This file explains
exactly which numbers are **real reported figures** (with citations)
and which are **derived using standard humanitarian ratios** — so
nothing here is unlabeled guesswork.

## Read this first: two real limitations of this data

1. **Only 4 events.** This is nowhere near enough to train a
   statistically valid regression model. It's a genuine starting
   point (real numbers, not invented ones), not a finished dataset.
   Add more events as you find good sources.

2. **Scale mismatch.** These are *state/event-wide* aggregates
   (100,000 to 15 million people), while the app's own sample zones
   (e.g. "Kochi Riverside Sector") are *city/district-sized*
   (10,000-50,000 people). District-level breakdowns of these events
   aren't readily available in public reporting at the granularity
   needed for exact zone-level training. Feeding the model both very
   large (real) and very small (sample) population values means it's
   learning across a huge range it will rarely see in practice for
   this app's typical zone size. Two honest ways to fix this properly:
   - Find real *district-level* (not state-level) figures for these
     same events and use those instead, or
   - Keep the app's zones at realistic city/district scale and treat
     these 4 rows as filled-in reference points for the *upper end*
     of the severity curve only, adding more real *small-scale*
     events (single-district floods, local landslides) to fill in
     the lower end.

## Row-by-row sourcing

### Row 1 — Kerala Floods 2018
- **population = 5,400,000** — REAL. "Affected" population, per the
  UNDP Post-Disaster Needs Assessment (PDNA) for Kerala.
  Source: https://www.undp.org/publications/post-disaster-needs-assessment-kerala
- **shelter_capacity = 1,400,000** — REAL. Displaced population, same
  PDNA source.
- **severity = critical** — REAL classification basis: designated an
  "L3" (highest) level disaster under India's National Disaster
  Management Plan.
- **vulnerable_pct = 0.21** — DERIVED (not event-specific). Uses a
  national Census of India proxy (population aged 0-6 plus 60+ is
  roughly 21% nationally), not a measured figure for this specific
  event's affected population.
- **water_liters = population × 15** — DERIVED using the Sphere
  Handbook's minimum humanitarian water standard: 15 litres per
  person per day. Source: https://spherestandards.org/handbook/
  This is a **single day's** requirement, not a multi-day total.
- **medical_kits = population / 10,000** — DERIVED using the WHO
  Interagency Emergency Health Kit (IEHK) ratio: one kit is designed
  to cover 10,000 people for approximately 3 months.
- **food_packets = population** — DERIVED using a simplifying
  operational assumption (1 packet per affected person per day) that
  is commonly implied in Indian state relief situation reports, but
  is **not itself a published Sphere/WHO standard** — flagged here so
  you don't mistake it for one.

### Row 2 — Chennai Floods 2015
- **population = 1,800,000** — REAL. People sent to relief camps per
  government reports, cited in a peer-reviewed rapid assessment.
  Source: https://www.researchgate.net/publication/309133815_Chennai_Floods_2015_A_Rapid_Assessment
- **shelter_capacity = 1,800,000** — REAL, same source (camp
  population figure used directly since a separate "displaced but not
  camped" figure wasn't found).
- **severity = critical** — REAL classification basis: Chennai was
  declared a National Disaster zone by the Government of India.
- **vulnerable_pct, water_liters, medical_kits, food_packets** —
  DERIVED the same way as Row 1 (see above).

### Row 3 — Cyclone Fani 2019 (Odisha)
- **population = 15,093,513** — REAL. Total affected population
  across 14 districts, per the Joint Rapid Needs Assessment (JRNA).
  Source: https://reliefweb.int/report/india/cyclone-fani-joint-rapid-needs-assessment-jrna-report-2019-aftermath-cyclone-odisha-may
- **shelter_capacity = 1,470,197** — REAL. People evacuated to
  shelters, per Odisha's Special Relief Commissioner's report.
  Source: https://www.deccanherald.com/national/east-and-northeast/fani-affected-15-crore-people-in-14-odisha-districts-733117
- **severity = critical** — REAL classification basis: India
  Meteorological Department classified it an "Extremely Severe
  Cyclonic Storm."
- **vulnerable_pct, water_liters, medical_kits, food_packets** —
  DERIVED the same way as Row 1.

### Row 4 — Uttarakhand Floods 2013
- **population = 100,000** — REAL (approximate). Commonly cited
  figure for people stranded/evacuated in the flood zone.
  Source: https://www.bhoomikatrust.org/disaster-relief/uttar-floods/
- **shelter_capacity = 100,000** — same figure used directly; a
  separate "sheltered vs. rescued-but-not-sheltered" breakdown wasn't
  found in public sources.
- **severity = critical** — REAL classification basis: 6,054 deaths
  (Government of Uttarakhand figure, via Wikipedia's well-cited
  summary: https://en.wikipedia.org/wiki/2013_North_India_floods) —
  one of India's deadliest disasters relative to population affected.
- **vulnerable_pct, water_liters, medical_kits, food_packets** —
  DERIVED the same way as Row 1.

## What's still missing

- No "moderate" or "low" severity real events — international/national
  reporting overwhelmingly covers only the largest disasters, so
  smaller, equally-real events (a single flooded taluk, a local
  landslide) aren't represented here yet. Add them as you find sources
  (state SDMA websites, local news archives, ReliefWeb's smaller
  situation reports) to give the model examples across the full
  severity range, not just "critical."
