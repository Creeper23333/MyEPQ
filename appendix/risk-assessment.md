# Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Project scope becomes too broad | Medium | High | Focus mainly on Bitcoin; keep Ethereum as optional extension |
| Machine learning model is too complex to explain clearly | Medium | Medium | Evaluate interpretability separately from accuracy and explain why the LSTM architecture was kept deliberately small |
| Data source changes or becomes unavailable | Low | Medium | Save raw data locally and record source details |
| Results do not show machine learning improvement | Medium | Low | Treat this as a valid finding and evaluate why simpler models may be sufficient |
| Time pressure near deadline | Medium | High | Set staged deadlines and keep appendices updated during the project |
| Daily process notes fall behind the actual work | Medium | Medium | Maintain an evidence-based daily log and update the production log on the same day as major changes |
| Accidental plagiarism or weak referencing | Low | High | Record sources immediately and write literature notes in original wording |
| Random train-test split gives misleading results | Medium | High | Use a fixed chronological primary holdout plus clearly separated expanding-window rolling-origin checks; never shuffle time rows |
| Forecast rows become misaligned after feature rows are dropped | Low after mitigation | High | Align model forecasts to test observations by date and fail the run when dates are missing or duplicated |
| An unfinished daily candle enters the dataset | Low after mitigation | High | Retain a candle only when its API end timestamp is strictly earlier than the fetch time; record excluded-row count in metadata |
| Malformed, duplicated or gapped candles silently enter modelling | Low after mitigation | High | Enforce required fields, strict ordering, expected cadence, symbol/interval consistency, valid OHLC, positive prices and non-negative activity before writing data |
| GARCH likelihood uses information from the return being scored | Low after mitigation | High | Score each return using the preceding conditional variance, then update the next variance; retain a regression test for the recursion |
| GARCH-to-rolling conversion mishandles the random sample mean | Low after mitigation | Medium | Derive the expected sample variance algebraically and retain a numeric regression test for the conversion |
| LSTM overfits the small daily dataset or distracts from the final written argument | Medium | High | Use chronological validation, early stopping, and discuss the LSTM result critically rather than assuming it must win |
| Realised volatility proxy is imperfect | Medium | Medium | State that rolling realised volatility is an estimate and cite Patton (2011) when discussing proxy limitations |
| One holdout score is treated as certain | Medium | Medium | Report 14/30-day windows, test halves, four expanding-window blocks, volatility regimes and a paired moving-block bootstrap; avoid claiming universal superiority |
| AI-supported drafting is disclosed inaccurately or not at all | Medium | High | Use a factual candidate-specific disclosure that follows centre policy; do not invent supervisor approval, signatures, or authorship claims |
