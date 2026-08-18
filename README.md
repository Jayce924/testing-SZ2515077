# 软件测试综合实验

- 学生：刘智超
- 学号：SZ2515077
- 技术路线：Python + pytest + GitHub Actions

本仓库包含三个相互独立的实验对象：

1. `01_service_api_test`：面向公开 Open-Meteo 服务的 REST 接口测试。
2. `02_continuous_integration`：航班延误风险评估 Python 包及 GitHub Actions 流程。
3. `03_performance_profiling`：航班日志分析器的 CPU/内存性能跟踪与优化对比。

三个目录均包含独立的说明、代码、测试和运行命令。课程报告及最终提交压缩包由仓库外的交付流程生成。

## GitHub 使用

在 GitHub 新建空仓库后，在本目录执行：

```powershell
git add .
git commit -m "Complete software testing experiments"
git remote add origin https://github.com/<你的用户名>/software-testing-lab-SZ2515077.git
git branch -M main
git push -u origin main
```

如果 Git 首次提交提示身份未配置，请先按 GitHub 账户信息设置当前仓库的
`user.name` 和 `user.email`；不要照抄他人的邮箱。

推送后，根目录下的 `.github/workflows/ci.yml` 会自动测试并打包实验二。
