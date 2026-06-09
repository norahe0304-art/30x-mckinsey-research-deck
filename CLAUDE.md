# 30x-mckinsey-deck - Claude Code 麦肯锡级市场研究 deck skill 发布包
Node (零依赖 CLI) + Markdown skills + Python 渲染引擎

<directory>
bin/ - cli.js: npx 安装器, 把 skills/ 复制进 ~/.claude/skills/ 或 ./.claude/skills/
skills/mckinsey-deck/ - 排版 skill: SKILL.md + assets/deck_engine.py (引擎唯一真相源)
skills/mckinsey-market-research-deck/ - 研究 skill: SKILL.md + README.md + references/ (methodology · design-system · qc-checklist · image-handoff)
docs/ - index.html: 介绍页 (GitHub Pages 可直接启用)
</directory>

<config>
package.json - npm 包定义, bin 入口, files 白名单
LICENSE - MIT (30x Company)
</config>

铁律: 引擎只活在 skills/mckinsey-deck/assets/deck_engine.py — 上游修复同步到这里, 禁止分叉。
发布: npm version patch|minor && npm publish; GitHub 同步 push。

[PROTOCOL]: 变更时更新此文件，架构调整必须同步此地图。
