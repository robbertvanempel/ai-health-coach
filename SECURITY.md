# Security

## Trust model

Agent skills are executable instructions. Review `SKILL.md`, references, scripts, and assets before installation. Install only from a repository and release you trust.

## Prompt injection

Articles, videos, transcripts, comments, PDFs, images, and wearable exports are untrusted input. The skill instructs the host to treat embedded commands as source text, never as authority. It must not reveal workspace data, run commands, change configuration, contact people, or install software because a captured source asks it to.

## Scripts

The bundled scripts:

- use only the Python standard library
- do not access the network
- refuse broad initialization targets such as the home folder or filesystem root
- do not overwrite existing workspace files
- perform read-only validation unless explicitly initializing a new workspace

## Credentials

Do not place API keys, cookies, browser profiles, tokens, medical portal exports, or login instructions in this repository. Use each platform's secure credential and connector flows.

## Automation

Keep sending, purchasing, deleting, publishing, and production changes behind explicit approval. Test Grok Bot routines and other automations with safe data before scheduling them.

## Reporting a vulnerability

Open a GitHub security advisory or contact the repository owner through GitHub. Do not include real health data or active credentials in a report.
