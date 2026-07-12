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
| Random train-test split gives misleading results | Medium | High | Use chronological split or walk-forward validation |
| LSTM overfits the small daily dataset or distracts from the final written argument | Medium | High | Use chronological validation, early stopping, and discuss the LSTM result critically rather than assuming it must win |
| Realised volatility proxy is imperfect | Medium | Medium | State that rolling realised volatility is an estimate and cite Patton (2011) when discussing proxy limitations |
