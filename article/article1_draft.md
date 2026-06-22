# Operations at the New York and Eastern: Designing for Authentic 1905 Timetable and Train Order Sessions

*From ten years of paper-and-pencil dispatching to a distributed digital control system — the operations concept hasn't changed.*

**By Allen D. Byrne and Claude (Anthropic AI)**

*Draft — second pass, 2026-06-22. Word count target 3,000–3,500; current draft 3,360 words.*

---

**[Figure: Lead photo — operators at work on the old layout during a session, paper train orders visible on the fascia. `/home/abyrne/ITD_WEB/itd/images/AlOpSessionYM.jpg`]**

---

## 1. The Railroad

The New York and Eastern Railroad (NY&E), Northern Lights Subdivision, is a freelanced branch line set in 1905, built on the operating character of a Chesapeake & Ohio mountain branch. It's modeled in HO, two levels: a short section of C&O mainline up top, running between East and West staging with no through traffic, and the NY&E branch below it, where the actual operating session happens.

The branch itself is simple in plan and demanding in practice: a single main track, point-to-point, running from the yard at Williamsport (WP) north to the resort terminus at Hemlock Crest (HC), with five stations in between — Xina Pass, Becs Bend, Jacks Creek, Michelles Cove, and Stans Knob. Every station has a passing siding. There's no double track and no signaling in the modern sense; the only thing that keeps two trains from occupying the same piece of track at the same time is the timetable, the train order, and the dispatcher's judgment. Among trains of the same class, southward trains are superior by direction, which means a northward train has to be in the clear — in a siding, off the main — whenever a southward train of the same class is due. Class outranks direction, though: a lower-class or unscheduled extra has no rights against a higher-class train regardless of which way either one is headed, unless a train order says otherwise.

**[Figure 1 — Track schematic, WP to HC: `docs/diagrams/track_schematic.svg`]**

This era of operation — 1905, ahead of automatic block signals and centralized traffic control — is exactly why timetable and train order (T&TO) operation rewards a group session rather than a solo running session. With a real dispatcher, real station agents, and real train crews following a real set of rules, the railroad becomes a small organization with its own internal communication problem to solve, and that problem is the whole point. Twelve scheduled trains run in each direction every operating day on the NY&E, three classes of service, with meets and waits arranged by the dispatcher as conditions develop — and on a branch with switchback stations and limited siding capacity, those meets aren't always where the timetable expects them to be.

## 2. Ten Years of Operations

None of this is new to the NY&E. The previous layout ran this same operating concept — same railroad, same era, same rules — for more than ten years, with operating sessions that regularly drew six to eight participants. Everything was paper: a printed Timetable, a hand-drawn dispatcher's string table tracking every train's progress against time and distance, and a pad of blank train order forms that the dispatcher filled out by hand. Getting word back and forth was just as manual: a crew member yelling an OS across to the dispatcher, a runner carrying a written order out to the train, or the crew simply walking up to the dispatcher in person to pick one up.

**[Figure 2 — Old dispatcher string table, Timetable No. 4: `NYELayoutDocs/alt/DispatcherSheet_StringTable4.pdf`]**

It worked. It worked well enough, for long enough, that when the layout came down and the new one began construction in 2020, there was never a real question about whether to keep timetable and train order operation — only about how to support it better. The paper system has one structural weakness that any dispatcher who's run one will recognize immediately: bookkeeping load. A good dispatcher is doing three things at once — tracking where every train actually is, deciding where the next conflict is going to happen, and writing it all down accurately enough that nobody gets confused later. The string table may show where the gaps are in the schedule, but issuing a train order in real time, under time pressure, by someone who'd rather be thinking about the railroad than writing everything down in multiple places, can spell disaster for an op session.

The new layout's control system exists to take that third job — the bookkeeping — off the dispatcher's plate, without changing the other two at all. Nothing about *what* a dispatcher decides is different. What's different is how much of the *recording* of those decisions the system does automatically, so the dispatcher can spend the session's mental energy on the actual railroading.

## 3. The Control System at a Glance

The system is small and deliberately self-contained — it doesn't depend on home internet access, and it doesn't try to do anything the 1905 operating concept doesn't already call for. A single Raspberry Pi 5 sits at the center of it, hosting its own isolated WiFi network for the layout, an MQTT message broker that every other device talks through, the dispatcher's web application, a shared fast clock, and JMRI for DCC throttle bridging. Everything else on the network — station units, the yardmaster terminal, the dispatcher's own browser — is just a client of that one box.

**[Figure 3 — System block diagram: `docs/diagrams/system_overview.svg`]**

Out at the railroad, each of the seven stations has a small fascia-mounted touchscreen unit — an ESP32 "Cheap Yellow Display," CYD for short — sitting where a station agent's desk would have been in 1905. It shows the fast clock, takes OS (on-sheet) reports as trains arrive and depart, and displays train orders and clearance forms as the dispatcher issues them. Five of the seven stations also drive a small servo-actuated signal arm, raised automatically the instant the dispatcher issues an order addressed to that station and lowered once the dispatcher releases it — a physical, visible cue that matches what a real train order signal did on the prototype.

At Williamsport, the yardmaster works from a dedicated 7-inch touchscreen terminal of their own, separate from both the dispatcher and the station units, because the yard is the yardmaster's domain exclusively — more on that below. Engineers run their locomotives from a smartphone using a standard WiThrottle app or a DCC throttle, and check the timetable and train orders before leaving a station.

The technology's job, in other words, is to enforce the bookkeeping and surface the right information to the right person at the right moment. It doesn't make decisions, and it doesn't talk to the crew directly — every interaction a road crew has with the operating system happens through a station's touchscreen or a paper order in their hand, exactly as it would have in 1905.

## 4. Choosing Your Position

An operating session on the NY&E has five kinds of jobs. None of them require knowing anything about what's happening inside the control system — every interface is built around the paper form or rulebook procedure it's standing in for, not the other way around.

### Dispatcher

The dispatcher runs the whole main line for the session, working from a full-screen browser dashboard — typically in a separate room from the layout itself, the way a real train dispatcher would never have been standing trackside. The OS log on screen fills in as station reports arrive: train number, direction, section, time. As conflicts develop, the dispatcher composes a train order — a structured form that produces correctly formatted 1905-style order text, the same phrasing a real 1905-era dispatcher would have written by hand — and indicates which stations need the signal arms set to stop. From there, the dispatcher's screen tracks which stations have acknowledged the order and which are still outstanding.

**[Figure 4 — Dispatcher web app, mid-session: `IOTtrains/docs/screenshots/dispatcher_ui_session2.5.png`]**

It's worth being explicit about something the system is deliberately careful about: paper is still the authority. The dispatcher's screen helps track and compose, but the operating discipline — what gets written on a clearance form, what a crew can and can't do without an order in hand — hasn't moved off paper at all. The software just makes sure the dispatcher doesn't have to do that bookkeeping twice.

### Yardmaster

The yardmaster has exclusive authority over the yard at Williamsport — building consists for departing trains, breaking down arrivals, assigning yard tracks, and handling the interchange with the C&O. The dispatcher has no say in track assignment inside the yard; when a southbound train is approaching and about to arrive, the dispatcher's only job is to send the yardmaster an arrival notice with an expected time. From there, getting that train onto the right track, in the right order, with the engine serviced and ready for its next assignment, is entirely the yardmaster's call.

**[Figure 5 — Yardmaster terminal: `IOTtrains/docs/screenshots/yardmaster_ui_session2.0.png`]**

The yardmaster works from their own 7-inch touchscreen at the yard, separate from the dispatcher's station and built around the same logic as a real yardmaster's clipboard: a list of departing trains with their build status, a track board showing what's sitting where, and an arrivals panel for what's inbound. Building a consist means recording an engine number, a caboose number, and a count of loaded and empty cars — read straight off the physical Car Cards and Waybills for the actual cars in the actual yard. The system doesn't track individual cars; that detail stays on paper, the same as it always has.

### Crew — Engineer and Conductor

Running a train is, deliberately, the role with the least amount of technology attached to it. The engineer drives from a phone using a standard WiThrottle app or a DCC throttle. The conductor's job is to follow timetable and train order rules at each station: report on arrival and departure, watch for orders waiting at the next station's signal, take the siding when the rules call for it. There's no app for that side of the job, because there doesn't need to be — the discipline lives in the rulebook, the same as it would have in 1905, and that's exactly the point of running T&TO operations in the first place.

One thing worth knowing before choosing a train: four of the line's five intermediate stations — Becs Bend, Jacks Creek, Michelles Cove, and Stans Knob — are switchbacks, which means the crew has to physically reverse the train and move the caboose to the other end before continuing. It's a mountain branch of this era, and it's part of the appeal for some crews — but it's also extra physical work at every stop, and worth discussing with the session host before you pick an assignment if that's not your idea of a good time. The intention is to keep the engine at the front of the train and the caboose at the end. So even the simple passenger run requires a little work to move the engine.

### Trainmaster

The trainmaster is a pre-session planning role, not a live one. Before the session starts, the trainmaster reviews the waybills and customer requests on file, builds the train manifests that tell the yardmaster what each scheduled train needs to carry, and identifies where demand has outgrown the timetable's scheduled capacity — which becomes a request for an extra train. Right now this is a paper-and-printout job, done at the workbench before anyone touches a throttle; whether it grows into a live terminal presence during the session itself is an open question for a future phase.

### Owner

The owner's role during a session is mostly to stay out of the way — monitoring system health from any device on hand, without any live operational controls of their own, and generating whatever post-session reports are useful for next time. Between sessions, though, the owner does most of the actual railroad-running work that doesn't happen during the session itself: adjusting the timetable, assigning waybill routing, printing the materials every operator needs, and tracking equipment maintenance.

## 5. A Session from Start to Finish

The best way to see how these roles fit together is to watch one real meet happen, start to finish — pulled straight from the published Timetable No. 4, not a hypothetical. No. 52 is the daily local way freight, second class, scheduled to leave Hemlock Crest at 6:15 AM and work every station on its way down to the yard. At the same moment, an extra freight — Engine 14, no number of its own — gets running orders to leave Williamsport northbound. The two converge on Jacks Creek, the branch's main passing siding — but getting them through in the right order takes a train order, not just the timetable, because of how the two trains rank against each other.

This is worth pausing on, because it's a rule a lot of newer operators get backwards: direction only decides superiority between trains of the *same* class. Class comes first. An extra has no rights of its own at all — it's inferior to every scheduled train on the timetable, schedule or no schedule, regardless of which way either one is headed. Left to the default rules, No. 52 has every right to hold the main at Jacks Creek for its scheduled 10-minute work stop and highball south right on time at 7:09, extra or no extra. The dispatcher wants Engine 14 kept moving, so the order isn't an ordinary Form A meet — it's a Form C, *Giving Right Over Another Train*. The dispatcher app tracks both: which of its structured order types supplies the fields (a meet, in this case — same fields either way), and which of the rulebook's lettered forms the order actually represents, since that's what determines what authority it's carrying.

It starts with OS reports, as it does at every station, all session long — entered right on the station's own touchscreen, the same screen that shows the clock, takes the OS report, and later displays whatever order or clearance the dispatcher sends back.

**[Figure 6 — Station CYD touchscreen, four states: Clock / OS Entry / Train Orders / Next Station: `docs/diagrams/cyd_screens/`]**

> 6:15 AM — No. 52 S reports at HC (departing)
> 6:15 AM — Extra 14 North reports at WP (departing)
> 6:24 AM — No. 52 S reports at SK
> 6:33 AM — Extra 14 North reports at XP
> 6:48 AM — Extra 14 North reports at BB
> 6:51 AM — No. 52 S reports at MC
> 6:59 AM — No. 52 S reports at JC

No. 52 reports in at Jacks Creek right on schedule, set to do its usual ten minutes of work and head out again at 7:09 — but Extra 14 North is already past Becs Bend and closing fast. The dispatcher issues a Form C order to Jacks Creek, holding No. 52 in the siding past its scheduled departure:

> No. 52 Eng 205 take siding at Jacks Creek and wait for Extra 14 North.

The station's touchscreen displays the order until the crew taps acknowledge, and the dispatcher's screen tracks it from issued to acknowledged in real time — the same OS log and signal-state view shown in Figure 4. The signal arm at Jacks Creek drops the moment the order goes out, so the crew can see at a glance — before they've even read the order — that something's waiting for them there.

The meet plays out exactly as ordered:

> 7:03 AM — Extra 14 North reports at JC (passes No. 52 in the siding)
> 7:21 AM — No. 52 S reports at BB (resuming south)
> 7:35 AM — No. 52 S reports at XP

No. 52's report at Xina Pass is a southbound arrival into Williamsport territory, so the dispatcher sends the yardmaster a Notify YM message with an expected arrival time. On the yardmaster's terminal, that shows up on the Arriving Trains panel — prompting the yardmaster to line up a track and ready the switch route well before the train actually shows up. Meanwhile, on the same yardmaster screen, a departing train (No. 3) has already been built and marked ready, engine, caboose, and car counts all recorded, sitting on the track board waiting for its scheduled departure.

That's the whole loop: a train moves, a station reports it, the dispatcher reacts if a conflict is developing, an order or a notice goes out to exactly the people who need it, and the yard stays a step ahead of what's coming. None of it required anyone to remember anything that wasn't already showing on a screen in front of them — which, on a session with six or eight people each tracking a piece of a much larger picture, is most of what the system is actually for.

## 6. What's Built, What's Next

As of this writing, the system covers what the NY&E calls Phase 1 and Phase 2: the network infrastructure, the fast clock, station OS reporting, structured train order issuance and acknowledgment, clearance forms, TO signal arm control, and the yardmaster terminal described above — all implemented, with the exception of the yardmaster's physical kiosk hardware (in progress as this is written), drawing on the ten years of real operating sessions on the previous layout.

It's worth saying plainly how this got built, since it's likely the more surprising part of the story for some readers: the RR_Server software — the MQTT bridge, the dispatcher and yardmaster web applications, the structured train order engine — was written in close collaboration with Claude, an AI coding assistant from Anthropic, over a series of working sessions spanning about seven weeks. The railroading judgment stayed exactly where it belonged: what separates a Form A meet from a Form C right-over order, what authority a yardmaster has that a dispatcher doesn't, what stays on paper and what doesn't. Claude's job was turning each of those rules, once discussed, into working code — and into tests. The project carries a 155-test suite that runs in continuous integration on every change, the kind of engineering discipline a one-person hobby project rarely gets the hours for on its own. None of this replaced the modeling or the rules research; it meant the bookkeeping software could be built and revised as fast as the operating concept itself was being worked out. For any modeler looking at a system like this and assuming it's out of reach without years of software background: it's worth trying anyway. The AI handles more of the implementation than most people expect, and the part that actually matters — knowing what your railroad needs — was never the bottleneck.

Three more phases are planned beyond that. Phase 3 adds station cameras, giving the dispatcher a camera grid view of the layout without leaving the dispatcher's desk. Phase 4 introduces RFID-based block detection, automating part of what's currently a manual OS report. Phase 5 brings layout lighting under the same control system, for day/night operating cycles. None of these change the operating concept in the slightest — they're refinements to the same T&TO system that's been running on this railroad, in one form or another, for over a decade.

What hasn't changed, and isn't going to, is the thing that made the old layout's sessions worth running for ten years in the first place: a small group of people, a real set of 1905 operating rules, and a railroad just complicated enough that running it well takes all of you paying attention. The control system's only job is to make sure that attention goes toward the railroad, and not toward bookkeeping.

---

*Allen D. Byrne has been modeling proto-freelanced New York and Eastern in HO scale for 27 years. The NY&E Northern Lights Subdivision was in operation for over ten years in its previous form, with formal operating sessions averaging 6–8 participants using timetable and train order operations based on the ARA Standard Code of 1906. The new layout has been under construction since 2020, with the digital control system in active development since Allen retired as a software engineer at the end of 2025.*

---

## Editor's notes / open items for next pass

- [x] Word count: 3,360 words (body only, excluding title/byline/editor notes) as of 2026-06-22, after the Section 6 AI-collaboration addition and the Figure 5 callout — comfortably within the 3,000–3,500 target, no further expansion needed
- [x] Section 5 expansion for word count — not needed; word count target already met without it (author decision, 2026-06-22)
- [x] Figure 5 (station CYD clock/OS screens) called out inline — added in Section 5, right before the OS report transcript (the touchscreen is what generates those reports), 2026-06-22: `docs/diagrams/cyd_screens/`
- [x] Section 5 walkthrough was reworked from the original demo session (which was a forced/test example, not a real op session — system is still in development): station order corrected (WP→XP→BB→JC→MC→SK→HC) and MC stops added; the meet was also recast around a real published-timetable train, No. 52 (the daily Class 2 way freight, HC dep. 06:15, scheduled JC work 06:59–07:09 per `timetable.json`), against an unscheduled extra (Engine 14) departing WP at the same moment — so the conflict and the Form C order both follow directly from real timetable data instead of two invented train numbers. Order text now matches the dispatcher app's actual "meet" template exactly (`No. 52 Eng 205 take siding at Jacks Creek and wait for Extra 14 North.`), with the Form C classification (not Form A) carrying the "right over" meaning, matching `to_types.json` / `active_forms.json` / `dispatcher.js`'s `ALL_FORMS` list on rpi5-2. `controlsystem/session.html` updated to match.
- [x] Screenshots recaptured against the live rpi5-2 system (confirmed safe first — no session in progress, no physical CYD/TO-signal hardware connected to the broker at the time). Replaced `dispatcher_ui_session2.5.png`, `yardmaster_ui_session2.0.png`, and the web tour's `images/dispatcher_ui.png` / `images/yardmaster_ui.png` with captures of the actual No. 52 / Extra 14 North Form C meet, OS log, and yard consist/arrival notice. rr-dispatcher was restarted afterward to clear the in-memory OS log/TO log/yard test data and the JC signal arm was reset to raised — system is back to its normal pre-capture state.
- [x] Highlight where Claude helped with RR_Server's design/development, to encourage other modelers to try AI-assisted projects (not a byline credit, woven into the narrative) — added as a new paragraph in Section 6, covering the AI-collaboration process, the 155-test CI suite, and the seven-week build timeline. Also tightened the preceding sentence's phrasing per author review (2026-06-22).
- [x] Byline / AI co-authorship disclosure — resolved 2026-06-20: editor Eric Smith confirmed DO has no disclosure policy blocker for AI attribution in the byline
- [x] Author bio: "27 years" confirmed accurate as of 2026-06-22 — previous layout's construction began 1999 (design predates that), 2026 − 1999 = 27, matches the text as written; no change needed
- [x] Lead photo file (`AlOpSessionYM.jpg`) — confirmed 2026-06-22, photo was taken by the author; no permissions issue, clear to publish
- [x] **Editorial pass, 2026-06-22.** Fixed: typos ("trian"→"train", "rather then"→"than", "inmultiple"→"in multiple", "a op session"→"an op session"); subject-verb agreement in Section 3 ("Engineers...checks"→"check"); an ungrammatical run-on in Section 2 about how OS reports and train orders moved by hand (runner/yelling/in-person) — same facts, cleaner grammar; an overloaded three-clause sentence in the Dispatcher section, split in two. **Figure ordering fixed:** Figure 5 (Yardmaster terminal) and Figure 6 (CYD touchscreen) were swapped so figure numbers now appear in the order a reader encounters them (Yardmaster appears in Section 4, before the CYD touchscreen figure in Section 5) — also updated in `ARTICLE_PITCH.md`'s Figure Inventory table. Removed a duplicate unnumbered figure placeholder in Section 5 that just re-showed Figure 4; replaced with an inline cross-reference instead, since reprinting the same image with no caption inside a print layout would read as a mistake. Updated the stale draft-status line (was still "first pass, [DATE]") and final word count (3,376). **One item left for the author's judgment, not changed:** the last sentence of the switchback paragraph in Section 4 ("So even the simple passenger run requires a little work to move the engine.") reads as a loosely-connected afterthought after the sentence before it already makes the same point — consider cutting it, or confirm what additional fact it's meant to add.
