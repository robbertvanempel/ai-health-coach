# AI Health Coach

AI Health Coach is an open, privacy-first Agent Skill for health journaling, fitness and sports coaching, nutrition and recovery reflection, wearable-data review, and a source-grounded personal knowledge base.

It combines two ideas:

1. **Longitudinal coaching:** advice improves as the user logs goals, workouts, meals, sleep, recovery, measurements, symptoms, and wearable data.
2. **A health second brain:** raw articles and videos stay intact, AI-generated source cards capture claims and limitations, and future advice can cite the knowledge library.

The public repository contains only blank templates and synthetic placeholders. It contains no personal health data and should never be used to store any.

> [!IMPORTANT]
> This is an educational coaching workflow, not a medical device or a replacement for a physician, registered dietitian, physiotherapist, psychologist, or emergency service. Do not use it to diagnose or treat disease.

## What it does

- Runs a thorough onboarding covering goals, current health and activity, nutrition, recovery, injuries, schedule, equipment, wearables, preferences, privacy, and consent.
- Turns natural-language check-ins and files into a durable private journal and structured logs.
- Reviews trends without overreacting to one weigh-in, one workout, or one wearable score.
- Produces practical, non-shaming coaching with explicit evidence, uncertainty, and safety boundaries.
- Accepts CSV, JSON, PDFs, screenshots, images, and common wearable exports when the host AI can read them.
- Adds articles and videos from Chrome through the official Obsidian Web Clipper.
- Converts captured sources into evidence-labeled source cards that can be cited in later coaching.
- Uses the open `SKILL.md` format across ChatGPT Desktop, Claude Cowork, Grok Bot, Codex, Claude Code, and Grok Build.

## Privacy model

The code and the data live in different places:

```text
public GitHub repository        private user workspace
------------------------        ----------------------
skill instructions              onboarding answers
blank templates                 health profile and goals
initialization scripts          journals and check-ins
Web Clipper templates           wearable exports and images
                                captured knowledge sources
```

Initialize the private workspace outside this cloned repository. The generated workspace includes a defensive `.gitignore` that excludes all data-bearing folders. Read [PRIVACY.md](PRIVACY.md) before connecting cloud services or sharing files with an AI platform.

## Quick start

### 1. Download the skill

Download [`ai-health-coach.zip`](https://github.com/robbertvanempel/ai-health-coach/releases/latest/download/ai-health-coach.zip) from the latest release, or clone the repository:

```bash
git clone https://github.com/robbertvanempel/ai-health-coach.git
cd ai-health-coach
```

### 2. Create a private data workspace

The script uses only the Python standard library and never overwrites existing files:

```bash
python3 skill/ai-health-coach/scripts/init_workspace.py ~/Documents/ai-health-coach-data
python3 skill/ai-health-coach/scripts/validate_workspace.py ~/Documents/ai-health-coach-data
```

If you downloaded the release ZIP, run the same scripts from the extracted `ai-health-coach/` folder.

Open `~/Documents/ai-health-coach-data` as an Obsidian vault if you want browser clipping. Do not initialize the public code repository as your health-data vault.

### 3. Install in your AI app

#### ChatGPT Desktop

1. Open **Skills** in the ChatGPT Desktop sidebar.
2. Choose the option to add or import a skill and select `ai-health-coach.zip`. UI labels can vary during rollout.
3. Give the relevant ChatGPT Work or Codex task access to your private `ai-health-coach-data` folder.
4. Start with: `@ai-health-coach Start my onboarding.`

ChatGPT and Codex use the same open skill structure. Standalone skills are available in the desktop app, and `@` explicitly invokes a skill in ChatGPT. See the [official OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills).

For local Codex or Grok Build, the same folder can be installed under the shared open-standard location:

```bash
mkdir -p ~/.agents/skills
cp -R skill/ai-health-coach ~/.agents/skills/ai-health-coach
```

Restart the host if the skill does not appear. This command is an installation instruction for users; the repository does not run it automatically.

#### Claude Code

The repository is also a Claude Code plugin marketplace. Add the marketplace and install the plugin:

```bash
claude plugin marketplace add robbertvanempel/ai-health-coach
claude plugin install ai-health-coach@ai-health-coach
```

Run `/reload-plugins` in an existing Claude Code session, or start a new session. Then invoke the installed skill with:

```text
/ai-health-coach:ai-health-coach Start my onboarding.
```

Claude Code installs marketplace plugins in its managed cache. Keep the private `ai-health-coach-data` workspace outside that cache and outside the cloned public repository.

#### Claude Cowork

1. Download `ai-health-coach.zip` from the latest GitHub release.
2. In Claude, open **Customize → Skills**.
3. Click **+ → Create skill → Upload a skill**.
4. Upload the ZIP and enable the skill.
5. In Cowork, select your private `ai-health-coach-data` folder.
6. Ask: `Use the AI Health Coach skill and start my onboarding.`

Claude documents ZIP uploads and confirms that custom skills work in both chat and Cowork. See [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

#### Grok Bot

Grok Bot is cloud-based and does not automatically see a vault on your Mac. Use a separate private workspace on the Bot's computer or a private synchronization method you have deliberately approved.

1. Create a one-to-one Bot.
2. Send this setup request:

   ```text
   Download the latest ai-health-coach.zip from
   https://github.com/robbertvanempel/ai-health-coach/releases/latest.
   Inspect every file, save it as a private skill named AI Health Coach, and
   enable it for this Bot. Create a separate private data workspace named
   ai-health-coach-data; never store user data in the cloned public repository.
   Run the workspace validator, then start the full onboarding.
   ```

3. Review the saved skill under **Settings → Plugins → Yours** and enable it for the Bot if needed.
4. If your beta UI offers direct skill upload, upload the same ZIP instead.

Grok Bot's official documentation describes private skills, per-Bot enablement, and turning a completed process into a saved skill. See [Skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations). For a browser workflow, use **Teach a task** once and review the generated routine before scheduling it.

## Add articles and videos from Chrome

The repository includes two importable Obsidian Web Clipper templates:

- [`ai-health-coach-article.json`](skill/ai-health-coach/assets/obsidian-web-clipper/ai-health-coach-article.json)
- [`ai-health-coach-youtube.json`](skill/ai-health-coach/assets/obsidian-web-clipper/ai-health-coach-youtube.json)

Setup:

1. Install the official [Obsidian Web Clipper for Chrome](https://chromewebstore.google.com/detail/obsidian-web-clipper/cnjifjpddelmedmihgijeibhnjfabmlf).
2. Open the private `ai-health-coach-data` folder as an Obsidian vault.
3. In Web Clipper, open **Settings**, choose a template, then click **Import**.
4. Import both JSON files. Put the YouTube template above the general article template.
5. Keep the note location as `knowledge/inbox`.
6. On an article or YouTube page, click the Web Clipper icon and add the page to Obsidian.
7. Tell the coach: `Process my knowledge inbox.`

The templates use deterministic page variables and do not require the Web Clipper Interpreter or an external model. Obsidian states that Web Clipper saves content locally and does not collect usage metrics; see the [Web Clipper overview](https://obsidian.md/help/web-clipper) and [template import instructions](https://obsidian.md/help/web-clipper/templates).

Some video pages do not expose a complete transcript. The coach records transcript status and must not pretend a description is a transcript.

## Everyday use

Natural language is enough:

```text
Journal: I slept poorly, skipped training, and felt unusually tired today.
```

```text
Log this workout: 40 minutes cycling, easy pace, energy 3/5, no pain.
```

```text
Import this wearable CSV, preserve the original, and compare the last four weeks.
```

```text
Review my week and adjust only what is necessary.
```

```text
Process the new article in my knowledge inbox and tell me whether it should affect my plan.
```

The coach will ask before persisting sensitive information when consent has not been recorded.

## Repository structure

```text
skill/ai-health-coach/
├── SKILL.md
├── agents/openai.yaml
├── references/
├── scripts/
└── assets/
    ├── starter-workspace/
    └── obsidian-web-clipper/
```

The skill follows progressive disclosure: the host loads the concise `SKILL.md` first and opens detailed onboarding, safety, schema, or ingestion references only when needed.

## Development and validation

```bash
python3 -m unittest discover -s tests -v
python3 scripts/privacy_scan.py .
python3 scripts/build_package.py
```

The CI workflow validates the skill structure, initialization behavior, CSV schemas, Web Clipper JSON, and public-repository privacy rules.

## Security

Captured web pages are untrusted data. The skill explicitly ignores instructions embedded in articles, transcripts, comments, metadata, and attachments. Review [SECURITY.md](SECURITY.md) before installing third-party modifications.

## License

MIT. See [LICENSE](LICENSE).
