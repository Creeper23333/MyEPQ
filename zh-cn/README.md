# EPQ 中文文档

> 最后核对：2026-08-09
> 最后一根完整日线：2026-07-19

本目录只保留当前中文成品，不存放重复副本或旧版草稿。

## 当前文件

- [最终报告中文版](final-report-zh-cn.md)：与英文最终报告对应的完整中文版本
- [完整 Production Log 中文版](complete-production-log-zh-cn.md)：与英文版结构严格一致的核对稿
- [完整 Production Log 中文 Word 版](complete-production-log-zh-cn.docx)：由 Markdown 可重复生成
- [中文每周工作日志](weekly-work-log-zh-cn.md)：与英文每周日志对应

英文正本入口：

- [项目总览](../README.md)
- [最终英文报告](../report/final-report.md)
- [完整 Production Log 英文版](../production-log/complete-production-log-en.md)
- [最终展示讲稿](../presentation/final-presentation-script.md)

## 研究问题

研究问题是：预测由 Hyperliquid 比特币永续期货收益率构建的波动率代理值的次日更新时，Random Forest 和 LSTM 增加的复杂度在多大程度上值得？

日期为 $t$ 的特征预测下一根完整日线更新后的滚动波动率：

$$
y_t = RV_{t+1}^{(n)}.
$$

这里主要使用 30 日目标，并以 14 日目标做稳健性检查；研究对象不是价格涨跌，也不是未来 30 天的方向预测。

## 当前数据与结果

- Hyperliquid API 返回 1,241 行，排除 1 根未完成日线后保留 1,240 行。
- 数据范围为 2023-02-26 至 2026-07-19。
- 30 日建模表有 1,195 个预测起点，其中训练集 950 行，固定测试集 245 行。
- 测试边界固定在 2025-11-16；另有四个扩展窗口分段检查。
- 43 项自动化测试全部通过。

30 日固定留出结果：

| 排名 | 模型 | RMSE | QLIKE |
| ---: | --- | ---: | ---: |
| 1 | GARCH(1,1) | `0.00098502` | `0.00370047` |
| 2 | 滞后线性回归 | `0.00140087` | `0.00623445` |
| 3 | 滚动历史波动率 | `0.00142744` | `0.00669043` |
| 4 | LSTM | `0.00174351` | `0.00816805` |
| 5 | Random Forest | `0.00220594` | `0.01170773` |

结论是：在本次实验中，GARCH 流程表现最好。Random Forest 和 LSTM 增加了复杂度，却没有带来足够稳定的准确性改进。由于各模型的输入和转换不同，这不是对所有算法或所有比特币市场的普遍结论。

## 数值核对优先级

文档数字如与重跑输出不一致，以生成文件为准：

1. [`model_performance.csv`](../code/outputs/model_performance.csv)
2. [`model_walk_forward_performance.csv`](../code/outputs/model_walk_forward_performance.csv)
3. [`model_robustness_by_window.csv`](../code/outputs/model_robustness_by_window.csv)
4. [`model_run_metadata.json`](../code/outputs/model_run_metadata.json)
5. [`hyperliquid_BTC_1d_quality_report.json`](../data/raw/hyperliquid_BTC_1d_quality_report.json)

## 文档维护规则

- 英文报告只维护 `report/final-report.md`。
- 中文报告只维护 `zh-cn/final-report-zh-cn.md`。
- 中英文 Production Log 各保留一个 Markdown 源文件和一个生成的 Word 文件。
- 旧草稿、重复导出和拆分式中文指南不放在当前目录；需要追溯时使用 Git 提交历史。
