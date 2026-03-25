import os
import shutil
import json
import tomllib

def migrate_builtin_tools(content):
    content = content.replace("`write_file`", "`Write`")
    content = content.replace("`replace`", "`Edit`")
    content = content.replace("`run_shell_command`", "`Bash`")
    content = content.replace("`enter_plan_mode`", "`EnterPlanMode`")
    content = content.replace("`exit_plan_mode`", "`ExitPlanMode`")
    content = content.replace("`ask_user`", "`AskUserQuestion`")
    content = content.replace("~/.gemini/extensions/conductor", "${CLAUDE_SKILL_DIR}")
    return content

def migrate_conductor():
    if os.path.exists("plugins/conductor"):
        shutil.rmtree("plugins/conductor")

    os.mkdir("plugins/conductor/")
    os.mkdir("plugins/conductor/.claude-plugin")

    json.dump({
        "name": "conductor",
        "description": "Conductor is a Claude Code plugin that allows you to specify, plan, and implement software features.",
        "version": "1.0.0",
        "author": {
            "name": "Logitropic"
        }
    }, open("plugins/conductor/.claude-plugin/plugin.json", "w"), indent=2)

    os.mkdir("plugins/conductor/commands")

    shutil.copytree("templates", "plugins/conductor/templates")

    # SETUP
    with open(os.path.join("commands/conductor", "setup.toml"), "rb") as f:
        data = tomllib.load(f)

    with open(os.path.join("plugins/conductor/commands", "setup.md"), "w") as f:
        f.write(
f"""---
description: {data['description']}
argument-hint: [project-type]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
model: inherit
disable-model-invocation: true
---

{migrate_builtin_tools(data['prompt'])}
"""
        )

    # NEW TRACK
    with open(os.path.join("commands/conductor", "newTrack.toml"), "rb") as f:
        data = tomllib.load(f)

    with open(os.path.join("plugins/conductor/commands", "newTrack.md"), "w") as f:
        f.write(
f"""---
description: {data['description']}
argument-hint: [description]
allowed-tools: Read, Write, Glob, Task
model: inherit
disable-model-invocation: true
---

{migrate_builtin_tools(data['prompt'])}
"""
        )

    # NEW TRACK
    with open(os.path.join("commands/conductor", "implement.toml"), "rb") as f:
        data = tomllib.load(f)

    with open(os.path.join("plugins/conductor/commands", "implement.md"), "w") as f:
        f.write(
f"""---
description: {data['description']}
argument-hint: [<track-name>] [--all]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
model: inherit
disable-model-invocation: true
---

{migrate_builtin_tools(data['prompt'])}
"""
        )

    # REVIEW
    with open(os.path.join("commands/conductor", "review.toml"), "rb") as f:
        data = tomllib.load(f)

    with open(os.path.join("plugins/conductor/commands", "review.md"), "w") as f:
        f.write(
f"""---
description: {data['description']}
allowed-tools: Read, Glob, Bash
model: inherit
disable-model-invocation: true
---

{migrate_builtin_tools(data['prompt'])}
"""
        )

    # STATUS
    with open(os.path.join("commands/conductor", "status.toml"), "rb") as f:
        data = tomllib.load(f)

    with open(os.path.join("plugins/conductor/commands", "status.md"), "w") as f:
        f.write(
f"""---
description: {data['description']}
allowed-tools: Read, Glob, Bash
model: inherit
disable-model-invocation: true
---

{migrate_builtin_tools(data['prompt'])}
"""
        )

    # REVERT
    with open(os.path.join("commands/conductor", "revert.toml"), "rb") as f:
        data = tomllib.load(f)

    with open(os.path.join("plugins/conductor/commands", "revert.md"), "w") as f:
        f.write(
f"""---
description: {data['description']}
argument-hint: [track|phase|task] [name]
allowed-tools: Read, Bash, Glob, Grep
model: inherit
disable-model-invocation: true
---

{migrate_builtin_tools(data['prompt'])}
"""
        )

    shutil.copy("GEMINI.md", os.path.join("plugins/conductor", "SKILL.md"))


if __name__ == "__main__":
    if os.path.exists("plugins"):
        shutil.rmtree("plugins")

    os.mkdir("plugins")

    migrate_conductor()
