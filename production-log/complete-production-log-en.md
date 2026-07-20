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

> I selected Bitcoin volatility forecasting because it allowed me to combine mathematics, statistics, computing and an applied financial problem. Volatility is relevant to risk, the result can be evaluated quantitatively, and historical market data can support a reproducible product. The project was also suitable for critical evaluation because a more complex forecasting model would not necessarily be more accurate, interpretable or practical. Before this wording is used, I will confirm that it reflects my actual initial reasoning rather than only the later direction of the repository.

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-05.03-A | Real preliminary sources consulted | {{INITIAL_RESEARCH_SOURCES_AND_DATES}} |
| PL-05.03-B | Actual initial supervisor comments | {{INITIAL_SUPERVISOR_COMMENTS}} |
| PL-05.03-C | Modifications made after the initial meeting | {{INITIAL_MEETING_MODIFICATIONS}} |
| PL-05.03-D | Initial-meeting date | {{INITIAL_MEETING_DATE}} |

<!-- PAIR: PL-05.04 -->
### PL-05.04 Proposed title, aim and objectives

**Proposed title recorded in the first tracked proposal:**
To what extent can machine learning models improve Bitcoin volatility forecasting compared with traditional statistical models?

**Proposed aim:**
To critically evaluate the predictive power, interpretability, computational practicality and practical limitations of machine-learning approaches compared with traditional statistical approaches in Bitcoin volatility forecasting.

**Proposed objectives:**

1. Research logarithmic returns, realised volatility and GARCH-type models.
2. Collect daily Bitcoin price data and construct a realised-volatility target.
3. Implement rolling historical volatility and GARCH(1,1) as statistical benchmarks.
4. Implement Random Forest and, if feasible, an LSTM.
5. compare forecasts using MAE, MSE and RMSE.
6. Decide whether any accuracy improvement is meaningful after interpretability, computational complexity and project scale are considered.

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-05.04-A | Candidate confirms that this reflects the actual initial proposal | {{INITIAL_PROPOSAL_CANDIDATE_CONFIRMED}} |
| PL-05.04-B | Date entered on the candidate's official record | {{INITIAL_PROPOSAL_DATE}} |

---

<!-- PAIR: PL-06.01 -->
## PL-06 Part A: Candidate proposal

### PL-06.01 Working title and focus

**Working title:**
To what extent can machine learning models improve Bitcoin volatility forecasting compared with traditional statistical models?

**Focused research question developed from it:**
How do Random Forest and Long Short-Term Memory networks compare with rolling historical volatility and GARCH(1,1) when forecasting Bitcoin volatility, in terms of accuracy, interpretability, computational practicality and robustness?

<!-- PAIR: PL-06.02 -->
### PL-06.02 Initial resources

Candidate-review draft:

> At the proposal stage I planned to use daily BTC price data, Python for data processing and modelling, academic literature on volatility forecasting and machine learning, a source-evaluation workbook, saved code and outputs, and a chronological evaluation design. The first tracked proposal named Yahoo Finance; the project changed to Hyperliquid exchange-level BTC perpetual-futures candles later in the documented process. I will keep that change visible rather than rewriting the original proposal as though Hyperliquid had always been selected.

| Field ID | Resource category | Planned resource |
| --- | --- | --- |
| PL-06.02-A | Market data | Daily BTC data; the first tracked plan named Yahoo Finance |
| PL-06.02-B | Statistical theory | Log returns, realised volatility and GARCH literature |
| PL-06.02-C | Machine learning | Random Forest and LSTM literature |
| PL-06.02-D | Evaluation | MAE, MSE, RMSE and chronological train/test separation |
| PL-06.02-E | Tools | Python or notebook environment, source-evaluation workbook, scripts, output tables and charts |
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
To critically evaluate whether the additional complexity of machine-learning approaches is justified when compared with transparent statistical approaches to Bitcoin volatility forecasting.

**Objectives at this stage:**

1. Explain the mathematical foundations of returns and volatility.
2. Build a reproducible daily BTC dataset and realised-volatility target.
3. Implement rolling historical volatility and GARCH(1,1).
4. Implement Random Forest and attempt a small LSTM after the baseline workflow is stable.
5. Preserve chronological order and evaluate MAE, MSE and RMSE.
6. Evaluate accuracy, interpretability, computational practicality and limitations.

The later addition of lagged linear regression, alternative target windows, test segments, expanding-window folds, volatility regimes, bootstrap uncertainty, Random Forest diagnostics and multi-seed LSTM checks belongs in later reviews, not in this original proposal section.

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

> I narrowed the project from a broad cryptocurrency-prediction idea to a focused comparison of Bitcoin volatility forecasts. I planned to establish transparent benchmarks before implementing machine learning, preserve chronological order, save raw and processed data, and export tables and charts rather than rely on screenshots. I also widened the evaluation from accuracy alone to interpretability, computational practicality and usefulness because a lower error would not automatically justify a more opaque model.

| Field ID | Planned stage | Original target | Resource or evidence |
| --- | --- | --- | --- |
| PL-09.01-A | Refine question, aims and objectives | 2026-06-17 | Candidate proposal, report outline and supervisor-feedback summary |
| PL-09.01-B | Collect and evaluate sources | 2026-06-18 | Research notes, search log and source-evaluation workbook |
| PL-09.01-C | Complete planning review | 2026-06-19 | Planning-review draft |
| PL-09.01-D | Download and clean BTC data | 2026-06-22 | Raw archive, processed dataset and data notes |
| PL-09.01-E | Implement rolling volatility and GARCH | 2026-06-25 | Python pipeline and outputs |
| PL-09.01-F | Implement Random Forest and first LSTM prototype | 2026-06-30 | Python pipeline, model settings and outputs |
| PL-09.01-G | Compare models | 2026-07-03 | MAE, MSE, RMSE and forecast chart |
| PL-09.01-H | Complete mid-project review | 2026-07-05 | Mid-project review draft |
| PL-09.01-I | Draft report | 2026-07-20 | Section drafts and consolidated report |
| PL-09.01-J | Prepare presentation and final reflection | 2026-07-31 | Slide material, script, Q&A preparation and final reflection |

These are documented target dates, not proof that a review or task occurred on each date.

<!-- PAIR: PL-09.02 -->
### PL-09.02 Reasons for decisions

| Field ID | Decision | Reason |
| --- | --- | --- |
| PL-09.02-A | Focus on Bitcoin rather than several cryptocurrencies | Depth was more feasible than a shallow multi-asset comparison within the project scale. |
| PL-09.02-B | Use rolling volatility and GARCH as benchmarks | Rolling volatility gives a transparent minimum benchmark; GARCH explicitly models volatility clustering. |
| PL-09.02-C | Use Random Forest and LSTM as the main machine-learning comparison | The two models test nonlinear lag relationships and sequential learning without adding many unrelated model families. |
| PL-09.02-D | Preserve chronological order | Random shuffling would allow later market information to influence an earlier forecast evaluation. |
| PL-09.02-E | Change the planned data source to Hyperliquid | The project moved to a specific exchange-level BTC perpetual-futures market rather than an aggregated finance site. |
| PL-09.02-F | Compare more than accuracy | Interpretability, measured runtime, structural complexity and robustness affect whether extra complexity is worthwhile. |

<!-- PAIR: PL-09.03 -->
### PL-09.03 Supervisor advice and response

The repository contains a candidate-side summary suggesting that the comparison should not be a simple ranking by MAE or RMSE and should define comparative analysis more clearly. It is not an authenticated supervisor quotation.

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-09.03-A | Actual supervisor advice, quotation or approved paraphrase | {{PLANNING_SUPERVISOR_ADVICE_APPROVED}} |
| PL-09.03-B | Date and medium of the advice | {{PLANNING_SUPERVISOR_ADVICE_DATE_AND_MEDIUM}} |
| PL-09.03-C | Candidate response | I expanded the planned comparison to include model-specific interpretability evidence, measured local runtime, structural scale, reproducibility and robustness. Candidate confirmation: {{PLANNING_RESPONSE_CONFIRMED}} |
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

The timetable recorded 2026-07-05 as a target for this review, but the repository does not prove that a formal supervisor review occurred on that date. The official date remains {{MID_REVIEW_DATE}}.

Candidate-review draft:

> The project broadly followed the planned topic but developed in important ways. Bitcoin remained the core asset, while Ethereum was dropped so that the main comparison could be deeper. Hyperliquid replaced the initially planned Yahoo Finance source. The first modelling workflow established rolling volatility, GARCH and feature-based models, and lagged linear regression was added as a transparent check on whether engineered features required a nonlinear model. The evaluation remained chronological. I also recognised that daily rolling volatility is an overlapping proxy for latent volatility and that this limits how widely the findings can be generalised.

<!-- PAIR: PL-10.02 -->
### PL-10.02 Problems identified

| Field ID | Problem | Response planned at the mid-project stage |
| --- | --- | --- |
| PL-10.02-A | Daily realised volatility is a proxy rather than directly observed latent volatility | Define the target precisely and state the limitation throughout the report. |
| PL-10.02-B | The rolling target overlaps strongly across days | Preserve time order and avoid treating observations as independent. |
| PL-10.02-C | The dataset is small for deep learning | Keep the LSTM modest, use chronological validation and report architecture and training evidence. |
| PL-10.02-D | Machine-learning models are harder to explain | Export model-specific evidence and avoid claiming that complexity itself is useful. |
| PL-10.02-E | Early outputs could contain implementation errors | Audit alignment, scaling, target construction and forecast dates before treating rankings as final. |
| PL-10.02-F | Project administration was not recorded consistently while work was happening | Use Git, saved outputs and dated files to build an evidence-based weekly chronology, leaving gaps explicit. |

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
To evaluate whether the additional complexity of Random Forest and LSTM is justified when compared with transparent statistical approaches to Bitcoin volatility forecasting.

**Revised objectives:**

1. Define log returns and rolling realised-volatility targets.
2. Collect and quality-check daily Hyperliquid BTC perpetual-futures candles.
3. Implement rolling historical volatility, GARCH(1,1), lagged linear regression, Random Forest and LSTM.
4. Use chronological validation and common MAE, MSE and RMSE metrics.
5. Compare interpretation evidence, measured runtime, structural complexity and reproducibility.
6. Audit temporal alignment, scaling and target construction.
7. Test whether the conclusion remains stable under alternative windows and later robustness checks.
8. Give a bounded conclusion for this dataset and implementation.

<!-- PAIR: PL-10.05 -->
### PL-10.05 Planned next steps

1. Complete the LSTM and verify that validation and scaling use training-period information only.
2. Audit GARCH forecast alignment and the rolling-target conversion.
3. Rerun the complete model set after each material correction.
4. Add at least one alternative volatility window.
5. Expand the literature review, methodology, results, discussion and conclusion.
6. Prepare presentation materials and record genuine Q&A after delivery.

| Field ID | Required information | Entry |
| --- | --- | --- |
| PL-10.05-A | Candidate confirms these were genuine next steps at the review date | {{MID_NEXT_STEPS_CONFIRMED}} |
| PL-10.05-B | Mid-project review signature/date entry | {{MID_REVIEW_SIGNATURE_AND_DATE_OFFICIAL_FORM_ONLY}} |

---

<!-- PAIR: PL-11.01 -->
## PL-11 Project product review

### PL-11.01 Product and adherence to the revised plan

Candidate-review draft:

> The product is a research report supported by a reproducible Python pipeline, archived market data, processed features and targets, model predictions, comparison tables, robustness outputs, a native chart, source evaluation and presentation preparation. The project followed the revised topic and comparison logic, but the methodology became stricter after several audits. Those changes are part of the product's development rather than being hidden from the record.

| Field ID | Current product item | Evidence or status |
| --- | --- | --- |
| PL-11.01-A | English research report | report/final-report.md; current body count: 5,356 |
| PL-11.01-B | Reproducible code and tests | code/epq_pipeline, code/tests and run scripts; current passing-test count: 39 |
| PL-11.01-C | Market data and quality record | Completed daily Hyperliquid candles and quality JSON; current retained rows: 1,240 |
| PL-11.01-D | Model evidence | Predictions, metrics, parameters, timing, complexity and diagnostic outputs |
| PL-11.01-E | Research evidence | Source list, literature notes, search log and source-evaluation workbook |
| PL-11.01-F | Presentation preparation | Slide outline, full script and Q&A preparation; final delivered slide file: {{FINAL_PRESENTATION_FILE}} |

<!-- PAIR: PL-11.02 -->
### PL-11.02 Major development and audit trail

| Field ID | Development | Effect on the project |
| --- | --- | --- |
| PL-11.02-A | Data source changed from Yahoo Finance to Hyperliquid | Defined one exchange-level BTC perpetual-futures market and made the market scope more precise. |
| PL-11.02-B | Lagged linear regression added | Tested whether engineered lag information needed a nonlinear model. |
| PL-11.02-C | LSTM implemented and code refactored into a package | Completed the planned sequential-model comparison and improved reproducibility. |
| PL-11.02-D | GARCH predictions mapped by date rather than reset row number | Removed a forecast-to-target alignment risk. |
| PL-11.02-E | GARCH likelihood update order corrected | Prevented the current shock from entering its own conditional variance. |
| PL-11.02-F | Rolling sample-variance expectation corrected | Accounted for the uncertain next return changing both the sum of squares and the sample mean. |
| PL-11.02-G | LSTM scaler limited to the fitting portion | Removed validation-period information from scaling estimates. |
| PL-11.02-H | Still-open daily candle excluded | Prevented a partial close and partial activity measures from entering the dataset. |
| PL-11.02-I | Robustness and diagnostics expanded | Added target-window, segment, expanding-window, regime, bootstrap, OOB, permutation and multi-seed evidence. |

The candidate must describe personal involvement accurately. Replace any unsupported “I coded” or “I corrected” wording with a truthful account of what was done with AI assistance and what the candidate personally reviewed or tested.

<!-- PAIR: PL-11.03 -->
### PL-11.03 Current 2026-07-20 evidence snapshot

The values below come from the final 2026-07-20 data refresh and model run. The run metadata was generated at 2026-07-20T06:14:33+00:00.

| Field ID | Measure | Current value |
| --- | --- | --- |
| PL-11.03-A | Refresh date | 2026-07-20 |
| PL-11.03-B | Fetch timestamp UTC | 2026-07-20T06:12:26+00:00 |
| PL-11.03-C | API rows returned | 1,241 |
| PL-11.03-D | Incomplete rows excluded | 1 |
| PL-11.03-E | Completed candle rows retained | 1,240 |
| PL-11.03-F | Last completed candle date | 2026-07-19 |
| PL-11.03-G | Modelling-frame rows | 1,195 |
| PL-11.03-H | Training rows | 950 |
| PL-11.03-I | Test rows | 245 |
| PL-11.03-J | GARCH 30-day RMSE | 0.00098502 |
| PL-11.03-K | Lagged linear 30-day RMSE | 0.00140087 |
| PL-11.03-L | Rolling 30-day RMSE | 0.00142744 |
| PL-11.03-M | LSTM 30-day RMSE | 0.00174351 |
| PL-11.03-N | Random Forest 30-day RMSE | 0.00232370 |
| PL-11.03-O | GARCH expanding-window RMSE | 0.00098681 |
| PL-11.03-P | GARCH bootstrap interval versus rolling | [-0.00099670, -0.00017158] |
| PL-11.03-Q | Passing tests | 39 |

<!-- PAIR: PL-11.04 -->
### PL-11.04 Successes and strengths

1. The same explicit target and chronological test logic are used across the five primary comparators.
2. Saved outputs support numerical claims and preserve forecast-origin and target dates.
3. The audit trail records material corrections instead of silently retaining an invalid early ranking.
4. Robustness evidence tests whether the conclusion depends on one window, one test segment, one volatility regime or one LSTM seed.
5. The final conclusion is bounded to the selected market, period, target and implementations.

<!-- PAIR: PL-11.05 -->
### PL-11.05 Failures, limitations and lessons

1. Daily realised volatility is a proxy and does not use intraday realised variance.
2. Overlapping rolling targets create strong persistence and dependent errors.
3. The Random Forest is a lightweight local implementation rather than an extensively tuned library benchmark.
4. The LSTM is deliberately small and the dataset is limited for deep learning.
5. One BTC perpetual-futures market cannot establish universal model superiority.
6. Four expanding-window blocks remain parts of one history, not independent external datasets.
7. Early administration was weaker than the later technical audit; many days lack direct process records.
8. AI-supported implementation and drafting require precise disclosure and candidate verification.

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

1. How the question narrowed from a broad machine-learning comparison to Bitcoin volatility forecasting.
2. Why the data source changed to Hyperliquid BTC perpetual-futures candles.
3. How log returns and rolling realised-volatility targets were constructed.
4. Why a chronological holdout and expanding-window checks were used.
5. How date alignment, likelihood order, sample-variance conversion, scaling and incomplete-candle audits improved the evidence.
6. How source evaluation, code outputs and limitations informed the final judgment.

<!-- PAIR: PL-12.03 -->
### PL-12.03 Planned findings and conclusion

The presentation will insert the final synchronised values:

| Field ID | Finding | Value |
| --- | --- | --- |
| PL-12.03-A | Best primary 30-day RMSE model | GARCH(1,1) |
| PL-12.03-B | GARCH primary RMSE | 0.00098502 |
| PL-12.03-C | Rolling benchmark RMSE | 0.00142744 |
| PL-12.03-D | Alternative-window conclusion | GARCH ranks first for the 14-day target with RMSE 0.00178208, 35.482% below rolling. |
| PL-12.03-E | Expanding-window conclusion | GARCH ranks first overall with RMSE 0.00098681 and ranks first in each of the four chronological folds. |
| PL-12.03-F | Machine-learning conclusion | Neither machine-learning model beats rolling: LSTM ranks fourth and Random Forest fifth on primary RMSE. |

The intended conclusion is bounded: the tested machine-learning models do not justify their additional complexity under this daily-data design; this is not a claim about every Bitcoin market or every machine-learning method.

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

> This project taught me that the quality of a forecast comparison depends first on the definition of the question and target. I learned to distinguish latent volatility from an observable rolling proxy, to calculate log returns, and to understand why volatility clustering motivates GARCH. I also learned that a persistent target can make simple models strong. A complicated model does not begin with an automatic advantage, and a small numerical difference is not meaningful unless the validation design and uncertainty support it.

<!-- PAIR: PL-14.02 -->
### PL-14.02 Method and evidence learning

Candidate-review draft:

> My most important methodological lesson was that reproducible code can still be conceptually wrong. Saving a script is not enough if a prediction is aligned to the wrong date, if the current shock leaks into its own conditional variance, if a sample-variance conversion ignores the moving sample mean, if validation information influences scaling, or if an unfinished candle enters the data. The audit changed the strength of the evidence and made me more cautious about accepting the first output. I learned to use explicit dates, failure checks, unit tests, metadata and saved predictions as part of the argument rather than treating code as a hidden calculation.

<!-- PAIR: PL-14.03 -->
### PL-14.03 Strengths

1. The project developed a focused and answerable research question.
2. It compared transparent baselines with two different machine-learning approaches.
3. It retained an audit trail and reported method changes that affected the result.
4. It combined numerical accuracy with interpretability, practicality and robustness.
5. It produced reusable code, datasets, tables, diagnostics and presentation preparation rather than only a narrative report.

<!-- PAIR: PL-14.04 -->
### PL-14.04 Weaknesses

1. Early project administration was not recorded consistently, so some process history is reconstructed from Git and generated files.
2. The target is based on daily data and overlapping rolling windows rather than intraday realised variance.
3. The project studies one market and a modest set of implementations.
4. Machine-learning tuning is limited, particularly for the LSTM.
5. Extensive AI assistance means that the candidate must be especially precise about personal decisions, verification and understanding.

<!-- PAIR: PL-14.05 -->
### PL-14.05 Skills developed

Candidate-review draft:

> I developed skills in narrowing a research question, evaluating sources, designing chronological validation, interpreting statistical and machine-learning models, checking data quality, reading generated evidence critically, organising a repository and communicating a bounded conclusion. I also improved my understanding of why model comparison must separate predictive accuracy from interpretability and computational cost. I will identify which of these skills I personally demonstrated and provide examples before signing the final log.

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

> If I repeated the project, I would write the evaluation protocol before fitting models, keep a contemporaneous activity log from the first day, preserve an untouched future test period, use higher-frequency data to estimate realised variance, and specify model-tuning limits in advance. I would also agree an AI-use record with the supervisor at the start and record which outputs I personally checked. Only after the core BTC workflow was stable would I add another exchange, asset or richer information such as sentiment.

<!-- PAIR: PL-14.07 -->
### PL-14.07 Advice to another candidate

Candidate-review draft:

> Start with a strong baseline, define the target before choosing an advanced model, keep raw evidence, separate forecast-origin and target dates, and let the result contradict the original expectation. Record changes when they happen rather than reconstructing them later. Treat an AI-generated or software-generated output as something to verify and explain, not as evidence of understanding by itself.

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
| PL-15.01-A | 2026-06-13 | Git-verified | Project structure and initial folders were created in commit 8aee51f. |
| PL-15.01-B | 2026-06-14 to 2026-06-16 | No direct repository evidence | No separate dated activity is claimed for this interval. |
| PL-15.01-C | 2026-06-17 | Git-verified | The question and production-log drafts were developed, sources were recorded, the planned data source changed to Hyperliquid, and first model outputs were added in commits 155ce90, 595d119 and b4a3cf6. |
| PL-15.01-D | 2026-06-18 to 2026-07-08 | Sparse evidence | The timetable contains targets, but it does not prove completion on those dates. No detailed daily activity is reconstructed. |
| PL-15.01-E | 2026-07-09 to 2026-07-10 | Generated metadata and workspace evidence | Data and outputs were refreshed and report/status materials were expanded. These entries are supported by saved files rather than a dedicated Git commit. |
| PL-15.01-F | 2026-07-12 | Superseded generated output | A refresh included a daily candle that a later audit identified as still open at fetch time; the completion-aware fetch replaced it. |
| PL-15.01-G | 2026-07-13 | Git-verified | LSTM implementation, package refactoring, date-alignment correction and expanded evaluation were recorded in commits f7d20bf, f0ab18a, af458e7 and 8c98f36. |
| PL-15.01-H | 2026-07-14 | Generated outputs and workspace evidence | Likelihood order, rolling-target conversion, scaler scope and completed-candle handling were audited; data-quality, expanding-window, regime, bootstrap, OOB, permutation and multi-seed evidence was generated. |
| PL-15.01-I | 2026-07-15 to 2026-07-19 | No separate direct evidence preserved | No specific activity is asserted for this interval. |
| PL-15.01-J | 2026-07-20 | Final generated metadata and test run | The data and complete pipeline were refreshed again. The API returned 1,241 rows; one incomplete row was excluded; 1,240 completed candles were retained through 2026-07-19; 39 tests passed. |

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
### PL-16.02 Research, technical and product evidence

| Field ID | Evidence | Purpose | Status |
| --- | --- | --- | --- |
| PL-16.02-A | research/sources.md and literature-notes.md | Academic evidence and critical notes | Candidate should verify reading and understanding |
| PL-16.02-B | research/search-log.md | Search decisions | Dated process evidence |
| PL-16.02-C | research/Source_Evaluation_Tianlin_He.xlsx | Source evaluation | Candidate should verify identity, content and submission relevance |
| PL-16.02-D | data/raw and data/processed | Archived data and target construction | Generated evidence |
| PL-16.02-E | code/epq_pipeline and code/tests | Reproducible implementation and tests | AI assistance and candidate verification must be disclosed |
| PL-16.02-F | code/outputs/model_run_metadata.json | Run design, sample and timestamps | Canonical generated run metadata |
| PL-16.02-G | code/outputs/model_performance.csv and model_predictions.csv | Primary numerical result | Canonical generated output after final run |
| PL-16.02-H | code/outputs robustness and diagnostic files | Robustness, uncertainty and model diagnostics | Supporting generated outputs |
| PL-16.02-I | report/final-report.md | Main written product | Final count and wording to be synchronised |
| PL-16.02-J | presentation materials | Presentation preparation | Delivery evidence still required |

---

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
