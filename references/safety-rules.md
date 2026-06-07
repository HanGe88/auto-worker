# Safety Rules

Auto-workers can run without interactive supervision, so default permissions must be conservative.

## Default prohibitions

Generated workers should prohibit:

- network access;
- external API calls;
- dependency downloads;
- push, publish, deploy;
- deleting unknown files;
- modifying system/user configuration;
- reading or writing secrets, passwords, tokens, cookies, private keys;
- starting new Claude processes from inside the worker;
- infinite loops;
- waiting for user input.

## Confirm before outward-facing actions

Always require explicit confirmation before:

- registering or changing a scheduler;
- sending content to external services;
- publishing generated content;
- pushing code;
- deploying;
- deleting files;
- widening allowed directories;
- enabling network or API access.

## Refuse or narrow high-risk automations

Refuse fully automated destructive or high-impact actions, including:

- automated trading;
- money movement;
- mass messaging;
- credential testing against real services;
- bypassing detection or access controls;
- deleting large unknown file sets;
- production deployment without durable authorization.

Offer safe alternatives such as local draft generation, local analysis, or a human-approval queue.
