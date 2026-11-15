# Decomposing_Health_Data_Hub_Problems_for_AI_Systems_Design

Source: https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-health-data-hub

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Decomposing the Problem: The Health Data Hub

Break down the National Health Data Office's request to integrate national health data from multiple sources. Identify data sources, their characteristics, and the systems and users that consume the data. Define data freshness requirements, how they will be measured, and which users or systems are authorised to link records across sources. Translate these findings into system constraints and a proposed initial scope for agency approval.

We'll cover the following...

- [What “bring national health data together” means](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-health-data-hub#What-bring-national-health-data-together-means)
- [What the three source profiles must contain](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-health-data-hub#What-the-three-source-profiles-must-contain)
- [What five-minute freshness actually measures](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-health-data-hub#What-five-minute-freshness-actually-measures)
- [Who can associate HOSP-A/4172 with CLINIC-B/4172](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-health-data-hub#Who-can-associate-HOSP-A4172-with-CLINIC-B4172)
- [Where responsibility for LAB-884 passes next](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-health-data-hub#Where-responsibility-for-LAB-884-passes-next)
- [A first version the National Health Data Office can approve](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-health-data-hub#A-first-version-the-National-Health-Data-Office-can-approve)
- [Practice: Whether a weekly screening source can support same-day care access](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-health-data-hub#Practice-Whether-a-weekly-screening-source-can-support-same-day-care-access)

Care teams request recent laboratory reports, analysts need daily reporting extracts, and the project sponsor wants a unified patient record. Each request has different workflow, data freshness, access control, and decision-making requirements. Document these requirements separately during discovery to avoid embedding incorrect access, freshness, or record-linkage assumptions in the integration design.

## What “bring national health data together” means

Start with the work each consumer needs to complete:

- **Care access:** A source organisation publishes a laboratory report that an authorised care team can retrieve as part of its clinical workflow. Identify which clinical actions require access to the report and which organisation is responsible for follow-up.
- **National reporting:** Approved data from source systems is included in a daily reporting extract for national analysts. Define the required fields, population coverage, reporting period, and approvals for the extract.
- **Cross-source patient view:** The sponsor requires reports to be linked to individual patients. Identify who is authorised to establish these links and review uncertain matches.

Assign separate owners for technical delivery, patient record linkage, and clinical follow-up, and define the handoffs between them.

Use the CLIENT framework from Chapter 1 to structure discovery and produce a workflow-focused brief before designing the architecture.

Classify the information in the discovery brief as follows:

- **Given case facts:** The National Health Data Office is the client, and the three stakeholder groups have submitted distinct requests.
- **Working assumptions:** The initial care-access scope includes laboratory reports issued by two participating organisations: a hospital laboratory and a clinic network. A separate daily reporting extract may include data exported by a regional laboratory, subject to approval.
- **Unresolved questions:** Confirm the receiving organisations, access ...