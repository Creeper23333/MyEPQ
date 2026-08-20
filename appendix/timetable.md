# Detailed EPQ Timetable

Updated status note: 2026-08-20

This table distinguishes the original or revised plan from what the repository
can currently evidence. A target date is not treated as proof of completion on
that date.

| Phase | Planned window | What was planned | Why this stage was needed | Current status and evidence |
| ---: | --- | --- | --- | --- |
| 1 | 13-17 Jun | Define the topic, asset, forecast target and comparison question | A narrow question was needed before sources or models could be chosen fairly | Completed; initial repository structure and proposal history in Git and PL-05/PL-06 |
| 2 | 17-18 Jun | Search for and evaluate volatility, GARCH, RF and LSTM sources | The method choices and limitations required an academic basis | Completed; `research/sources.md`, literature notes, search log and source-evaluation files |
| 3 | 17-19 Jun | Write the proposal, aims, objectives, initial resources and planning review | The project needed an examiner-visible plan and a reason for each decision | Completed as a candidate-review draft; PL-05 to PL-09, with authentic supervisor fields still outstanding |
| 4 | 17-22 Jun | Download, retain and check daily Bitcoin data | All methods needed one traceable market and a common chronological dataset | Completed and later strengthened; raw/processed data, metadata and quality report |
| 5 | 22-25 Jun | Implement rolling historical volatility and GARCH(1,1) | Clear statistical benchmarks were needed before judging extra complexity | Completed and audited; model code, GARCH parameters and dated predictions |
| 6 | 25-30 Jun | Implement lagged linear regression, Random Forest and LSTM | These methods test linear features, nonlinear tabular relationships and sequence learning | Completed; standard RF and compact LSTM pipelines with training-only selection |
| 7 | 1-3 Jul | Produce the first common-period comparison and forecast chart | A shared holdout and common metrics were needed for a fair first ranking | Completed, then superseded by corrected audited outputs |
| 8 | 5 Jul | Complete the mid-project review and revise the next steps | Problems, scope changes and remaining work needed to be recorded before finalisation | Candidate-review draft completed in PL-10; real review date and supervisor wording require confirmation |
| 9 | 9-14 Jul | Refresh the data, inspect dates and audit the model calculations | The report could not rely on outputs until alignment, leakage and incomplete-candle risks were checked | Completed; date mapping, recursion, target conversion and data-quality tests added |
| 10 | 20 Jul | Freeze the cutoff, perform the final completed-candle refresh and rerun robustness checks | A stable test start allows new days to extend rather than redefine the experiment | Completed; 1,240 completed candles, 950 training rows and 245 test rows |
| 11 | 4-20 Jul | Draft and consolidate the report, appendices and bilingual material | Results needed to become a coherent research argument rather than a table of scores | Completed and later revised; final English/Chinese reports and evidence summaries |
| 12 | 25-26 Jul | Revise the question and method; add QLIKE and strengthen the fairness, explanation and practicality checks | The conclusion needed to match the exact target and the methods that were actually tested | Completed; 43 tests and the final method revision in PL-11.07 |
| 13 | 6 Aug | Complete the six-item Appendix checklist and audit Production Log WHAT/WHY coverage | The examiner needs a navigable plan, structure, source, risk and result record | Completed as a candidate-review package; Appendix pack and PL-11.08 |
| 14 | 26 Jul-31 Aug | Finalise slides, rehearse, present, record real questions and complete the official form | Presentation and authenticated form evidence can only be completed by the relevant people | In progress; script and Q&A preparation exist, but delivery, signatures and supervisor-only sections remain outstanding |
| 15 | 20 Aug | Refresh the completed-candle archive and rerun the unchanged frozen-cutoff comparison | New market movement can extend the holdout without redefining training or selecting on observed test results | Completed; 1,272 rows returned, one open 20 Aug row excluded, 1,271 completed candles through 19 Aug, 950 training rows and 276 test rows; GARCH remained first overall |

## Gantt Chart

The chart visualises the recorded plan and revision periods. It is a planning
aid, not independent authentication of every completion date.

![EPQ Gantt chart](gantt-chart.svg)
