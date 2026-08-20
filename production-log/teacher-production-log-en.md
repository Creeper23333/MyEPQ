# Production Log

## Project idea

My first idea was about machine learning and cryptocurrency, but it did not specify an asset or a target. I narrowed it to Bitcoin volatility so that the models could be compared using numerical errors. My research question became:

**To what extent do Random Forest and LSTM justify their additional complexity over rolling historical volatility and GARCH(1,1) when forecasting the next-day update of a volatility proxy constructed from Hyperliquid BTC perpetual-futures returns?**

I chose volatility because it is linked to market risk and can be measured and compared more clearly than a general question about whether Bitcoin will go up or down. My main aim was to find out whether the extra complexity of Random Forest and LSTM was actually useful when compared with simpler statistical methods.

## Planning and research

The early research notes cover log returns, volatility, rolling historical volatility, GARCH, Random Forest and LSTM. The recorded plan uses one Bitcoin dataset and one test period, comparing error together with explanation, running time and whether the result stayed similar in later checks.

The first plan used Yahoo Finance data. The documented source was later changed to Hyperliquid so that the project referred to one specific Bitcoin perpetual-futures market. The data included each day's open, high, low, close, volume and trade count.

The recorded plan used this order:

1. collect and check the Bitcoin data;
2. calculate log returns and a rolling volatility target;
3. build simple baseline methods;
4. add Random Forest and LSTM;
5. compare every model on later data;
6. check the results again using different settings;
7. use the results to answer whether extra complexity was worthwhile.

## Data preparation and first comparison

The saved data retain the original Hyperliquid daily rows alongside the processed dataset. Derived outputs use daily log returns and their 30-day rolling sample standard deviation as the volatility measure. The target is the next day's updated value. Two neighbouring windows share 29 returns, so the task predicts an update, not a completely new future 30-day period.

The comparison starts with rolling historical volatility as a simple, explainable baseline. It adds GARCH to model periods of high and low volatility and lagged linear regression as a simple check before Random Forest and LSTM.

The data remain in date order, with the earlier part used for training and the later part for testing. The comparison does not randomly shuffle the rows because that could allow future market information to affect an earlier forecast. The saved evaluation uses RMSE and MAE on the standard-deviation proxy and QLIKE on squared target and forecast values.

## Problems and changes

Several checks changed the method. One refresh included a daily candle that had not ended, so its close, volume and trade count were incomplete. The data step was changed to keep completed candles only.

The GARCH predictions had also been joined by row number rather than by date. That could compare a forecast with the wrong target day. The matching was changed to use dates, and the full comparison was rerun.

The final method revision corrected the GARCH update order and rolling-target conversion, and LSTM scaling used training data only. The project-local forest was replaced with scikit-learn's Random Forest. Six RF settings and four LSTM settings were compared using the end of the training period; the final test set was not used to choose them. QLIKE, a linear-coefficient table and an LSTM input-removal check were also added.

## Further checks

The saved robustness outputs repeat the comparison with 14-day and 30-day targets, the first and second halves of the test period, low-, medium- and high-volatility periods and four expanding time windows.

Random Forest outputs include the chosen settings, out-of-bag error and feature importance. LSTM outputs cover three seeds and one-input-at-a-time removal to show which inputs most affect its errors. The models use different inputs and transformations, so the result compares the complete tested pipelines; it does not isolate the effect of model type alone.

## Final result

The 20 August refresh returned 1,272 Hyperliquid daily rows. Excluding one unfinished row left 1,271 completed days through `2026-08-19`. The modelling frame contains 1,226 forecast origins. The frozen split still uses 950 earlier rows for training, while the later test has extended to 276 rows and its target dates now run through 19 August.

The final 30-day results were:

| Model | MAE | RMSE | QLIKE |
| --- | ---: | ---: | ---: |
| GARCH(1,1) | 0.00048109 | 0.00098301 | 0.00445845 |
| Lagged linear regression | 0.00072090 | 0.00137492 | 0.00724584 |
| Rolling historical volatility | 0.00061444 | 0.00139570 | 0.00754794 |
| LSTM | 0.00099818 | 0.00168735 | 0.00897661 |
| Random Forest | 0.00123057 | 0.00211129 | 0.01182354 |

GARCH ranked first in the main comparison and also remained first in the 14-day, test-half, volatility-group and expanding-window checks. Neither LSTM nor Random Forest beat the rolling baseline overall. The fixed-cutoff comparison with the earlier 19 July archive preserved all five ranks.

The last target covers a sharp move: BTC closed at 69,323 on 19 August, up from 64,696 on 18 August. Its log return was `0.06908`, and the 30-day proxy rose from `0.0121249` to `0.0174694`. Because the forecast origin was 18 August, the move was not yet known when that target was forecast. This records a shock-day miss; it is not a reason to tune on the holdout and score the revised model on the same day.

Within this comparison, GARCH performed best. Random Forest and LSTM were more complicated and did not beat the rolling baseline. The finding is limited to the tested market, dates, inputs and pipelines; a different dataset or design may give another ranking.

## AI and authorship note

OpenAI Codex assisted with code review and editing, data processing and checks, software tests, writing and editing, English-Chinese translation, and DOCX/PDF export. Repository files and timestamps show saved work, not who performed each action. Only research choices and checks personally verified by the candidate should be presented as the candidate's own work.

## Reflection

The saved corrections show that date alignment, completed-candle filtering and information timing affected the comparison. The result is limited to the tested market, dates, features and pipelines.

**Candidate adds own reflection:** {{CANDIDATE_REFLECTION_IN_OWN_WORDS}}
