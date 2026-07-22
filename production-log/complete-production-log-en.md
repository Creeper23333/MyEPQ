# PL-00 Complete Production Log — English Candidate-Review Draft

<!-- PAIR: PL-00.01 -->
## PL-00.01 Document control

| Field ID | Field | Entry |
| --- | --- | --- |
| PL-00.01-A | Document status | Candidate-review draft. Every first-person statement must be checked by the candidate before it is transferred to a centre-issued form. |
| PL-00.01-B | Version date | 2026-07-20 |
| PL-00.01-C | Official-use status | This is a structured evidence document, not a signed OxfordAQA form. The candidate's own blank/current centre-issued form takes precedence. |
| PL-00.01-D | English/Chinese parity | This file and zh-cn/complete-production-log-zh-cn.md use the same section IDs, table rows, evidence references and placeholder tokens. |
| PL-00.01-E | Repository inclusion rule | No third-party or partially populated form is tracked. The candidate must use their own current centre-issued form. |
| PL-00.01-F | Historical-document rule | Superseded fragments and unverified extracts are excluded from the current tree. Git history is used for process traceability. |

<!-- PAIR: PL-00.02 -->
## PL-00.02 Evidence and authorship rules

1. **Candidate-only fields:** identity, qualifications, first-person decisions, declarations, dates and signatures remain subject to candidate confirmation.
2. **Supervisor-only fields:** authentication, taught skills, comments, approval, marks, presentation observations and signatures remain placeholders for the real supervisor.
3. **Centre-coordinator-only fields:** approval, recommendations, name, signature and date remain placeholders.
4. **Presentation evidence:** audience details, delivery observations and five questions and answers are recorded only after the real presentation.
5. **Repository evidence:** a commit, generated metadata file or saved output supports what the repository contained; it does not by itself prove who personally performed or understood the work.
6. **AI assistance:** the final disclosure must describe the actual use of OpenAI Codex and other tools, including any code editing, testing, data refresh, analysis, drafting or translation that occurred.

---

<!-- PAIR: PL-01.01 -->
## PL-01 Candidate record and declarations

### PL-01.01 Candidate and centre details

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-01.01-A | Centre number | {{CENTRE_NUMBER}} |
| PL-01.01-B | Centre name | {{CENTRE_NAME}} |
| PL-01.01-C | Candidate number | {{CANDIDATE_NUMBER}} |
| PL-01.01-D | Candidate full name | {{CANDIDATE_FULL_NAME}} |
| PL-01.01-E | Supervisor full name | {{SUPERVISOR_FULL_NAME}} |
| PL-01.01-F | Working title | To what extent can machine learning models improve Bitcoin volatility forecasting compared with traditional statistical models? |
| PL-01.01-G | Final title | Accuracy, Interpretability and Practicality in Bitcoin Volatility Forecasting: Machine Learning versus Statistical Models |

<!-- PAIR: PL-01.02 -->
### PL-01.02 Assistance and materials declaration

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-01.02-A | Help or information received beyond the supervisor | {{ASSISTANCE_YES_NO_AND_DETAILS}} |
| PL-01.02-B | AI assistance, candidate-verified wording | {{AI_ASSISTANCE_SCOPE_CANDIDATE_VERIFIED}} |
| PL-01.02-C | Other software and data services requiring disclosure | Python, NumPy, pandas, Pillow, PyTorch and Hyperliquid's public information API were used in the repository. The candidate must confirm the final list, versions where required, and which items are already acknowledged in the report. |
| PL-01.02-D | Other people or specialist consultants | {{OTHER_PEOPLE_OR_CONSULTANTS}} |
| PL-01.02-E | Materials not otherwise acknowledged | {{OTHER_UNACKNOWLEDGED_MATERIALS}} |

Candidate-review disclosure draft:

> OpenAI Codex was used during repository inspection, code review and editing, software testing, data refreshes, output checking, report and production-log drafting, consistency review and English–Chinese translation. The candidate must replace this draft with a precise account of the functions actually used, the work personally checked, and any limits set by the centre. Python libraries and Hyperliquid's public information API supported data processing and modelling. Academic and technical sources used in the investigation are listed in the report.

<!-- PAIR: PL-01.03 -->
### PL-01.03 Declarations

| Field ID | Declaration item | Entry |
| --- | --- | --- |
| PL-01.03-A | Candidate confirms that the submitted account is accurate and that assistance is disclosed | {{CANDIDATE_DECLARATION_CONFIRMED}} |
| PL-01.03-B | Candidate signature | {{CANDIDATE_SIGNATURE_OFFICIAL_FORM_ONLY}} |
| PL-01.03-C | Candidate declaration date | {{CANDIDATE_DECLARATION_DATE}} |
| PL-01.03-D | Supervisor authentication and declaration | {{SUPERVISOR_DECLARATION_OFFICIAL_FORM_ONLY}} |
| PL-01.03-E | Supervisor signature | {{SUPERVISOR_SIGNATURE_OFFICIAL_FORM_ONLY}} |
| PL-01.03-F | Supervisor declaration date | {{SUPERVISOR_DECLARATION_DATE}} |

---

<!-- PAIR: PL-02.01 -->
## PL-02 Submission checklist

### PL-02.01 Supervisor-completed checklist

| Field ID | Item | Status |
| --- | --- | --- |
| PL-02.01-A | Signed candidate record, production log and assessment record | {{SUPERVISOR_CHECK_FORM_COMPLETE}} |
| PL-02.01-B | Research-based written report within the required word range | {{SUPERVISOR_CHECK_REPORT}} |
| PL-02.01-C | Presentation evidence within the production log | {{SUPERVISOR_CHECK_PRESENTATION}} |
| PL-02.01-D | Working title recorded | {{SUPERVISOR_CHECK_WORKING_TITLE}} |
| PL-02.01-E | Final title recorded | {{SUPERVISOR_CHECK_FINAL_TITLE}} |
| PL-02.01-F | Final report body word count before references | 5,356 |

---

<!-- PAIR: PL-03.01 -->
## PL-03 Taught skills

### PL-03.01 Supervisor record

This section must describe skills genuinely taught by the centre or supervisor. Possible categories visible in the project include research-question refinement, source evaluation, referencing, project planning, statistical interpretation, coding validation, presentation structure and reflection, but only the supervisor may confirm what was actually taught.

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-03.01-A | Group or class skills taught | {{SUPERVISOR_TAUGHT_SKILLS_GROUP}} |
| PL-03.01-B | Individual skills taught | {{SUPERVISOR_TAUGHT_SKILLS_INDIVIDUAL}} |
| PL-03.01-C | Dates or scheme-of-work reference | {{SUPERVISOR_TAUGHT_SKILLS_DATES_OR_REFERENCE}} |
| PL-03.01-D | Supervisor supporting evidence | {{SUPERVISOR_TAUGHT_SKILLS_EVIDENCE}} |

---

<!-- PAIR: PL-04.01 -->
## PL-04 Record of marks and authentication

### PL-04.01 Compulsory-element checks

| Field ID | Assessment evidence | Supervisor entry |
| --- | --- | --- |
| PL-04.01-A | Area of interest identified and selected | {{SUPERVISOR_MARK_CHECK_TOPIC}} |
| PL-04.01-B | Working title set | {{SUPERVISOR_MARK_CHECK_WORKING_TITLE}} |
| PL-04.01-C | Project plan produced | {{SUPERVISOR_MARK_CHECK_PLAN}} |
| PL-04.01-D | Plan implemented and changes documented | {{SUPERVISOR_MARK_CHECK_IMPLEMENTATION}} |
| PL-04.01-E | Product addresses final title | {{SUPERVISOR_MARK_CHECK_PRODUCT}} |
| PL-04.01-F | Referencing method used | {{SUPERVISOR_MARK_CHECK_REFERENCING}} |
| PL-04.01-G | Findings communicated in report and presentation | {{SUPERVISOR_MARK_CHECK_COMMUNICATION}} |
| PL-04.01-H | Bibliography or reference list included | {{SUPERVISOR_MARK_CHECK_BIBLIOGRAPHY}} |
| PL-04.01-I | Strengths and weaknesses evaluated | {{SUPERVISOR_MARK_CHECK_EVALUATION}} |

<!-- PAIR: PL-04.02 -->
### PL-04.02 Marks and comments

| Field ID | Skill area | Maximum | Supervisor mark | Supervisor supporting statement |
| --- | --- | ---: | --- | --- |
| PL-04.02-A | AO1 Selection of topic | 6 | {{AO1_MARK}} | {{AO1_SUPPORTING_STATEMENT}} |
| PL-04.02-B | AO2 Planning, monitoring and developing | 12 | {{AO2_MARK}} | {{AO2_SUPPORTING_STATEMENT}} |
| PL-04.02-C | AO3 Demonstration of research skills | 12 | {{AO3_MARK}} | {{AO3_SUPPORTING_STATEMENT}} |
| PL-04.02-D | AO4 Analysis and application of research | 24 | {{AO4_MARK}} | {{AO4_SUPPORTING_STATEMENT}} |
| PL-04.02-E | AO5 Evaluation of product, process and self | 6 | {{AO5_MARK}} | {{AO5_SUPPORTING_STATEMENT}} |
| PL-04.02-F | Total | 60 | {{TOTAL_MARK}} | {{SUPERVISOR_CONCLUDING_COMMENTS}} |
| PL-04.02-G | Internal moderation comments | — | {{INTERNAL_MODERATION_STATUS}} | {{INTERNAL_MODERATION_COMMENTS}} |
| PL-04.02-H | Supervisor final signature and date | — | {{SUPERVISOR_FINAL_SIGNATURE_OFFICIAL_FORM_ONLY}} | {{SUPERVISOR_FINAL_DATE}} |

---

<!-- PAIR: PL-05.01 -->
## PL-05 Record of initial ideas

### PL-05.01 Provenance note

The repository does not contain an independently authenticated, dated initial-ideas record. The earliest verifiable project direction is the repository setup recorded in commit 8aee51f. The entries below therefore preserve only that verifiable direction and leave earlier alternatives for the candidate to supply from genuine memory or evidence.

<!-- PAIR: PL-05.02 -->
### PL-05.02 Ideas considered

| Field ID | Initial idea | Candidate confirmation and evidence |
| --- | --- | --- |
| PL-05.02-A | Bitcoin or cryptocurrency volatility forecasting using statistical and machine-learning models | Supported as the selected direction by the first repository commit and candidate proposal materials; candidate confirmation: {{INITIAL_IDEA_1_CONFIRMED}} |
| PL-05.02-B | {{INITIAL_IDEA_2_CANDIDATE_CONFIRMED}} | {{INITIAL_IDEA_2_EVIDENCE_OR_MEMORY_NOTE}} |
| PL-05.02-C | {{INITIAL_IDEA_3_CANDIDATE_CONFIRMED}} | {{INITIAL_IDEA_3_EVIDENCE_OR_MEMORY_NOTE}} |

<!-- PAIR: PL-05.03 -->
### PL-05.03 Preliminary research and selection

Candidate-review draft:

> I selected Bitcoin volatility forecasting because it connects my interests in mathematics, computing and finance and gives me a question that can be tested with real data. It also lets me compare whether a more complicated method actually gives a useful improvement. Before using this wording, I will confirm that it matches my own reasons at the start of the project.

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-05.03-A | Real preliminary sources consulted | {{INITIAL_RESEARCH_SOURCES_AND_DATES}} |
| PL-05.03-B | Actual initial supervisor comments | {{INITIAL_SUPERVISOR_COMMENTS}} |
| PL-05.03-C | Changes made after the initial meeting | {{INITIAL_MEETING_MODIFICATIONS}} |
| PL-05.03-D | Initial-meeting date | {{INITIAL_MEETING_DATE}} |

<!-- PAIR: PL-05.04 -->
### PL-05.04 Proposed title, aim and objectives

**Proposed title recorded in the first tracked proposal:**
To what extent can machine learning models improve Bitcoin volatility forecasting compared with traditional statistical models?

**Proposed aim:**
To compare several ways of forecasting Bitcoin volatility and decide whether the more complicated machine-learning methods give enough extra benefit to justify their use.

**Proposed objectives:**

1. Read about Bitcoin returns, volatility and the selected forecasting methods.
2. Collect and prepare a consistent set of daily Bitcoin data.
3. Build two clear statistical comparison methods.
4. Build Random Forest and, if manageable, an LSTM for comparison.
5. Test every method on the same time-ordered data and compare the errors.
6. Consider accuracy together with ease of explanation, time required and important limitations.

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-05.04-A | Candidate confirms that this reflects the actual initial proposal | {{INITIAL_PROPOSAL_CANDIDATE_CONFIRMED}} |
| PL-05.04-B | Date entered on the candidate's official record | {{INITIAL_PROPOSAL_DATE}} |

<!-- PAIR: PL-06.01 -->
## PL-06 Part A: Candidate proposal

### PL-06.01 Working title and focus

**Working title:**
To what extent can machine learning models improve Bitcoin volatility forecasting compared with traditional statistical models?

**Focused research question developed from it:**
When the same Bitcoin data and testing period are used, do Random Forest and LSTM give a useful improvement over two clearer statistical approaches, and are they still practical and understandable enough for this project?

<!-- PAIR: PL-06.02 -->
### PL-06.02 Initial resources

Candidate-review draft:

> At the proposal stage, I planned to use daily Bitcoin data, academic and educational reading about forecasting, Python to organise the data and run the comparisons, a source-evaluation workbook, saved results and a time-ordered test. The first plan named Yahoo Finance, but the documented project later changed to Hyperliquid. I will keep this change visible instead of rewriting the starting plan.

| Field ID | Resource category | Planned resource |
| --- | --- | --- |
| PL-06.02-A | Market data | Daily Bitcoin data; the first tracked plan named Yahoo Finance |
| PL-06.02-B | Background reading | Sources explaining returns, volatility and established forecasting methods |
| PL-06.02-C | Comparison reading | Sources explaining the selected machine-learning methods |
| PL-06.02-D | Evaluation | Common error measures and a test that keeps the original time order |
| PL-06.02-E | Tools | Python, the source-evaluation workbook, saved tables and charts |
| PL-06.02-F | Actual sources available at the proposal date | {{PROPOSAL_STAGE_SOURCE_LIST_CANDIDATE_CONFIRMED}} |

<!-- PAIR: PL-06.03 -->
### PL-06.03 Relation to courses and personal interests

Candidate-review draft:

> The topic connects my interests in mathematics, computer science and quantitative finance. It applies statistics and probability to a real time series, requires programming and data-quality decisions, and extends beyond a standard classroom exercise by requiring comparison of research methods, uncertainty, interpretation and practical limitations.

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-06.03-A | Candidate confirms the personal-interest statement | {{PERSONAL_INTEREST_STATEMENT_CONFIRMED}} |
| PL-06.03-B | Qualification 1 and awarding body/subject | {{QUALIFICATION_1_AND_AWARDING_BODY_SUBJECT}} |
| PL-06.03-C | Qualification 2 and awarding body/subject | {{QUALIFICATION_2_AND_AWARDING_BODY_SUBJECT}} |
| PL-06.03-D | Qualification 3 and awarding body/subject | {{QUALIFICATION_3_AND_AWARDING_BODY_SUBJECT}} |
| PL-06.03-E | Other relevant course or interest | {{OTHER_RELEVANT_COURSE_OR_INTEREST}} |

<!-- PAIR: PL-06.04 -->
### PL-06.04 Aim and objectives at proposal stage

**Aim:**
To decide whether the extra complication of the selected machine-learning approaches is worthwhile when compared with clearer statistical approaches to Bitcoin volatility forecasting.

**Objectives at this stage:**

1. Explain the key ideas behind Bitcoin returns and volatility in accessible language.
2. Prepare a reliable daily Bitcoin dataset for the comparison.
3. Build two statistical reference methods.
4. Build Random Forest and attempt a small LSTM after the first comparison works.
5. Keep the data in time order and compare every method using the same error measures.
6. Discuss accuracy, ease of explanation, practical use and limitations.

Later extra checks belong in the review sections because they were not part of the original proposal.

<!-- PAIR: PL-06.05 -->
### PL-06.05 Proposal declaration and date

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-06.05-A | Candidate confirms the proposal accurately reflects the plan at that time | {{PROPOSAL_CANDIDATE_CONFIRMED}} |
| PL-06.05-B | Candidate signature | {{PROPOSAL_CANDIDATE_SIGNATURE_OFFICIAL_FORM_ONLY}} |
| PL-06.05-C | Proposal date | {{PROPOSAL_DATE}} |

---

<!-- PAIR: PL-07.01 -->
## PL-07 Part B: Supervisor comments on candidate proposal

### PL-07.01 Supervisor-only entries

| Field ID | Required supervisor judgment | Entry |
| --- | --- | --- |
| PL-07.01-A | Relation to and extension beyond the candidate's courses or interests | {{SUPERVISOR_PROPOSAL_COURSE_EXTENSION_COMMENT}} |
| PL-07.01-B | Suitability of initial sources and research base | {{SUPERVISOR_PROPOSAL_SOURCES_COMMENT}} |
| PL-07.01-C | Feasibility within the timescale and possible difficulties | {{SUPERVISOR_PROPOSAL_FEASIBILITY_COMMENT}} |
| PL-07.01-D | Suitability of title, aim and objectives | {{SUPERVISOR_PROPOSAL_TITLE_AIM_COMMENT}} |
| PL-07.01-E | Supervisor signature | {{SUPERVISOR_PROPOSAL_SIGNATURE_OFFICIAL_FORM_ONLY}} |
| PL-07.01-F | Supervisor proposal date | {{SUPERVISOR_PROPOSAL_DATE}} |

No repository file authenticates supervisor wording. The placeholders below must not be replaced with a quotation or signed supervisor statement unless the real source is confirmed.

---

<!-- PAIR: PL-08.01 -->
## PL-08 Part C: Centre coordinator approval

### PL-08.01 Centre-coordinator-only entries

| Field ID | Required coordinator information | Entry |
| --- | --- | --- |
| PL-08.01-A | Supervisor name | {{SUPERVISOR_FULL_NAME}} |
| PL-08.01-B | Feasibility and acceptability comments | {{CENTRE_COORDINATOR_COMMENTS}} |
| PL-08.01-C | Decision | {{CENTRE_COORDINATOR_APPROVAL_DECISION}} |
| PL-08.01-D | Recommendations or conditions | {{CENTRE_COORDINATOR_RECOMMENDATIONS}} |
| PL-08.01-E | Centre coordinator name | {{CENTRE_COORDINATOR_NAME}} |
| PL-08.01-F | Centre coordinator signature | {{CENTRE_COORDINATOR_SIGNATURE_OFFICIAL_FORM_ONLY}} |
| PL-08.01-G | Approval date | {{CENTRE_COORDINATOR_APPROVAL_DATE}} |

---

<!-- PAIR: PL-09.01 -->
## PL-09 Planning review

### PL-09.01 Progress and next steps

Candidate-review draft:

> I narrowed the project from a broad cryptocurrency-prediction idea to a focused Bitcoin volatility comparison. I planned to begin with clear reference methods, keep the dates in order, save both the original and prepared data and produce tables and charts that could be checked. I also decided to compare clarity and practicality as well as accuracy, because a slightly lower error would not automatically make a more complicated method the better choice.

| Field ID | Planned stage | Original target | Resource or evidence |
| --- | --- | --- | --- |
| PL-09.01-A | Refine the question and objectives | 2026-06-17 | Candidate proposal, report outline and feedback summary |
| PL-09.01-B | Collect and evaluate sources | 2026-06-18 | Research notes, search log and source-evaluation workbook |
| PL-09.01-C | Complete the planning review | 2026-06-19 | Planning-review draft |
| PL-09.01-D | Download, check and organise the Bitcoin data | 2026-06-22 | Original data, prepared dataset and data notes |
| PL-09.01-E | Build the first two comparison methods | 2026-06-25 | Saved work and result tables |
| PL-09.01-F | Build the two machine-learning comparisons | 2026-06-30 | Saved work, settings and results |
| PL-09.01-G | Compare the results | 2026-07-03 | Error table and forecast chart |
| PL-09.01-H | Complete the mid-project review | 2026-07-05 | Mid-project review draft |
| PL-09.01-I | Draft the report | 2026-07-20 | Section drafts and combined report |
| PL-09.01-J | Prepare the presentation and final reflection | 2026-07-31 | Slides, script, Q&A preparation and reflection |

These dates show the plan, not proof that every task was completed on its target date.

<!-- PAIR: PL-09.02 -->
### PL-09.02 Reasons for decisions

| Field ID | Decision | Reason |
| --- | --- | --- |
| PL-09.02-A | Focus on Bitcoin rather than several cryptocurrencies | One asset allowed a deeper and more manageable project. |
| PL-09.02-B | Begin with two clear reference methods | They provided understandable results against which the later methods could be judged. |
| PL-09.02-C | Compare Random Forest and LSTM | They represented two different machine-learning approaches without making the project too wide. |
| PL-09.02-D | Keep the original time order | Using future information to judge an earlier prediction would be unfair. |
| PL-09.02-E | Change the planned data source to Hyperliquid | This gave the project one clearly defined Bitcoin market. |
| PL-09.02-F | Compare more than accuracy | Ease of explanation, time required and consistency also affect whether extra complexity is useful. |

<!-- PAIR: PL-09.03 -->
### PL-09.03 Supervisor advice and response

The repository contains a candidate-side summary suggesting that the comparison should go beyond simply ranking the error figures and should explain more clearly what was being compared. It is not an authenticated supervisor quotation.

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-09.03-A | Actual supervisor advice, quotation or approved paraphrase | {{PLANNING_SUPERVISOR_ADVICE_APPROVED}} |
| PL-09.03-B | Date and medium of the advice | {{PLANNING_SUPERVISOR_ADVICE_DATE_AND_MEDIUM}} |
| PL-09.03-C | Candidate response | I added clearer comparison points covering explanation, time required, repeatability and whether the result stayed similar after further checks. Candidate confirmation: {{PLANNING_RESPONSE_CONFIRMED}} |
| PL-09.03-D | Centre-coordinator recommendation implemented | {{PLANNING_COORDINATOR_RECOMMENDATION_RESPONSE}} |
| PL-09.03-E | Planning-review date | {{PLANNING_REVIEW_DATE}} |

<!-- PAIR: PL-09.04 -->
### PL-09.04 Evidence appended

- the proposal material consolidated in PL-05 and PL-06;
- appendix timetable and risk assessment;
- research source list, literature notes, search log and source-evaluation workbook;
- data-source decision record;
- initial code and output files.

---

<!-- PAIR: PL-10.01 -->
## PL-10 Mid-project review

### PL-10.01 Development from the plan

The timetable recorded 2026-07-05 as the target for this review, but the repository does not prove that a formal review occurred on that date. The official date remains {{MID_REVIEW_DATE}}.

Candidate-review draft:

> The project kept its main Bitcoin topic but became more focused. I removed Ethereum so that I could study one market in more depth and changed the data source from Yahoo Finance to Hyperliquid. I built the planned comparison methods and added one extra simple method to check whether the more complicated approaches were really necessary. I kept the data in time order and became more careful about explaining that the chosen daily volatility measure is only an estimate, so the conclusion should not be applied too widely.

<!-- PAIR: PL-10.02 -->
### PL-10.02 Problems identified

| Field ID | Problem | Response planned at the mid-project stage |
| --- | --- | --- |
| PL-10.02-A | The project measures volatility indirectly | Define the measure clearly and keep this limitation visible. |
| PL-10.02-B | Neighbouring daily results are closely related | Keep the dates in order and avoid treating every row as completely separate. |
| PL-10.02-C | The dataset is not large for the most complicated method | Keep that method small and make a cautious comparison. |
| PL-10.02-D | Some methods are harder to explain | Include clarity as part of the final judgement. |
| PL-10.02-E | An early result could contain a data or date mistake | Check the dates, input data and calculations before accepting the ranking. |
| PL-10.02-F | Weekly administration had not always been recorded | Reconstruct only what the saved evidence supports and leave gaps visible. |

<!-- PAIR: PL-10.03 -->
### PL-10.03 Supervisor advice and modifications

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-10.03-A | Actual mid-project supervisor comments | {{MID_SUPERVISOR_COMMENTS}} |
| PL-10.03-B | Date and medium of comments | {{MID_SUPERVISOR_COMMENTS_DATE_AND_MEDIUM}} |
| PL-10.03-C | Modifications made in response | {{MID_MODIFICATIONS_AFTER_SUPERVISOR_DISCUSSION}} |
| PL-10.03-D | Candidate confirms the development account | {{MID_DEVELOPMENT_ACCOUNT_CONFIRMED}} |

<!-- PAIR: PL-10.04 -->
### PL-10.04 Final title, aim and objectives

**Final title:**
Accuracy, Interpretability and Practicality in Bitcoin Volatility Forecasting: Machine Learning versus Statistical Models

**Final aim:**
To judge whether Random Forest and LSTM provide enough benefit to justify their extra complexity when compared with clearer statistical approaches.

**Revised objectives:**

1. Explain the chosen measure of Bitcoin volatility.
2. Collect, organise and check the daily Bitcoin data.
3. Build the selected statistical and machine-learning comparisons.
4. Test every method on the same time-ordered data.
5. Compare accuracy, clarity, time required and repeatability.
6. Check that dates, data preparation and results match correctly.
7. Repeat the comparison in several reasonable ways to see whether the conclusion changes.
8. Give a careful conclusion limited to this project.

<!-- PAIR: PL-10.05 -->
### PL-10.05 Planned next steps

1. Complete the final planned method and check that it uses only the information available at the time.
2. Check that every prediction is matched to the correct date and comparison value.
3. Repeat the full comparison after any important correction.
4. Try at least one reasonable alternative way of measuring volatility.
5. Expand the report's research, method, results, discussion and conclusion sections.
6. Prepare the presentation and record the real questions after it is delivered.

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-10.05-A | Candidate confirms these were genuine next steps at the review date | {{MID_NEXT_STEPS_CONFIRMED}} |
| PL-10.05-B | Mid-project review signature/date entry | {{MID_REVIEW_SIGNATURE_AND_DATE_OFFICIAL_FORM_ONLY}} |

<!-- PAIR: PL-11.01 -->
## PL-11 Project product review

### PL-11.01 Product and adherence to the revised plan

Candidate-review draft:

> The main product is a research report supported by saved Bitcoin data, the work used to run the comparisons, result tables, a chart, source evaluation and presentation preparation. The topic stayed consistent with the revised plan, but the checking process became more careful after I found problems with dates and an incomplete day of data. I have kept those changes visible because they show how the project developed.

| Field ID | Current product item | Evidence or status |
| --- | --- | --- |
| PL-11.01-A | English research report | report/final-report.md; current body count: 5,356 |
| PL-11.01-B | Saved comparison work and checks | code folder, test folder and run files; 39 checks currently pass |
| PL-11.01-C | Market data and data-quality record | Completed daily Hyperliquid records; 1,240 completed days retained |
| PL-11.01-D | Results evidence | Saved predictions, comparison figures and supporting checks |
| PL-11.01-E | Research evidence | Source list, reading notes, search log and source-evaluation workbook |
| PL-11.01-F | Presentation preparation | Slide outline, script and Q&A preparation; final slide file: {{FINAL_PRESENTATION_FILE}} |

<!-- PAIR: PL-11.02 -->
### PL-11.02 Major development and checking record

| Field ID | Development | Effect on the project |
| --- | --- | --- |
| PL-11.02-A | The data source changed from Yahoo Finance to Hyperliquid | The study used one clearly identified Bitcoin market. |
| PL-11.02-B | An extra simple comparison was added | It helped show whether a more complicated method was actually needed. |
| PL-11.02-C | The final planned method was completed and the files were reorganised | The full comparison became easier to repeat and review. |
| PL-11.02-D | Predictions were matched using dates | This corrected the risk of connecting a result to the wrong day. |
| PL-11.02-E | One calculation step was corrected | The result no longer used information from the wrong point in time. |
| PL-11.02-F | The volatility calculation was checked and corrected | The target was calculated more consistently. |
| PL-11.02-G | Data preparation for the final method was limited to the correct period | Later information was kept out of an earlier stage. |
| PL-11.02-H | The still-open daily record was excluded | Only completed days entered the final comparison. |
| PL-11.02-I | The comparison was repeated under several reasonable settings | This showed whether the main conclusion was stable. |

The candidate must describe personal involvement accurately. Any statement about creating or correcting work should explain truthfully what was completed with AI assistance and what the candidate personally reviewed or tested.

<!-- PAIR: PL-11.03 -->
### PL-11.03 Current 2026-07-20 evidence snapshot

The values below come from the data refresh and full comparison completed on 2026-07-20. More detailed figures remain in the report and saved output files.

| Field ID | Measure | Current value |
| --- | --- | --- |
| PL-11.03-A | Refresh date | 2026-07-20 |
| PL-11.03-B | Time the data was collected | 2026-07-20T06:12:26+00:00 |
| PL-11.03-C | Daily records returned | 1,241 |
| PL-11.03-D | Unfinished records removed | 1 |
| PL-11.03-E | Completed daily records kept | 1,240 |
| PL-11.03-F | Last complete date | 2026-07-19 |
| PL-11.03-G | Rows used after preparation | 1,195 |
| PL-11.03-H | Earlier rows used for learning | 950 |
| PL-11.03-I | Later rows used for comparison | 245 |
| PL-11.03-J | Best main error figure | 0.00098502 |
| PL-11.03-K | Extra simple comparison | 0.00140087 |
| PL-11.03-L | Rolling comparison | 0.00142744 |
| PL-11.03-M | LSTM comparison | 0.00174351 |
| PL-11.03-N | Random Forest comparison | 0.00232370 |
| PL-11.03-O | Best result in the repeated time-based check | 0.00098681 |
| PL-11.03-P | Range from the uncertainty check | [-0.00099670, -0.00017158] |
| PL-11.03-Q | Automated checks passed | 39 |

<!-- PAIR: PL-11.04 -->
### PL-11.04 Successes and strengths

1. All main methods were compared using the same target and the same time order.
2. Results were saved in tables so that the figures could be checked again.
3. Important corrections were recorded instead of hiding the earlier problem.
4. The comparison was repeated in several ways to see whether the overall answer changed.
5. The final conclusion is limited to the market, dates and methods used in this project.

<!-- PAIR: PL-11.05 -->
### PL-11.05 Failures, limitations and lessons

1. The project estimates volatility from daily data rather than observing it directly.
2. Results for neighbouring days are closely related, so the evidence is not completely independent.
3. The Random Forest comparison is deliberately modest and was not tuned in every possible way.
4. The LSTM is small and the available dataset is limited for a complicated model.
5. One Bitcoin market cannot prove that the same result will hold everywhere.
6. Repeating the test across parts of the same history is not the same as using a completely new dataset.
7. Early weekly record-keeping was weaker than the later checking process.
8. Any AI-supported work and writing must be disclosed accurately and checked by the candidate.

<!-- PAIR: PL-11.06 -->
### PL-11.06 Supervisor advice, modifications and remaining work

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-11.06-A | Actual final-stage supervisor comments | {{PRODUCT_REVIEW_SUPERVISOR_COMMENTS}} |
| PL-11.06-B | Date and medium of comments | {{PRODUCT_REVIEW_SUPERVISOR_DATE_AND_MEDIUM}} |
| PL-11.06-C | Modifications made in response | {{PRODUCT_REVIEW_MODIFICATIONS}} |
| PL-11.06-D | Candidate confirms the product-review account | {{PRODUCT_REVIEW_ACCOUNT_CONFIRMED}} |
| PL-11.06-E | Remaining report or appendix work | {{REMAINING_REPORT_WORK}} |
| PL-11.06-F | Remaining administrative work | Complete the centre-issued form, candidate and supervisor declarations, dates, signatures and authorised sections. |
| PL-11.06-G | Remaining presentation work | Create or finalise the slide file, rehearse, deliver the presentation and record real Part B evidence. |
| PL-11.06-H | Product-review date | {{PRODUCT_REVIEW_DATE}} |

---

<!-- PAIR: PL-12.01 -->
## PL-12 Presentation record Part A

### PL-12.01 Planned format

Candidate-review draft:

> I plan a presentation of approximately ten minutes using about ten visually simple slides, brief speaker notes and the project's own result chart and tables. The intended audience must satisfy the centre's requirement and should include the supervisor and at least one other adult. I will explain the research decision and result rather than read report paragraphs from the screen.

| Field ID | Planning item | Entry |
| --- | --- | --- |
| PL-12.01-A | Intended presentation date | {{PRESENTATION_PLANNED_DATE}} |
| PL-12.01-B | Intended audience | {{PRESENTATION_PLANNED_AUDIENCE}} |
| PL-12.01-C | Planned duration | Approximately ten minutes |
| PL-12.01-D | Visual aids | Slides, validation timeline, comparison chart, robustness table and conclusion |
| PL-12.01-E | Notes | Brief speaker notes based on presentation/final-presentation-script.md |
| PL-12.01-F | Final slide file | {{FINAL_PRESENTATION_FILE}} |

<!-- PAIR: PL-12.02 -->
### PL-12.02 Planned project-process content

1. How I narrowed the question to Bitcoin volatility forecasting.
2. Why I changed the data source to Hyperliquid.
3. How I prepared the daily data and decided what to measure.
4. Why I kept the data in date order for a fair comparison.
5. How checking the dates, calculations and unfinished daily record changed the project.
6. How the research, results and limitations led to the final judgement.

<!-- PAIR: PL-12.03 -->
### PL-12.03 Planned findings and conclusion

The presentation will use the final checked values:

| Field ID | Finding | Value |
| --- | --- | --- |
| PL-12.03-A | Best result in the main comparison | GARCH(1,1) |
| PL-12.03-B | Best main error figure | 0.00098502 |
| PL-12.03-C | Simple rolling comparison | 0.00142744 |
| PL-12.03-D | Result with a shorter measurement period | The same method remained first, with an error of 0.00178208. |
| PL-12.03-E | Result when the comparison was repeated through time | The same method ranked first overall and in each of the four sections. |
| PL-12.03-F | Machine-learning result | Neither machine-learning method beat the simple rolling comparison. |

My conclusion will be careful: in this project, the tested machine-learning methods did not improve the result enough to justify their extra complexity. This does not prove that the same answer applies to every Bitcoin market or every machine-learning method.

<!-- PAIR: PL-12.04 -->
### PL-12.04 Rehearsal changes

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-12.04-A | Rehearsal date | {{REHEARSAL_DATE}} |
| PL-12.04-B | People present | {{REHEARSAL_AUDIENCE}} |
| PL-12.04-C | Timing observed | {{REHEARSAL_DURATION}} |
| PL-12.04-D | Changes to pace or slide density | {{REHEARSAL_PACE_AND_DENSITY_CHANGES}} |
| PL-12.04-E | Changes to explanation of the target or audit | {{REHEARSAL_EXPLANATION_CHANGES}} |
| PL-12.04-F | Candidate Part A date | {{PRESENTATION_PART_A_DATE}} |

---

<!-- PAIR: PL-13.01 -->
## PL-13 Presentation record Part B

### PL-13.01 Delivery record — supervisor only

No planned Q&A answer may be transferred into this section as though it were asked. Complete it after the real presentation.

| Field ID | Required presentation evidence | Entry |
| --- | --- | --- |
| PL-13.01-A | Actual presentation date and time | {{PRESENTATION_ACTUAL_DATE_AND_TIME}} |
| PL-13.01-B | Staff present and number | {{PRESENTATION_STAFF_COUNT_AND_ROLES}} |
| PL-13.01-C | Students present and number | {{PRESENTATION_STUDENT_COUNT}} |
| PL-13.01-D | Other adults present and number | {{PRESENTATION_OTHER_ADULT_COUNT_AND_ROLES}} |
| PL-13.01-E | Notes used | {{SUPERVISOR_PRESENTATION_NOTES_OBSERVATION}} |
| PL-13.01-F | Display items and software used | {{SUPERVISOR_PRESENTATION_MEDIA_OBSERVATION}} |
| PL-13.01-G | Clarity and structure | {{SUPERVISOR_PRESENTATION_CLARITY_STRUCTURE}} |
| PL-13.01-H | Pace and engagement | {{SUPERVISOR_PRESENTATION_PACE_ENGAGEMENT}} |
| PL-13.01-I | Understanding demonstrated | {{SUPERVISOR_PRESENTATION_UNDERSTANDING}} |

<!-- PAIR: PL-13.02 -->
### PL-13.02 Five real questions and answers — supervisor record

| Field ID | Actual question | Candidate's actual answer | Supervisor comment |
| --- | --- | --- | --- |
| PL-13.02-A | {{PRESENTATION_QUESTION_1}} | {{PRESENTATION_ANSWER_1}} | {{PRESENTATION_QA_COMMENT_1}} |
| PL-13.02-B | {{PRESENTATION_QUESTION_2}} | {{PRESENTATION_ANSWER_2}} | {{PRESENTATION_QA_COMMENT_2}} |
| PL-13.02-C | {{PRESENTATION_QUESTION_3}} | {{PRESENTATION_ANSWER_3}} | {{PRESENTATION_QA_COMMENT_3}} |
| PL-13.02-D | {{PRESENTATION_QUESTION_4}} | {{PRESENTATION_ANSWER_4}} | {{PRESENTATION_QA_COMMENT_4}} |
| PL-13.02-E | {{PRESENTATION_QUESTION_5}} | {{PRESENTATION_ANSWER_5}} | {{PRESENTATION_QA_COMMENT_5}} |

<!-- PAIR: PL-13.03 -->
### PL-13.03 Supervisor authentication

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-13.03-A | Supervisor signature | {{PRESENTATION_SUPERVISOR_SIGNATURE_OFFICIAL_FORM_ONLY}} |
| PL-13.03-B | Signature date | {{PRESENTATION_SUPERVISOR_SIGNATURE_DATE}} |
| PL-13.03-C | Supporting presentation file or evidence reference | {{PRESENTATION_EVIDENCE_REFERENCE}} |

---

<!-- PAIR: PL-14.01 -->
## PL-14 Summary and reflection

### PL-14.01 Research and subject learning

Candidate-review draft:

> This project taught me that a comparison depends first on asking a clear question and defining exactly what will be measured. I learned how daily Bitcoin price changes can be used to estimate volatility and why a simple method can sometimes perform very well. I also learned that a complicated method does not automatically have an advantage and that a small difference in a result only matters if the comparison itself is fair.

<!-- PAIR: PL-14.02 -->
### PL-14.02 Method and evidence learning

Candidate-review draft:

> My most important lesson was that a saved and repeatable process can still contain a mistake. Dates may be matched incorrectly, later information may enter an earlier stage or an unfinished day may be included. I therefore learned to check the meaning and timing of the data, repeat the work after corrections and keep the earlier change visible. Saved results, dates and simple checks became part of the evidence rather than background computer work.

<!-- PAIR: PL-14.03 -->
### PL-14.03 Strengths

1. The project developed a focused and answerable question.
2. It compared clear reference methods with two different machine-learning methods.
3. It kept a record of important changes that affected the result.
4. It considered clarity and practicality as well as numerical accuracy.
5. It produced a report, saved data, result tables, checking records and presentation material.

<!-- PAIR: PL-14.04 -->
### PL-14.04 Weaknesses

1. Early project activity was not recorded consistently, so some weeks had to be reconstructed from saved evidence.
2. The project uses daily data and an estimated measure of volatility.
3. It studies one market and a limited group of methods.
4. There was not enough time or data to try every possible setting for the machine-learning methods.
5. Extensive AI assistance means that my own decisions, checks and understanding must be stated especially carefully.

<!-- PAIR: PL-14.05 -->
### PL-14.05 Skills developed

Candidate-review draft:

> I developed skills in narrowing a question, evaluating sources, organising a longer project, checking data quality, comparing results fairly and explaining a cautious conclusion. I also became better at reading computer-generated results critically rather than accepting the first output. Before signing the final log, I will identify the examples that I personally completed and can explain.

| Field ID | Candidate-confirmed skill example | Entry |
| --- | --- | --- |
| PL-14.05-A | Research and source evaluation | {{CANDIDATE_SKILL_EXAMPLE_RESEARCH}} |
| PL-14.05-B | Planning and project management | {{CANDIDATE_SKILL_EXAMPLE_PLANNING}} |
| PL-14.05-C | Mathematical or statistical understanding | {{CANDIDATE_SKILL_EXAMPLE_MATHEMATICS}} |
| PL-14.05-D | Coding, testing or evidence checking | {{CANDIDATE_SKILL_EXAMPLE_CODING_VERIFICATION}} |
| PL-14.05-E | Communication and presentation | {{CANDIDATE_SKILL_EXAMPLE_COMMUNICATION}} |

<!-- PAIR: PL-14.06 -->
### PL-14.06 What I would change

Candidate-review draft:

> If I repeated the project, I would write down the comparison rules before producing results, keep a short activity note after every work session and reserve a final set of data that remained untouched until the end. I would also agree how AI use should be recorded from the start and note exactly which results I checked myself. Only after the main Bitcoin comparison was stable would I consider adding another market or another type of information.

<!-- PAIR: PL-14.07 -->
### PL-14.07 Advice to another candidate

Candidate-review draft:

> Begin with a clear question and a simple comparison. Define what you are measuring before choosing a more advanced method, keep the original evidence and record changes when they happen. If a computer or AI produces an answer, check that you understand the data, dates and meaning of the result before using it in the report.

<!-- PAIR: PL-14.08 -->
### PL-14.08 Presentation reflection and final confirmation

This paragraph must be completed after the real presentation:

{{PRESENTATION_REFLECTION_AFTER_DELIVERY}}

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-14.08-A | How clearly the process and target were explained | {{PRESENTATION_REFLECTION_CLARITY}} |
| PL-14.08-B | How effectively questions were answered | {{PRESENTATION_REFLECTION_QUESTIONS}} |
| PL-14.08-C | What would be changed in a future presentation | {{PRESENTATION_REFLECTION_IMPROVEMENT}} |
| PL-14.08-D | Candidate confirms the complete reflection is personal and accurate | {{FINAL_REFLECTION_CANDIDATE_CONFIRMED}} |
| PL-14.08-E | Final reflection date | {{FINAL_REFLECTION_DATE}} |

---

<!-- PAIR: PL-15.01 -->
## PL-15 Dated milestone log

### PL-15.01 Evidence-based activity record

| Field ID | Date or period | Evidence status | Activity supported by the repository |
| --- | --- | --- | --- |
| PL-15.01-A | 2026-06-13 | Confirmed by Git | Project folders and the first planning structure were created in commit 8aee51f. |
| PL-15.01-C | 2026-06-17 | Confirmed by Git | The question and planning drafts were developed, sources were recorded, the data source changed and the first results were added. |
| PL-15.01-E | 2026-07-09 to 2026-07-10 | Saved files and workspace evidence | Data and results were refreshed and the report and status material were expanded. |
| PL-15.01-F | 2026-07-12 | Earlier saved result | A later check found that the newest daily record had not yet finished and replaced it with a completion-aware refresh. |
| PL-15.01-G | 2026-07-13 | Confirmed by Git | The planned methods were completed, files were reorganised, date matching was corrected and the comparison was expanded. |
| PL-15.01-H | 2026-07-14 | Saved results and workspace evidence | Important calculation and data checks were completed, followed by several repeated comparisons. |
| PL-15.01-J | 2026-07-20 | Final saved data and checking run | The project was refreshed again; one unfinished day was removed, 1,240 complete days were kept and 39 checks passed. |

<!-- PAIR: PL-15.02 -->
### PL-15.02 Candidate activity confirmation

Repository timestamps show when files were created or changed, not who performed each action. The candidate should add only genuine personal activity:

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-15.02-A | Candidate-confirmed activities on major dates | {{CANDIDATE_CONFIRMED_ACTIVITY_NOTES}} |
| PL-15.02-B | Offline research or meetings supported by separate evidence | {{OFFLINE_ACTIVITY_AND_EVIDENCE}} |
| PL-15.02-C | Corrections needed to the reconstructed chronology | {{CANDIDATE_CHRONOLOGY_CORRECTIONS}} |

---

<!-- PAIR: PL-16.01 -->
## PL-16 Evidence register

### PL-16.01 Candidate and process evidence

| Field ID | Evidence | Purpose | Status |
| --- | --- | --- | --- |
| PL-16.01-A | production-log/complete-production-log-en.md, PL-05 to PL-08 | Proposal development | Current consolidated candidate-review source |
| PL-16.01-B | production-log/complete-production-log-en.md, PL-09 | Planning development | Current consolidated candidate-review source |
| PL-16.01-C | production-log/complete-production-log-en.md, PL-10 | Mid-project development | Current consolidated candidate-review source |
| PL-16.01-D | report/final-report.md; PL-11 | Product evaluation | Current report and consolidated review material |
| PL-16.01-E | presentation/final-presentation-script.md; PL-14 | Reflection preparation | Current script and incomplete post-presentation section |
| PL-16.01-F | production-log/weekly-work-log-en.md; zh-cn/weekly-work-log-zh-cn.md | Weekly project development record | Continuing evidence-based record for tutor and candidate review |
| PL-16.01-G | PL-07, PL-09 and PL-10 supervisor placeholders | Feedback evidence | Requires supervisor, date and source confirmation |
| PL-16.01-H | Git commits 8aee51f through ce26fb8 | Process traceability | Historical states remain in Git, not as duplicate current files |
| PL-16.01-I | README.md; appendix/timetable.md | Current scope and milestones | Maintained current-state references |

<!-- PAIR: PL-16.02 -->
### PL-16.02 Research, project and product evidence

| Field ID | Evidence | Purpose | Status |
| --- | --- | --- | --- |
| PL-16.02-A | research/sources.md and literature-notes.md | Reading and critical notes | Candidate should verify reading and understanding |
| PL-16.02-B | research/search-log.md | Search decisions | Dated process evidence |
| PL-16.02-C | research/Source_Evaluation_Tianlin_He.xlsx | Source evaluation | Candidate should verify identity, content and relevance |
| PL-16.02-D | data/raw and data/processed | Original and prepared data | Saved project evidence |
| PL-16.02-E | code folder and test folder | Repeatable comparison work and checks | AI assistance and candidate verification must be disclosed |
| PL-16.02-F | code/outputs/model_run_metadata.json | Dates and overall run record | Main saved run information |
| PL-16.02-G | code/outputs/model_performance.csv and model_predictions.csv | Main numerical result | Saved result after the final run |
| PL-16.02-H | Other files in code/outputs | Extra comparison and checking evidence | Supporting saved results |
| PL-16.02-I | report/final-report.md | Main written product | Final count and wording to be checked |
| PL-16.02-J | presentation materials | Presentation preparation | Delivery evidence still required |

<!-- PAIR: PL-17.01 -->
## PL-17 Completion checklist

### PL-17.01 Candidate actions

| Field ID | Required action | Status |
| --- | --- | --- |
| PL-17.01-A | Confirm every first-person statement and remove anything that does not reflect the candidate's own decisions or understanding | {{COMPLETE_CANDIDATE_REVIEW}} |
| PL-17.01-B | Enter genuine identity, centre, qualifications and dates | {{COMPLETE_IDENTITY_AND_DATES}} |
| PL-17.01-C | Confirm initial ideas from independent memory or evidence rather than the third-party Form | {{COMPLETE_INITIAL_IDEAS_CONFIRMATION}} |
| PL-17.01-D | Finalise a complete AI and assistance disclosure | {{COMPLETE_AI_DISCLOSURE}} |
| PL-17.01-E | Synchronise the final report word count after the report edit | {{FINAL_WORD_COUNT_CONFIRMATION}} |
| PL-17.01-F | Recheck final report body word count against the centre requirement | {{COMPLETE_WORD_COUNT_CHECK}} |
| PL-17.01-G | Complete the real presentation and personal reflection | {{COMPLETE_PRESENTATION_AND_REFLECTION}} |

<!-- PAIR: PL-17.02 -->
### PL-17.02 Authorised-person actions

| Field ID | Required action | Status |
| --- | --- | --- |
| PL-17.02-A | Supervisor completes declarations, taught skills, comments, authentication and marks | {{COMPLETE_SUPERVISOR_SECTIONS}} |
| PL-17.02-B | Centre coordinator completes approval and any recommendations | {{COMPLETE_COORDINATOR_SECTIONS}} |
| PL-17.02-C | Supervisor records the real presentation audience, delivery and five Q&As | {{COMPLETE_PRESENTATION_PART_B}} |
| PL-17.02-D | Candidate and authorised people sign and date the centre-issued form | {{COMPLETE_OFFICIAL_SIGNATURES}} |

<!-- PAIR: PL-17.03 -->
### PL-17.03 Final submission control

| Field ID | Control | Entry |
| --- | --- | --- |
| PL-17.03-A | Correct blank/current centre-issued form obtained | {{OFFICIAL_FORM_OBTAINED}} |
| PL-17.03-B | Third-party Form excluded from submission | {{THIRD_PARTY_FORM_EXCLUDED}} |
| PL-17.03-C | Undated initial-ideas PDF either authenticated or excluded | {{INITIAL_IDEAS_PDF_DECISION}} |
| PL-17.03-D | English and Chinese versions checked for 1:1 structure | {{BILINGUAL_PARITY_CHECKED}} |
| PL-17.03-E | Candidate approves final English wording | {{CANDIDATE_FINAL_ENGLISH_APPROVAL}} |
| PL-17.03-F | Submission package checked by supervisor | {{SUPERVISOR_FINAL_PACKAGE_CHECK}} |
