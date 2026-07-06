# CAD Agent Skill

<p align="center">
  <a href="README.zh-CN.md"><img alt="中文说明" src="https://img.shields.io/badge/README-%E4%B8%AD%E6%96%87-1F883D?style=for-the-badge"></a>
  <a href="README.md"><img alt="English README" src="https://img.shields.io/badge/README-English-0969DA?style=for-the-badge"></a>
</p>

这是一个辅助 CAD Agent 工作的开源 skill 示例。它面向 CAD 工业设计，把开放式设计需求整理成可检查、可复现、可交接的结构化产物，便于在真正调用 CAD 建模后端之前完成规划、追踪和验证。

流程如下：

```text
输入资料 -> CAD IR -> 组件目录查询 -> 放置规划 -> 执行图 -> 验证报告
```

## 作为 CAD Agent Skill

这个仓库可以理解为辅助 CAD Agent 工作的 skill / workflow layer。它不是让 Agent 一步生成几何模型，而是先把需求、组件选择、放置关系、执行顺序和验证结果拆成可审查的中间产物，再交给下游 CAD 后端执行。

作为 CAD Agent skill，它主要帮助完成：

- 把自然语言 CAD 需求转换成结构化 CAD IR。
- 从组件目录中选择可复用组件。
- 生成确定性的放置规划，供后续 CAD 执行使用。
- 构建带检查点和依赖关系的执行图。
- 在建模前检查缺失字段、不安全假设和需要人工复核的内容。

## 目标

在 CAD 自动化场景中，直接让智能体自由生成几何模型，往往会带来三个问题：

- 过程难复现
- 决策难审查
- 错误难定位

本仓库提供一个轻量的中间层，把设计需求、组件选择、放置关系、执行顺序和验证结果拆成明确文件。这样可以让维护者先审核结构化计划，再决定是否交给下游 CAD 后端执行。

## 核心产物

- `cad_ir.json`：统一表达输入、约束、零件、装配关系和不确定项。
- `component_catalog.csv`：描述可复用组件的公开示例元数据。
- `placement_plan.csv`：记录组件放置、基准规则、姿态参数和审核状态。
- `execution_graph.json`：描述从输入、规范化、查询、放置、构建到验证的执行节点。
- `validation_report.json`：输出缺失字段、非法数值和需要人工复核的问题。

## 快速开始

```powershell
python -m pip install -e .
python -m unittest discover -s tests
python scripts\privacy_scan.py .
```

初始化一个演示工程：

```powershell
python -m cad_agent_skill init `
  --project-id demo-industrial-panel `
  --root .\out\demo-industrial-panel
```

根据公开或合成需求生成 IR：

```powershell
python -m cad_agent_skill create-ir `
  --project-id demo-industrial-panel `
  --out .\out\demo-industrial-panel\ir\cad_ir.json `
  --requirement "Create a modular industrial control panel with a frame, removable cover, hinge set, and access opening."
```

查询合成组件目录：

```powershell
python -m cad_agent_skill query-catalog `
  --catalog .\examples\synthetic_component_catalog.csv `
  --category hinge `
  --min-confidence medium `
  --out .\out\demo-industrial-panel\planning\hinge_candidates.csv
```

生成并验证放置规划：

```powershell
python -m cad_agent_skill build-plan `
  --selected .\examples\synthetic_selected_components.csv `
  --out .\out\demo-industrial-panel\planning\placement_plan.csv

python -m cad_agent_skill validate-placement `
  --placement-plan .\out\demo-industrial-panel\planning\placement_plan.csv `
  --out .\out\demo-industrial-panel\validation\placement_validation.json
```

## 适用范围

这个仓库关注 CAD 工业设计自动化中的规划、编排和验证层。它更适合作为 CAD Agent 的辅助 skill 或流程编译器，而不是替代 CAD 内核、建模软件或图形查看器。下游系统可以读取本仓库生成的 IR、放置规划和执行图，再执行实际建模。

## 隐私与脱敏

本仓库只包含合成示例和通用流程，不包含真实业务资料、真实主体信息、私有路径、真实 CAD 文件、业务文档或生产组件库。

维护公开版本时，请遵守以下原则：

- 默认只提交合成示例。
- 不提交真实图纸、截图、模型、表格、演示文稿或业务资料。
- 不提交本地机器路径和内部命名。
- 用 `demo`、`synthetic`、`panel`、`frame`、`cover`、`bracket`、`fixture` 等中性词替代真实标签。
- 发布前运行 `python scripts\privacy_scan.py .`。

## 许可证

MIT
