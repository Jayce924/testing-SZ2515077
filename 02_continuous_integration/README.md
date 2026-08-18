# 实验二：持续集成测试

## 项目介绍

`flight-risk` 是一个小型、可打包的 Python 库，根据能见度、风速、降水、过站时间和机场拥堵度估计航班延误风险。项目与实验一的外部 REST 服务不同，属于本地业务计算软件。

## 本地验证

```powershell
python -m pip install -e ".[test]"
python -m pytest -v --junitxml=reports/junit.xml
python -m pip install build
python -m build
```

## GitHub Actions 验收点

根目录 `.github/workflows/ci.yml` 在 push 和 pull request 时自动执行：

1. 安装 Python 3.12 和项目依赖。
2. 执行 10 个测试并生成 JUnit XML 报告。
3. 构建 wheel 与 source distribution。
4. 上传测试报告和 Python 包作为 workflow artifacts。
