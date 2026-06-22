# Article Series Pitch — The Dispatcher's Office
## NY&E Northern Lights Subdivision: Operations Design and Implementation

**Prepared for:** Eric Smith, Editor — The Dispatcher's Office (editor@opsig.org)  
**Authors:** Allen D. Byrne and Claude (Anthropic AI assistant)  
**Date:** June 2026

> **Note on AI co-authorship:** This article series was researched, outlined, and drafted with significant
> assistance from Claude, Anthropic's AI assistant. The railroad design, operations concept, system
> architecture, and all technical decisions are the author's own; Claude assisted with writing, structure,
> and diagrams. The editorial team may wish to discuss how to handle this in the byline or author's note —
> the author is happy to follow the DO's guidance on AI disclosure.

---

## Overview

I would like to propose a two-article series on the operations design and digital control system for the
**New York and Eastern Railroad (NY&E), Northern Lights Subdivision** — a freelanced 1905-era branch
railroad modeled on a C&O prototype. The series covers the same subject from two different angles:

- **Article 1** — An accessible overview aimed at any reader considering an operating position, structured
  around the five operating roles and how they interact. Connects ten years of paper-and-pencil T&TO
  sessions on the old layout to the digital-assist system now being implemented on the new layout.

- **Article 2** — A technical deep-dive for readers who want to understand the hardware and software
  architecture and apply the concepts to their own layout. Covers the ESP32 station units, MQTT message
  bus, dispatcher web application, fast clock, and train order workflow in detail.

Both articles are ready to be written. The system is design-complete through Phase 2 (infrastructure,
station OS, train order issuance, clearance forms, TO signal control); the Yardmaster terminal software
is in active development and is expected to be complete before submission. One physical station unit is
installed and tested; remaining stations will be installed as layout construction continues.

---

## Article 1 — Operations at the New York and Eastern

**Proposed title:** *Operations at the New York and Eastern: Designing for Authentic 1905 Timetable and
Train Order Sessions*

**Subhead:** *From ten years of paper-and-pencil dispatching to a distributed digital control system —
the operations concept hasn't changed.*

**Target length:** 4–5 pages, approximately 3,000–3,500 words, 5–6 figures.

**Lead photo:** Operators at work on the old layout during a session — paper train orders visible on the
fascia, the crew engaged. Captures ten years of successful T&TO operations before the digital system.

### Summary

The NY&E Northern Lights Subdivision is a freelanced branch railroad set in 1905, modeled on C&O
mountain branch practice. The layout is two-level: a C&O mainline above (East and West staging, used
primarily for interchange with the Williamsport yard) and the NY&E branch below, running point-to-point
from Williamsport (WP) south terminus to Hemlock Crest (HC) north terminus across seven stations with
passing sidings on a single main track. Southward trains are superior by direction.

The operations concept is timetable and train order — the dispatcher issues meet orders, extras, and
clearances; station agents OS trains through; the yardmaster assembles and receives consists at
Williamsport. This concept ran successfully for ten years on the previous layout with 6–8 operators
using entirely paper-based tools: a printed timetable, a handwritten dispatcher string table, and paper
train orders. The new layout applies digital tools to the same operations to reduce bookkeeping friction
and give operators more time railroading.

The article is structured around the five operating roles — Dispatcher, Yardmaster, Crew, Trainmaster,
and Owner — explaining what each role sees and does, what interface they use, and what background
makes a good fit. A brief "session from start to finish" narrative ties the roles together. The article
closes with a summary of what is built and what is planned in future phases.

### Outline

1. **The Railroad** — NY&E NLS, circa 1905; two-level, point-to-point, 7 stations; why T&TO at this
   era rewards a group session. *(Track schematic figure.)*

2. **Ten Years of Operations** — Previous layout; 6–8 operators; paper dispatcher sheet and string
   table; flexible assignments; what the new system improves without changing the operations concept.
   *(Old dispatcher sheet figure.)*

3. **The Control System at a Glance** — One central server, seven fascia station units, a yardmaster
   terminal, phone throttles. The technology enforces the rules; operators focus on railroading.
   *(System block diagram figure.)*

4. **Choosing Your Position** — One section per role:
   - *Dispatcher* — web app; OS log; structured TO forms generating 1905-style order text; signal arms.
     Paper is still the authority. *(Dispatcher web app screenshot.)*
   - *Yardmaster* — WP yard only; 7" touchscreen; construct/deconstruct consists; C&O interchange.
   - *Crew / Engineer* — phone throttle; OS report at each station CYD; receives TOs and clearances
     on the station screen. Note: switchbacks at BB, JC, MC, and SK require the crew to swap ends — not
     everyone's preference, worth discussing with the session host before choosing a train.
   - *Trainmaster* (pre-session) — reviews waybills; generates session manifest; identifies extras.
   - *Owner* (monitor) — system health from any device; no live operational controls; post-session
     report generation.

5. **A Session from Start to Finish** — Narrative walkthrough: system startup through session close.

6. **What's Built, What's Next** — Phase 2 complete; Phase 3 cameras; Phase 4 RFID detection;
   Phase 5 layout lighting; Phase 6 dispatcher assist.

---

## Article 2 — Building the NY&E Layout Control System

**Proposed title:** *Building the NY&E Layout Control System: A Distributed IoT Approach to Prototype
Operations*

**Target length:** 6–8 pages, approximately 4,500–5,500 words, 8–10 figures.

### Summary

This article covers the hardware, software, and design decisions behind the NY&E control system for
readers who want to understand the architecture and apply similar approaches to their own railroad.
The system is built around five design principles: self-contained layout network (no home internet
required during a session), MQTT as the universal message bus, DCC for traction only, prototypically
authentic workflows, and phased delivery so each phase delivers usable value.

A central Raspberry Pi 5 hosts the WiFi access point, MQTT broker, fast clock, dispatcher web
application, and JMRI. Seven ESP32 CYD (Cheap Yellow Display) touchscreen units — one per station,
fascia-mounted — handle OS reporting, train order display, clearance display, and TO signal arm
control via PCA9685 PWM servo drivers. The yardmaster operates from a dedicated 7" touchscreen
terminal running on a Raspberry Pi 3. Engineer smartphones connect via WiThrottle to JMRI for
locomotive control.

### Outline

1. **Design Principles** — Self-contained network, MQTT bus, inventory-first hardware, phased
   delivery, prototypically authentic workflows.

2. **Network Architecture** — RPi5 as WiFi AP + MQTT broker + server stack; all components as
   MQTT clients; isolation from home network during operations. *(Network topology diagram.)*

3. **MQTT as the Layout Message Bus** — Pub/sub architecture; topic structure; QoS and retained
   messages; why MQTT makes it easy to add devices. *(Topic map table.)*

4. **Station Units — ESP32 CYD** — Hardware walkthrough; LVGL screen state machine
   (Clock→OS→Orders→Clearance→Status); PCA9685 I2C PWM driver for TO signal servos; NVS
   provisioning; local fast clock interpolation between MQTT ticks. *(CYD screen state diagram.)*

5. **The Fast Clock** — Master/client architecture; 3:1 ratio; local interpolation for smooth display;
   session continuity (state persisted to disk; next session resumes from saved railroad time).

6. **The Dispatcher Web Application** — FastAPI + WebSocket MQTT bridge; station tile view; TO
   template system; structured form generation producing formatted 1905-style order text; paper
   primacy retained. *(Dispatcher UI screenshots.)*

7. **Train Order and Clearance Workflow** — TO types (meet, wait, running extra, work extra,
   annulment, sections); dispatcher reviews digital text, copies to paper log, issues to stations;
   station CYD displays order for agent to copy and acknowledge; TO signal arm raises automatically
   on issue, dispatcher lowers manually (prototypically authentic).

8. **Physical Hardware — Fascia Mounting** — 3D-printed CYD enclosures (Prusa Core One);
   TrainOrderServo bracket for signal arm servos; SwitchToggle lever for Blue Point turnout control.
   *(Photos of printed hardware.)*

9. **Adapting to Your Railroad** — What's generic (clock service, MQTT topic structure, CYD firmware);
   what's railroad-specific (timetable, TO templates, clearance rules); how to start with one station
   and grow.

10. **Build Phases — Starting Simple** — Phase-by-phase delivery; each phase is independently
    operational; where to start for a smaller or simpler layout.

---

## Figure Inventory

| # | Description | Article | Status |
|---|-------------|---------|--------|
| F1 | Track schematic — WP to HC, 7 stations, sidings, switchbacks | Art. 1 | `docs/diagrams/track_schematic.svg` |
| F2 | Old dispatcher string table (Timetable No. 4) | Art. 1 | Exists (PDF) |
| F3 | System block diagram — server, stations, YM terminal, phones, DCC | Art. 1 | `docs/diagrams/system_overview.svg` |
| F4 | Dispatcher web app screenshot | Art. 1 | Exists (screenshot) |
| F5 | Yardmaster terminal | Art. 1 | Exists (screenshot) |
| F6 | Station CYD — clock + OS screens | Art. 1 | Exists (4 simulated mockups) |
| F7 | Network topology diagram | Art. 2 | New SVG — planned |
| F8 | CYD screen state machine | Art. 2 | New SVG — planned |
| F9 | MQTT topic map (table) | Art. 2 | From architecture doc |
| F10 | Example TO order text output | Art. 2 | Generate from running system |
| F11 | 3D-printed CYD enclosure and servo bracket photos | Art. 2 | Needs photos |

---

## About the Author

Allen D. Byrne has been modeling proto-freelanced New York and Eastern in HO scale for 27 years. The NY&E
Northern Lights Subdivision was in operation for over ten years in its previous form, with formal operating sessions averaging
6–8 participants using timetable and train order operations based on the ARA Standard Code of 1906.
The new layout is currently under construction since 2020 with the digital control system in active development since
Allen retired as a software engineer at the end of 2025 — the IoT control system is an original design built on
open-source components.

---

## Proposed Timeline

| Milestone | Target |
|-----------|--------|
| Editor query / outline approval | [Upon receipt] |
| Yardmaster terminal software complete | Before article submission |
| Article 1 first draft | 4–6 weeks after outline approval |
| Article 1 figures complete | With first draft |
| Article 1 submitted | [Target issue TBD with editor] |
| Article 2 first draft | Following issue after Art. 1 |

---

*Questions or feedback welcome. Happy to discuss scope, length, or figure requirements.*
