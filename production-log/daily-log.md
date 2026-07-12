# Daily Project Log

This file is an evidence-based retrospective reconstruction of project activity by day. It uses repository commits, dated drafts, generated outputs, and the refreshed work completed through 2026-07-13. Dates without direct repository evidence are marked clearly rather than filled with invented detail.

| Date | Evidence status | Summary |
| --- | --- | --- |
| 2026-06-13 | Verified by repository commit and file set | Project structure created; initial EPQ folders, README, and production-log base materials were added. Git evidence: `8aee51f Set up EPQ project structure`. |
| 2026-06-14 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. Any reading or planning done offline is not reconstructable from the repository alone. |
| 2026-06-15 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-06-16 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-06-17 | Verified by commits, dated drafts, and generated outputs | Major project-development day. Research question refined, supervisor-comment response drafted, Hyperliquid adopted as data source, search log populated, planning and mid-project materials drafted, first model outputs generated, and commits `155ce90`, `595d119`, and `b4a3cf6` recorded. |
| 2026-06-18 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. The repository does not preserve enough evidence to claim specific work items. |
| 2026-06-19 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-06-20 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-06-21 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-06-22 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-06-23 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-06-24 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-06-25 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-06-26 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-06-27 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-06-28 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-06-29 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-06-30 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-07-01 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-07-02 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-07-03 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-07-04 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-07-05 | Indirect evidence via milestone target | `production-log/mid-project-review-draft.md` names this as the target date for the mid-project review draft, but there is no separate commit on this date. |
| 2026-07-06 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-07-07 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-07-08 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-07-09 | Verified by refreshed data and generated-output timestamps | Hyperliquid data refresh completed in UTC on 2026-07-09/2026-07-10 boundary, producing updated raw data, processed volatility data, metadata, and new model outputs. The refreshed dataset included the latest available daily candle dated 2026-07-09. |
| 2026-07-10 | Verified by current workspace changes | Repository close-out work completed: refreshed model outputs checked, project status reassessed, timetable and README updated, report drafts expanded, and this daily log created to keep future production-log updates precise by date. |
| 2026-07-11 | No direct repository evidence preserved | No separate dated commit or markdown update survives for this date. |
| 2026-07-12 | Verified by refreshed data and generated-output timestamps | Hyperliquid data refresh completed in UTC on 2026-07-12/2026-07-13 boundary, producing updated raw data, processed volatility data, metadata, and new model outputs. The refreshed dataset includes the latest available daily candle dated 2026-07-12. |
| 2026-07-13 | Verified by commits, tests, and generated outputs | The PyTorch LSTM was implemented and the code was refactored into the packaged `code/epq_pipeline` architecture. A later method audit corrected GARCH forecast extraction from reset row indexing to strict date alignment, added failure checks and unit tests, and changed the valid 30-day GARCH RMSE to `0.00099637`. The full model set was rerun for 14-day and 30-day targets; GARCH ranked first at both. New evidence exports record model timing, structural complexity, interpretation limitations, reproducibility, risk-use commentary, and robustness. Research question, aims/objectives, report drafts, appendix, presentation notes, README files, timetable, and production-log materials were updated to match the corrected evidence. |

## Git Record Note

Before this latest architecture clean-up was committed, the repository already contained the following dated commits:

1. `8aee51f` on 2026-06-13
2. `155ce90` on 2026-06-17
3. `595d119` on 2026-06-17
4. `b4a3cf6` on 2026-06-17
5. `f7d20bf` on 2026-07-13
6. `f0ab18a` on 2026-07-13
7. `af458e7` on 2026-07-13

This daily log is designed to complement Git, not falsify it. Future work should continue to be committed on the real day it is completed so the Git history and production log stay aligned.
