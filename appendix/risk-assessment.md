# Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Project scope becomes too broad | Medium | High | Focus mainly on Bitcoin; keep Ethereum as optional extension |
| Machine learning model is too complex to explain clearly | Medium | Medium | Use Random Forest before LSTM; evaluate interpretability separately from accuracy |
| Data source changes or becomes unavailable | Low | Medium | Save raw data locally and record source details |
| Results do not show machine learning improvement | Medium | Low | Treat this as a valid finding and evaluate why simpler models may be sufficient |
| Time pressure near deadline | Medium | High | Set staged deadlines and keep appendices updated during the project |
| Accidental plagiarism or weak referencing | Low | High | Record sources immediately and write literature notes in original wording |
| Random train-test split gives misleading results | Medium | High | Use chronological split or walk-forward validation |
| LSTM overfits small daily dataset | Medium | High | Start with a small architecture, use scaling, compare against simple baselines, and discuss limitations |
| Realised volatility proxy is imperfect | Medium | Medium | State that rolling realised volatility is an estimate and cite Patton (2011) when discussing proxy limitations |
