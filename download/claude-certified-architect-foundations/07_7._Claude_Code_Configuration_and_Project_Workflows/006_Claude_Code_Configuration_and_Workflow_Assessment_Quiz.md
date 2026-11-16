# Claude_Code_Configuration_and_Workflow_Assessment_Quiz

Source: https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-configuration-and-workflows-assessment-quiz

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Claude Code Configuration and Workflows Assessment Quiz

Explore Claude Code’s configuration system through a scenario-based quiz to reinforce your grasp of settings hierarchy, permission rules, hooks, commands, and agent SDK usage. This lesson helps you develop the reasoning skills needed to apply configuration rules correctly and prepare for real-world engineering challenges.

We'll cover the following...

- [Chapter summary](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-configuration-and-workflows-assessment-quiz#Chapter-summary)

This quiz covers the Claude Code configuration system introduced in this chapter. Each question presents a realistic engineering scenario. To choose the correct answer, you need to apply the rules and precedence logic from the lessons in this chapter rather than only recalling definitions. Select the single best answer for each question, then compare your reasoning with the explanation for that question.

Technical Quiz

1.

A developer has the following two settings files on their machine:

`~/.claude/settings.json`:

```
{
  "permissions": {
    "allow": ["Read(**)", "Bash(git status)", "Bash(git log *)"]
  }
}
```

`.claude/settings.json` (project-level):

```
{
  "permissions": {
    "allow": ["Bash(npm run *)", "Bash(python -m pytest *)"]
  }
}
```

After Claude Code starts in the project, which tool calls are pre-approved without a prompt?

A.

Only the project-level allows: `npm run *` and `python -m pytest *`

B.

Only the user-global allows: `Read(**)`, `git status`, and `git log *`

C.

Only `Read(**)` because file reads are always allowed by default

D.

All five: the user-global and project-level allow lists are merged

---

1 / 15

## Chapter summary[#](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-configuration-and-workflows-assessment-quiz#Chapter-summary)

Before you continue, make sure you can explain these five ideas clearly:

1. The four-file hierarchy resolves top to bottom. `~/.claude/settings.json` sets defaults; `.claude/settings.json` adds team settings; `.claude/settings.local.json` adds personal overrides; and `CLAUDE.md` is injected as project context, not merged as settings. Permission lists are additive. The last file wins on non-list keys.
2. Hooks are shell commands tied to life cycle events. `PreToolUse` can block by exiting with code 2 (not code 1). `PostToolUse` observes after the fact. `Stop` fires at session end. Hook exit code 1 is a script error that does not block; only exit code 2 blocks deliberately.
3. Deny overrides allow, always. A tool call that matches both an allow and a deny pattern is blocked. A call that matches neither is sent to the user for approval. No implicit allow exists for any tool.
4. Project commands are team conventions; user commands are personal. `.claude/commands/` is version-controlled and shared. `~/.claude/commands/` is personal and travels with the developer. `$ARGUMENTS` resolves to an empty string if not provided. Command files must handle the no-argument case explicitly. Skills are the newer format: a folder in `.claude/skills/` with a `SKILL.md` file adds supporting files, automatic loading by description, and control over who can invoke it. `allowed-tools` pre-approves tools; it does not restrict them.
5. Plan-first separates intent from execution; `--print` separates execution from interaction. Use plan mode when the task is wide in scope, touches irreversible operations, or involves assumptions that the developer should verify before changes begin. Use `--print` for CI pipelines and any non-interactive automation. Exit code 0 from `--print` means Claude Code ran; it does not mean the output is clean.

In the next chapter, we shift from configuration to correctness. We will cover validation, retry loops, and quality metrics: how to write validators that catch semantic errors even when output structure is valid, how to produce retry feedback that actually improves the next attempt, and how to measure quality at the level of document type, field, and workflow stage rather than as a single aggregate score.

Planning, Iteration, and CI Automation

Validators and Retry Feedback

Ask

[Chapter summary](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-configuration-and-workflows-assessment-quiz#Chapter-summary)