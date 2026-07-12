# Full Report Draft

## Title

To what extent can machine learning models improve Bitcoin volatility forecasting compared with traditional statistical models?

## Introduction

Cryptocurrency markets are widely described as volatile because prices can rise and fall sharply over short periods of time. Bitcoin is the most established cryptocurrency and has a longer public price history than most alternative coins, so it provides a suitable case study for investigating volatility forecasting. For traders, investors, and risk managers, volatility matters because it represents uncertainty about future returns. A model that forecasts volatility more accurately may help users judge risk exposure, position size, and whether market conditions are unusually unstable.

This project asks:

> To what extent can machine learning models, specifically Random Forest and Long Short-Term Memory networks, improve Bitcoin volatility forecasting compared with traditional statistical models such as rolling historical volatility and GARCH(1,1)?

This question is deliberately comparative rather than purely technical. Traditional time-series models such as rolling historical volatility and GARCH(1,1) are widely used because they are relatively simple, interpretable, and designed to capture volatility clustering. Machine-learning models offer a different approach. Random Forest can capture nonlinear relationships through many decision trees, while LSTM is designed for sequential patterns and long-term temporal dependence. Because cryptocurrency markets may contain nonlinearity and abrupt regime shifts, machine learning appears attractive. However, the project should not assume that newer or more complex methods must automatically be better.

The project therefore evaluates models across more than one dimension. Accuracy is measured using MAE, MSE, and RMSE. Interpretability is also important, because a model that is difficult to explain may be less useful in a small-scale EPQ and less practical for risk-management decisions. Computational practicality also matters, because a method that requires far more tuning or infrastructure may not be worth using unless its gain is substantial.

## Literature Review

The literature supports using Bitcoin volatility forecasting as a meaningful setting for comparing statistical and machine-learning methods, but it does not support a simple assumption that machine learning always wins. Earlier econometric work such as Bollerslev (1986) provides the theoretical basis for GARCH-type models, while Hansen and Lunde (2005) show why GARCH(1,1) remains a serious benchmark rather than a weak baseline.

Cryptocurrency-specific studies add important caution. Katsiampa (2017) shows that Bitcoin volatility can be analysed using GARCH-family models, while Catania, Grassi and Ravazzolo (2019) emphasise model and parameter instability in cryptocurrency forecasting. This supports the use of chronological validation, because a model that performs well in one period may not remain best later.

More recent work broadens the comparison to machine learning. Dudek et al. (2024) compare statistical models, Random Forest, LSTM, and other methods across cryptocurrencies and show that there is no universal winner across every asset, metric, and forecast horizon. Huang, Sangiorgi and Urquhart (2024) provide evidence that machine-learning techniques can outperform traditional volatility models for Bitcoin in their setting, while Shen, Wan and Leatham (2021) support the relevance of recurrent neural-network approaches for Bitcoin volatility forecasting.

These studies justify including both Random Forest and LSTM in the project. However, they also make an important methodological point: academic machine-learning models often use richer features, more extensive tuning, or different target variables than a small-scale EPQ can realistically reproduce. Interpretability research such as Lundberg and Lee (2017) and Molnar (2025) strengthens this concern. A small numerical gain is not automatically worthwhile if it comes with a large loss of transparency and reproducibility.

The current project results fit the balanced side of the literature. They suggest that machine learning can capture useful structure, but they do not support the claim that complex models are automatically superior.

## Mathematical Formulation

Daily logarithmic return is defined as:

```text
r_t = ln(P_t / P_{t-1})
```

where `P_t` is the daily close price. The project uses a 30-day rolling standard deviation of daily log returns as a proxy for realised volatility:

```text
RV_t = stdev(r_{t-29}, r_{t-28}, ..., r_t)
```

This is an observable proxy rather than the true latent volatility of Bitcoin. The forecast target is next-day realised volatility:

```text
y_t = RV_{t+1}
```

GARCH(1,1) is defined through the conditional variance equation:

```text
sigma_t^2 = omega + alpha * epsilon_{t-1}^2 + beta * sigma_{t-1}^2
```

Forecast accuracy is evaluated using:

```text
MAE = mean(|y_t - yhat_t|)
MSE = mean((y_t - yhat_t)^2)
RMSE = sqrt(MSE)
```

## Methodology

The project uses Hyperliquid BTC daily perpetual futures candles from the public public info API. In the latest refresh requested on 2026-07-13, the request window runs from 2023-02-26 to 2026-07-13, and the latest daily candle returned by the API is dated 2026-07-12. Earlier returned candles before 2023-02-26 showed zero volume and zero trade count, so the sample begins from that date to keep the dataset clearly exchange-based.

The modelling pipeline converts daily close prices into log returns, then calculates 30-day realised volatility. The target is shifted forward by one day so that the models forecast future volatility rather than reproducing the current value. The full modelling frame contains 1188 rows. A chronological 80/20 split is used, producing 950 training rows from 2023-04-11 to 2025-11-15 and 238 test rows from 2025-11-16 to 2026-07-11.

Five models are compared:

1. Rolling historical volatility, which predicts that tomorrow's realised volatility equals today's.
2. GARCH(1,1), fitted using grid-search maximum likelihood with variance targeting.
3. Lagged linear regression, using lagged returns, lagged realised volatility, volume-based variables, and rolling features.
4. Random Forest, implemented as a lightweight in-repo model because scikit-learn is not used.
5. LSTM, implemented in PyTorch using rolling 30-day sequences of core market features, a small hidden layer, and early stopping on a chronological validation split.

This design keeps the comparison fair while still allowing both tree-based and recurrent machine-learning models to be tested.

## Results

The current model ranking is:

| Rank | Model | Category | MAE | MSE | RMSE |
| --- | --- | --- | --- | --- | --- |
| 1 | Lagged linear regression | Interpretable lag-feature model | 0.00074798 | 0.00000201 | 0.00141843 |
| 2 | Rolling historical volatility | Benchmark | 0.00063564 | 0.00000209 | 0.00144481 |
| 3 | LSTM | Machine learning | 0.00106690 | 0.00000339 | 0.00184029 |
| 4 | Random Forest | Machine learning | 0.00121584 | 0.00000443 | 0.00210549 |
| 5 | GARCH(1,1) | Traditional statistical | 0.00987357 | 0.00016712 | 0.01292761 |

The results do not support a simple claim that machine learning improves Bitcoin volatility forecasting. Lagged linear regression achieves the lowest RMSE, and rolling historical volatility is very close behind. The implemented LSTM performs better than the Random Forest, so recurrent sequence modelling does add some predictive value. However, it still does not beat the strongest simple alternatives.

The rolling benchmark performs strongly because the target itself is a rolling measure. If volatility is persistent, then today's realised volatility is already highly informative about tomorrow's realised volatility. The LSTM result suggests that sequence modelling captures some additional structure, but not enough to overturn the dominance of persistence-based features. The Random Forest result is weaker still, suggesting that simple lag-based relationships already explain much of the target signal.

GARCH(1,1) performs worst in the current comparison. One likely reason is target mismatch. GARCH is designed to forecast conditional daily variance, while the evaluation target here is next-day 30-day realised volatility. Even though the script converts the GARCH output into a comparable realised-volatility-style forecast, the link remains less direct than for persistence-based models.

## Discussion

The key finding is not that machine learning has failed completely, but that higher complexity has not yet justified itself against the best simple models. This is important because the project set out to answer whether machine-learning gains are large enough to outweigh lower interpretability and higher implementation cost.

Rolling historical volatility remains a very strong benchmark because the target is persistent by construction. Lagged linear regression goes a step further by using explicit lagged features, and it performs best overall. This matters because it shows that a model can remain mathematically simple, easy to explain, and still highly competitive.

The LSTM result is useful because it prevents the project from turning into a narrow comparison between simple models and a weak machine-learning baseline. The project now includes both a tree-based machine-learning model and a recurrent neural-network model. The fact that the LSTM beats the Random Forest but still loses to the strongest simple models creates a more nuanced conclusion: machine learning is not useless, but its gains are not large enough here to justify declaring it superior.

Interpretability remains central. Rolling historical volatility is the easiest model to explain. Lagged linear regression is also relatively transparent because its inputs are explicit and economically intuitive. Random Forest is less transparent, even with feature importance. LSTM is less interpretable still, because its learned sequence representation is distributed across many parameters. For a project whose final judgment includes practical usefulness, this interpretability gap matters.

The project also has limitations. Realised volatility is estimated from daily returns rather than higher-frequency data. The project uses one core market rather than a multi-asset sample. The Random Forest is lightweight, and the LSTM is intentionally small rather than aggressively tuned. These limitations should be acknowledged clearly. However, they do not weaken the core answer. Instead, they help explain why the project is best interpreted as a fair, small-scale, critical comparison rather than as a search for the most advanced forecasting architecture.

## Conclusion

This project asked whether machine-learning models, specifically Random Forest and LSTM, could improve Bitcoin volatility forecasting compared with traditional statistical models such as rolling historical volatility and GARCH(1,1). Based on the current Hyperliquid BTC daily dataset and the latest modelling results, the answer is limited rather than strongly positive.

Lagged linear regression performs best, with rolling historical volatility extremely close behind. The implemented LSTM improves on the Random Forest but still does not outperform the strongest simple baselines. GARCH(1,1) performs worst on the current target. The project therefore does not support the claim that machine learning automatically improves Bitcoin volatility forecasting.

The wider conclusion is more important than the ranking alone. For this case study, model complexity has not produced a large enough gain to justify its extra interpretability and implementation costs. The most defensible final answer is therefore that machine learning can improve Bitcoin volatility forecasting in some settings, but in this project it has not clearly surpassed simpler alternatives. Complexity should only be preferred when the improvement is large enough to justify it.
