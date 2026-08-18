# 提交前检查清单

## GitHub 操作

1. 在 GitHub 新建空仓库 `software-testing-lab-SZ2515077`。
2. 在本目录执行 `git add .`、`git commit`，再添加远端并推送 `main` 分支。
3. 打开 **Actions**，确认 `Python CI - Flight Delay Risk` 为绿色成功状态。
4. 打开该 workflow run，确认 `Run automated tests` 和 `Build wheel and source package` 成功。
5. 在页面底部确认存在两个 Artifacts：`pytest-junit-report` 与 `flight-risk-packages`。

## 必补截图

- 图 2-2：GitHub 仓库首页，建议让页面中同时出现仓库名与学生姓名/学号。
- 图 2-3：Actions 成功概要页，显示绿色勾、commit 与运行时间。
- 图 2-4：`Run automated tests` 日志，显示全部测试通过。
- 图 2-5：Artifacts 区域，显示测试报告与构建包。

## 报告替换位置

打开实验报告 DOCX，搜索“待补 GitHub 截图”，依次插入上述图片并删除黄色提示框。不要使用伪造截图。

## 最终提交

- 实验报告 DOCX/PDF 中姓名与学号正确。
- 三个实验对象不同，均有缺陷风险分析、步骤、结果和个人思考。
- 关键图片已经内嵌，不使用短期链接。
- 源码、测试、配置、JUnit 报告、构建包及性能结果均在压缩包内。
- 附有大语言模型 prompt 和回答记录。
