# 实验一：服务单元测试

## 被测对象

Open-Meteo 天气预报 REST API。测试数据选择南京禄口、北京首都和上海虹桥三个机场附近坐标，使测试场景与航空出行相关。

## 风险与测试策略

- 必填经纬度缺失或越界时，接口应明确拒绝，而不是返回误导数据。
- 实时天气数值会随时间变化，不断言固定温度；改为校验字段、类型、单位和合理范围。
- 多地点输入需要参数化，避免复制测试代码。
- 公共网络可能超时，客户端统一使用 10 秒超时并给出清晰异常。

## 运行

```powershell
python -m pip install -r requirements.txt
python -m pytest -v --junitxml=reports/junit.xml
```

测试需联网。免费公共 API 不需要 API Key。
