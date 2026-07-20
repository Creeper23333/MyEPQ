# EPQ Timetable

Updated status note: 2026-07-20

| Stage | Task | Target date | Evidence |
| --- | --- | --- | --- |
| 1 | Record and refine the initial project direction | Completed | Git history beginning at commit `8aee51f`; current scope in `README.md` |
| 2 | Refine research question and aims/objectives | 2026-06-17 | `README.md`, `report/final-report.md` |
| 3 | Complete candidate proposal material | 2026-06-17 | `production-log/complete-production-log-en.md`, section PL-05 |
| 4 | Record feedback and planned responses | Candidate confirmation still required | `production-log/complete-production-log-en.md`, sections PL-05 to PL-07 |
| 5 | Collect and evaluate initial sources | 2026-06-18 | `research/sources.md`, `research/literature-notes.md`, source evaluation workbook |
| 6 | Complete planning review material | 2026-06-19 | `production-log/complete-production-log-en.md`, section PL-06 |
| 7 | Download and clean Bitcoin price data | Completed and refreshed on 2026-07-14 Beijing time; incomplete candle excluded and quality gate passed | `data/raw/`, `data/processed/`, `data/raw/hyperliquid_BTC_1d_quality_report.json`, `appendix/hyperliquid-data-source-notes.md` |
| 8 | Implement rolling volatility and GARCH(1,1) | Completed first pass and refreshed | `code/run_volatility_models.py`, `code/outputs/model_performance.csv`, `code/outputs/garch_parameters.json` |
| 9 | Implement Random Forest and first LSTM prototype | RF and LSTM completed in first-pass form with packaged pipeline structure | `code/epq_pipeline/`, `code/outputs/random_forest_feature_importance.csv`, `code/outputs/lstm_training_summary.json`, `code/outputs/lstm_training_history.csv` |
| 10 | Compare accuracy, interpretability, computational practicality, and robustness | Completed and corrected after method audit; target-window, segment, four-fold expanding-window, volatility-regime, block-bootstrap, RF diagnostic and LSTM multi-seed checks added | `code/outputs/model_performance.csv`, `code/outputs/model_multidimensional_comparison.csv`, `code/outputs/model_walk_forward_performance.csv`, `code/outputs/model_performance_by_volatility_regime.csv`, `code/outputs/model_rmse_block_bootstrap.csv`, `code/outputs/random_forest_oob_summary.json`, `code/outputs/lstm_seed_stability.csv` |
| 11 | Complete mid-project review material | 2026-07-05 | `production-log/complete-production-log-en.md`, section PL-07 |
| 12 | Write introduction, literature review, mathematical formulation, and methodology | Completed and consolidated | `report/final-report.md` |
| 13 | Complete results, comparative analysis, and conclusion | Canonical final report completed | `report/final-report.md`, `zh-cn/final-report-zh-cn.md` |
| 14 | Prepare presentation and production-log evidence | Current script, slide specification, Q&A notes, bilingual logs, and weekly records completed; actual delivery and the candidate's centre-controlled form remain candidate tasks | `presentation/`, `production-log/complete-production-log-en.md`, `zh-cn/complete-production-log-zh-cn.md` |
