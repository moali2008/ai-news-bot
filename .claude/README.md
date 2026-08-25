# .claude — project skills & agents

## banana-claude (vendored)

`/plugin` (marketplace install) is not available in Claude Code on the web, and
remote session containers are ephemeral, so the plugin is vendored into the repo
instead. Anything under `.claude/skills/` and `.claude/agents/` is picked up
automatically by Claude Code when working in this repository.

- Source: https://github.com/AgriciDaniel/banana-claude
- Version: 1.4.1 (commit `a4b5a7e`)
- License: MIT (see `skills/banana/LICENSE`)

### Contents
- `skills/banana/` — image-generation Creative Director skill (Gemini "Nano Banana")
- `agents/brief-constructor.md` — sub-agent that builds the optimized prompt

### Setup
The helper scripts are pure standard-library Python, so there is nothing to
install. They need a Google AI API key in the environment:

```bash
export GOOGLE_API_KEY="your-key"   # GOOGLE_AI_API_KEY is also accepted
python .claude/skills/banana/scripts/validate_setup.py
```

Get a key at https://aistudio.google.com/apikey. Do not commit it.

### Updating
Re-copy `skills/banana/` and `agents/brief-constructor.md` from the upstream
repo and bump the version noted above.
