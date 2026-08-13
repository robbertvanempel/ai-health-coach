# Privacy

AI Health Coach is designed to keep reusable instructions public and personal data private.

## What this repository contains

- Agent instructions
- Blank workspace templates
- Local initialization and validation scripts
- Obsidian Web Clipper templates
- Synthetic test fixtures

It contains no user profiles, journal entries, real measurements, wearable exports, contact details, credentials, or personal examples.

## What may be sensitive

Health goals, symptoms, diagnoses, medication, injuries, pregnancy status, diet, body metrics, wearable data, photographs, and journal text may all be sensitive. Store only what is useful, with the user's consent, and at the minimum necessary detail.

## Public repository boundary

Never store personal data in the cloned public repository. Initialize a separate workspace. Its default `.gitignore` excludes every data-bearing directory, but ignore rules are not encryption and do not protect files from other local users, backups, malware, cloud sync, or an AI provider.

## AI platform processing

Installing the skill does not by itself upload health data. Giving an AI app access to the private workspace may transmit or process data according to that provider's product, plan, region, settings, retention, and privacy terms. Cloud-hosted agents such as Grok Bot may store the workspace on their persistent cloud computer. Review the current provider terms before adding sensitive information.

Do not assume that a consumer AI product is configured for HIPAA, GDPR, or another regulated-health-data requirement. Organizations should complete their own legal, security, and data-protection review.

## Browser capture

The included Web Clipper templates use local deterministic extraction and do not require Obsidian Interpreter. Captured pages may still include names, account-specific URLs, paywalled content, comments, or tracking parameters. Review a clipping before using or syncing it.

## User control

The coach must honor requests to:

- see what has been stored
- correct inaccurate data
- export the workspace in open Markdown and CSV formats
- stop storing a category of information
- delete identified files after confirming exact targets

Deletion from one folder does not remove copies held by backups, synchronization services, or AI providers.

## No telemetry

The included Python scripts use the standard library, make no network requests, collect no analytics, and send no telemetry.
