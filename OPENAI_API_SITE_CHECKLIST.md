# What I Need From the OpenAI API Site for Issue #3

Use the [OpenAI Platform](https://platform.openai.com/) for this checklist. This is for provider setup only. Do not place a telephone call or add the voice-bot implementation while completing Issue #3.

## Required

- [ ] Sign in to or create an OpenAI API Platform account.
- [ ] Create or select a project dedicated to the PGAI challenge.
- [ ] Add a payment method or API credits so the project can use a Realtime audio model. Realtime is not supported on the free API tier.
- [ ] Review the current Realtime pricing and approve the expected spend before purchasing credits.
- [ ] Set a low project budget or usage alert appropriate for the challenge.
- [ ] Create one project API key for local development.
- [ ] Put the key only in the ignored local environment file as `OPENAI_API_KEY`.
- [ ] Confirm that the project can access the selected Realtime audio model.
- [ ] Record the exact available model ID locally as `OPENAI_REALTIME_MODEL`.
- [ ] Confirm the project's Realtime rate limit is sufficient for one controlled call at a time.

## Model Check

The architecture currently names `gpt-realtime-2.1`. Before putting that value in the local environment file, verify that this exact model ID appears in the project's model list or Playground. If it is unavailable, do not guess or silently substitute another model. Record the available Realtime model IDs and document the reason for any architecture change.

The current official model catalog lists `gpt-realtime-2.1` as a Realtime model. Access to that exact model ID was confirmed for the PGAI project through a non-call model-list request. The primary architecture will access it through LiveKit; the backup architecture may connect through WebSocket.

## Save Privately

- [ ] API key: save only as `OPENAI_API_KEY` in the ignored local environment file.
- [ ] Selected model ID: save as `OPENAI_REALTIME_MODEL` in the ignored local environment file.
- [ ] Project name and project ID: record in private setup notes if needed for billing and usage reconciliation.
- [ ] Billing receipt or credit-purchase confirmation: save under `.local/receipts/`.
- [ ] Pricing reviewed, purchase amount, and review date: record in private setup notes.
- [ ] Usage-tier and rate-limit confirmation: record in private setup notes.

## Do Not Commit

- API keys or screenshots that reveal an API key
- Billing details or receipts
- Account, organization, or project identifiers
- Private provider URLs or exported configuration
- A populated `.env` or `.env.local` file

The repository's committed `.env.example` must continue to contain only empty placeholders:

```dotenv
OPENAI_API_KEY=
OPENAI_REALTIME_MODEL=
```

## Non-Call Validation

After local configuration, validate authentication only with a non-call account, model-list, or configuration check. Do not start a Realtime audio session and do not place a telephone call during Issue #3.

Completion means the OpenAI project is funded, the local key works, the exact Realtime model ID is confirmed, usage limits are known, and all secrets and receipts remain in ignored local storage.

## Official OpenAI Documentation

- [Developer quickstart](https://developers.openai.com/api/docs/quickstart)
- [API keys](https://platform.openai.com/api-keys)
- [Projects](https://platform.openai.com/settings/organization/projects)
- [Billing](https://platform.openai.com/settings/organization/billing/overview)
- [Usage limits](https://platform.openai.com/settings/organization/limits)
- [Usage dashboard](https://platform.openai.com/usage)
- [OpenAI model catalog](https://developers.openai.com/api/docs/models)
- [API pricing](https://developers.openai.com/api/docs/pricing)
