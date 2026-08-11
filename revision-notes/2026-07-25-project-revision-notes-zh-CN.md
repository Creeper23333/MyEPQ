# EPQ 项目修改清单（工作稿）

**修改要点日期：2026 年 7 月 25 日**

**当前双语清稿整理日期：2026 年 8 月 9 日**

**文件性质：**本文件保留候选人 7 月 25 日的修改要点。OpenAI Codex 于 8 月 9 日协助整理、编辑并翻译当前双语清稿。本文件不是经过认证的导师反馈或老师评语。

## 1. 研究题目、Research Question、Aim 与 Objectives

目前题目中的 “Bitcoin volatility” 范围过大。文章实际研究的是 Hyperliquid BTC 永续合约日度数据，以及由该数据构造的滚动波动率代理指标，因此题目和 Research Question 都应收窄。

建议 Research Question 改为：

> **To what extent do Random Forest and LSTM justify their additional complexity over rolling historical volatility and GARCH(1,1) when forecasting the next-day update of a volatility proxy constructed from Hyperliquid BTC perpetual-futures returns?**

建议 Aim 改为：

> **To determine whether the additional complexity of Random Forest and LSTM is justified when forecasting the next-day update of a daily volatility proxy constructed from Hyperliquid BTC perpetual-futures returns.**

Objectives 需要写得更明确，使 Examiner 能直接看出项目如何回答 Research Question。建议写为：

1. 使用已完成的 Hyperliquid BTC 永续合约日线数据构造可复现的日度波动率代理指标，以 30 日滚动样本标准差为主要目标，并以 14 日窗口进行稳健性检验。
2. 实现 rolling historical volatility、GARCH(1,1)、lagged linear regression、Random Forest 与 LSTM，并说明每个模型使用的输入、训练样本、预测目标和输出转换。
3. 使用 RMSE、MAE 和补充指标 QLIKE 比较预测准确性。
4. 通过不同目标窗口、时间区段、expanding-window folds、volatility regimes、data refresh、随机种子和 block bootstrap 检验结果的稳健性。
5. 比较模型的可解释性与实践复杂度，包括参数、系数、特征重要性、网络结构、调参负担、依赖项、模型规模和本地运行时间。
6. 判断 Random Forest 或 LSTM 的改进是否足够明显、稳定并且具有实际意义，从而证明其额外复杂度是合理的。

最终判断应围绕四个核心维度展开：

| 维度 | 主要证据 |
| --- | --- |
| Accuracy | RMSE、MAE、QLIKE |
| Robustness | 不同窗口、时间区段、folds、regimes、refresh、seeds、bootstrap |
| Interpretability | 公式、参数、系数、特征重要性、网络结构及实际生成的解释材料 |
| Practicality | 调参和实现负担、依赖项、模型规模、训练稳定性、本地 fit/predict time |

Reproducibility 不必与上述四个维度争夺篇幅，但应作为贯穿整个项目的基本要求，通过固定日期、随机种子、配置、元数据、测试和 Production Log 来体现。

## 2. 明确预测目标

论文必须准确说明模型预测的是什么。主要预测目标不是独立观测到的“真实 Bitcoin volatility”，而是下一日更新后的 30 日滚动收益率标准差，即 `RV(t+1, 30)`。

当前窗口和下一日窗口共享 29 个收益率。最早的一个已知收益率移出窗口，新的未知收益率 `r(t+1)` 进入窗口。因此，这个任务本质上是在预测新收益率会如何改变一个高度重叠、具有很强持续性的滚动代理指标，而不是预测一个完全由未来市场重新形成的波动率。

正文中可以直接写：

> At time t, the model forecasts the 30-day rolling standard deviation after the return for day t+1 becomes available. The updated window shares 29 returns with the current window, so the target is a next-day update of an overlapping volatility proxy rather than a direct observation of latent market volatility.

这一点应在题目、Research Question、Abstract、Methodology、Results 与 Conclusion 中保持一致。文章中重复解释同一信息的地方可以合并。图中模型差异较大的区段也应结合这一目标结构解释：当新进入收益率较极端时，原有 29 个共享观测对预测的帮助会减弱。

## 3. Methodology 与模型比较的公平性

### 3.1 各模型的角色

- Rolling historical volatility 是最简单的 persistence benchmark，直接利用相邻窗口的高度重叠。
- GARCH(1,1) 是 conditional-variance benchmark，需要把下一期条件方差转换为滚动标准差代理指标的预测。
- Lagged linear regression 是低复杂度的监督学习比较项，用于捕捉工程化特征中的近似线性关系，应单独报告。
- Random Forest 与 LSTM 是能够表示非线性关系的高复杂度模型。

不能把模型表现简单归因于 “nonlinear architecture”。Random Forest 与 LSTM 不仅模型结构不同，使用的 feature、sequence、有效样本量、超参数和训练方法也不同。除非进行严格的 matched experiment 或 ablation，否则只能说明当前实现的完整 pipeline 是否增加了价值。

### 3.2 GARCH 与监督学习模型并非同一管线

GARCH 先预测下一期 conditional variance，再转换为滚动标准差代理指标。当前报告中的 Linear Regression、Random Forest 与 LSTM 使用工程化特征直接预测下一日滚动代理目标。口头讨论中也使用了 `r(t+1)^2` 表示新进入收益率的未知贡献，因此最终写作时必须回到代码核验，明确每个模型实际预测的是 `RV(t+1)`、`r(t+1)^2`，还是其他中间变量。

结论不能写成：

> GARCH is better than LSTM.

应写成：

> The current GARCH-based forecasting pipeline outperformed the current direct-target LSTM pipeline under this experimental design.

如果时间允许，可增加一个同管线比较作为拓展：让所有模型预测相同的中间量，例如新进入收益率的条件二阶矩，再使用同一个滚动窗口转换。这是加分项，不是完成 EPQ 的必要条件。

### 3.3 不同模型的 Feature 不完全一致

不同输入会影响实验的严格公平性，但不需要因此把现有实验和 Results 全部重做。应当：

- 列出每个模型的 feature 和 sequence length；
- 解释不同输入表示的原因；
- 报告有效训练样本量；
- 承认项目比较的是完整的、项目特定的 pipelines；
- 避免把所有表现差异都归因于模型类别。

例如，不应写：

> LSTM is not effective for Bitcoin volatility forecasting.

应写：

> LSTM did not provide a stable benefit under the available daily sample, selected inputs, and current training procedure.

### 3.4 Random Forest 实现

目前的 Random Forest 是简化的 project-local regressor，并不是一个具有充分代表性、经过广泛验证的标准库实现。对 EPQ 而言这一实现可以保留，但必须准确说明；其表现较差不能被用于否定 Random Forest 这一模型类别。

更专业的做法是使用标准 library Random Forest，并记录 library 版本、随机种子、树数量、最大深度、最小叶节点、feature subsampling 和 tuning 方法。如果时间不足，则应保留现有实现，同时把它明确称为 “lightweight project-local Random Forest implementation”，并收窄结论。

### 3.5 Hyperparameter Tuning

需要核验 Random Forest 与 LSTM 的超参数为什么这样设置，以及调参过程是否公平。应记录：

- 哪些参数预先固定，以及理由；
- 考虑过哪些参数或范围；
- 是否使用 chronological validation，而不是 final test set；
- 用哪个 metric 选择参数；
- 随机种子和 LSTM early stopping 的处理；
- 是否因 EPQ 的规模与时间限制而有意使用小模型。

如果没有进行充分或同等规模的 tuning，应将其写成 limitation，不能暗示当前结果代表该模型类别能够达到的最佳表现。

## 4. Evaluation Metrics 与 Results

RMSE 与 MAE 应保留，因为二者直观、容易解释。但波动率本身不可直接观测，当前 target 只是一个 imperfect proxy，因此建议增加 QLIKE 作为补充指标。

Patton（2011）讨论了使用不完美波动率代理指标比较预测时，loss function 可能改变模型排名的问题，并说明 QLIKE 在相关假设下具有较好的稳健性。QLIKE 应在 variance scale 上计算：

> `v_t = max(y_t^2, epsilon)`
> `v_hat_t = max(y_hat_t^2, epsilon)`
> `QLIKE_t = v_t / v_hat_t - ln(v_t / v_hat_t) - 1`

QLIKE 越低越好。论文需要说明 `epsilon` 的取值、非正预测如何处理，以及 QLIKE 是在标准差预测平方后计算的。

QLIKE 不能被写成彻底解决了 proxy 问题。Patton 的结论依赖相应假设，而本项目使用的是 30 日重叠滚动方差，因此更准确的说法是：QLIKE 提供了一项与 imperfect volatility proxy 有关的补充稳健性检验。

建议引用：

Patton, A. J. (2011), “Volatility forecast comparison using imperfect volatility proxies,” *Journal of Econometrics*, 160(1), 246-256. [DOI](https://doi.org/10.1016/j.jeconom.2010.03.034)；[作者主页全文](https://public.econ.duke.edu/~ap172/Patton_vol_proxies_JoE_2011.pdf)。

现有 Results 对 Accuracy 与 Robustness 的回答已经比较充分。加入 QLIKE 后，应将其排名与 RMSE、MAE 并列展示，并讨论三者是否给出不同结论。只有在新结果确实支持时才改变主结论，同时应同步更新相关 tables、discussion、conclusion 和 appendices。

## 5. Interpretability 与 Practicality

Interpretability 对 EPQ 来说基本合格，但证据弱于 Accuracy 与 Robustness。建议补充：

- Linear regression：在正文或 Appendix 中列出标准化 coefficients，展示方向和大小。
- GARCH(1,1)：解释 omega、alpha、beta、persistence 以及从 conditional variance 到 rolling proxy 的转换。
- Random Forest：展示 impurity importance；如已有结果，也可展示 permutation importance。需要说明 feature importance 是关联性证据，不能解释单个预测，也可能在相关特征之间分散。
- LSTM：architecture、loss curve 和 seed stability 主要说明模型结构与训练稳定性，并不等于解释了具体预测。如果时间允许，可增加少量 holdout cases 的 sensitivity 或 ablation 分析，但必须标明是探索性证据。

Practicality 不能只用 runtime 回答。本地 fit/predict time 可以保留，但还应讨论：

- 调参和实现步骤的数量；
- library 与运行环境依赖；
- 训练稳定性和 seed sensitivity；
- 模型参数量、节点数或结构规模；
- 复现、维护和解释的难度。

可以说 GARCH 在本项目中需要较少的调参和实现选择，但不能仅凭本地运行时间证明 GARCH 在一般部署中明显更快。

## 6. Conclusion、Academic Writing 与 Source Evaluation

Conclusion 必须限定在当前数据、target、features、implementations 和 tuning budget 之内。建议使用下面这种表述：

> 在本次测试的日度样本中，当前 GARCH 流程在误差、稳定性和实现负担之间表现最好。随机森林和 LSTM 总体上都没有超过滚动基准。这项判断只限于当前目标、输入、实现和调参范围；不同数据或设计可能得到另一种排名。

全文需要进行一次 academic-writing 修改，重点是：

- 统一使用 forecast、proxy、pipeline、conditional variance 和 rolling standard deviation；
- 区分 evidence、interpretation 与 speculation；
- 先说明 assumptions，再解释结果；
- 避免从关联性结果推出因果结论；
- 用 “the tested model” 或 “the current pipeline” 代替对整个模型类别的普遍判断。

项目已经体现了足够的 critical thinking 与 evaluation。Source Evaluation 还可以进一步比较不同文献的数据频率、volatility target、市场、预测期限、模型实现、验证方法、同行评审情况、相关性与限制。该部分可以放入 Appendix 和 Source Evaluation。

## 7. Production Log 与下一轮修改

后续所有修改都要记入 Production Log，包括：

- 修改日期；
- 引发修改的问题或决定；
- 修改了哪些文字、代码、实验、表格或图片；
- 修改原因；
- 哪些结果或结论受到影响；
- 修改后的反思与仍存在的限制；
- 相关文件或证据位置。

修改记录应写清改了什么、为什么改、哪些结果或结论受到影响，以及证据保存在哪里。以后如有真实导师意见，应另行记录实际日期，并使用原话或获批准的转述。正式 Production Log 应由候选人根据自己的实际记录和中心签发的表格填写。
