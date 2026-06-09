#!/usr/bin/env node
/**
 * [INPUT]: node:fs/path/os；包内 skills/ 目录（两个 skill 的全部文件）
 * [OUTPUT]: 把 mckinsey-deck + mckinsey-market-research-deck 安装到
 *           ~/.claude/skills/（默认）或 ./.claude/skills/（--project）
 * [POS]: 包的唯一入口 — npx 30x-mckinsey-research-deck 即安装，无任何依赖
 * [PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
 */
const fs = require("fs");
const path = require("path");
const os = require("os");

const SKILLS = ["mckinsey-deck", "mckinsey-market-research-deck"];
const SRC = path.join(__dirname, "..", "skills");

const args = process.argv.slice(2);
if (args.includes("--help") || args.includes("-h")) {
  console.log(`
30x-mckinsey-research-deck — McKinsey-grade market research decks for Claude Code

用法:
  npx 30x-mckinsey-research-deck            安装到 ~/.claude/skills/   (全局, 推荐)
  npx 30x-mckinsey-research-deck --project  安装到 ./.claude/skills/   (仅当前项目)

安装后, 在 Claude Code 里说一句:
  帮我做一份 XX 的麦肯锡市场研究 deck
`);
  process.exit(0);
}

const dest = args.includes("--project")
  ? path.join(process.cwd(), ".claude", "skills")
  : path.join(os.homedir(), ".claude", "skills");

fs.mkdirSync(dest, { recursive: true });

for (const name of SKILLS) {
  const from = path.join(SRC, name);
  const to = path.join(dest, name);
  const existed = fs.existsSync(to);
  fs.cpSync(from, to, { recursive: true });
  console.log(`  ${existed ? "↻ 已更新" : "✓ 已安装"}  ${name} → ${to}`);
}

console.log(`
完成。两个 skill 已就位:
  · mckinsey-market-research-deck — 完整研究生产线 (研究→验证→deck)
  · mckinsey-deck                 — 轻量排版 + 渲染引擎 (引擎唯一真相源)

在 Claude Code 里开始:
  帮我做一份 XX 的麦肯锡市场研究 deck

环境要求: Claude Code + 联网搜索 + Chrome (headless 导出 PDF)。
`);
