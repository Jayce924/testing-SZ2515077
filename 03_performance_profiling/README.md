# 实验三：程序性能跟踪

## 被测对象

航班运行日志分析器。程序从确定性生成的日志流中统计延误、取消、平均延误时间和最繁忙航线。

项目包含两个实现：

- `analyze_baseline`：先物化全部字典记录，重复扫描航线，并用 `datetime.strptime` 解析每个日期。
- `analyze_optimized`：逐行流式处理，只保存聚合状态，避免重复扫描与大对象列表。

二者输出完全一致，便于把性能差异归因于实现方式，而不是业务语义变化。

## 运行测试与性能分析

```powershell
python -m pytest -v --junitxml=reports/junit.xml
python profile_run.py --records 50000 --out results
```

输出包括：

- `profile_baseline.txt` 与 `profile_optimized.txt`：按累计时间排序的 CPU 热点。
- `baseline.prof` 与 `optimized.prof`：可供 snakeviz 等工具读取的原始数据。
- `comparison.csv`：运行时间、峰值内存及相对改进。
- `summary.json`：业务结果一致性证据。

## 工具比较

| 工具 | 重点 | 优点 | 局限 |
|---|---|---|---|
| cProfile/pstats | 函数调用与 CPU 累计时间 | Python 内置、可重复、无需额外安装 | 函数级为主，行级细节有限 |
| tracemalloc | Python 对象分配和峰值内存 | Python 内置、可比较快照 | 不覆盖所有原生库内存 |
| py-spy | 低侵入 CPU 采样 | 可附加到运行进程 | 需额外安装，短任务采样不稳定 |
| memory_profiler | 逐行内存变化 | 定位直观 | 运行开销较大，需额外安装 |
