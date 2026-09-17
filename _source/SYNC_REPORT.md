# Source synchronization report

- Snapshot: `_source/llms-full.txt` (preserved; no network fetch performed).
- Snapshot SHA256: `7e9b840d86b3d2cf1b78f5ac4a5b2e1f639018b62dcf56dcdad89eaa02249ef2`
- Baseline: git commit `f1d08c53f62f54901ffe507abc15b2bf25975185`, `_source/llms-full.txt`.
- Baseline snapshot SHA256: `2d98622e4a358df33ffc4b0946500c2eb3cb459be074046d176cf9cc12ba476b`
- Source sections: **227**; baseline normalized keys: **207**.
- Added: **20**; changed: **137**; unchanged: **70**; removed: **0**.

## Comparison rules

Comparisons and previous hashes use the git baseline dump, not existing extracts. Already-present untracked extracts remain added if absent from that baseline. Existing extract bodies and their SHA256 hashes are read before any overwrite; working-tree repair results are not persisted so reruns remain stable.

Source identities normalize `.md`/`.mdx` extensions. Bodies normalize newlines and outer whitespace after removing exactly one synthetic dump suffix. Internal separators and document content are preserved. SHA256 source hashes cover those normalized UTF-8 bodies; snapshot hashes cover the original bytes.

No fetch date is inferred. Local HTML existence is recorded only as `local_file_exists`; translation freshness has not been reviewed.

## Changed pages

| Source path | Extract path |
| --- | --- |
| `website/docs/developer-guide/acp-internals.md` | `_source/pages/developer-guide__acp-internals.md` |
| `website/docs/developer-guide/adding-platform-adapters.md` | `_source/pages/developer-guide__adding-platform-adapters.md` |
| `website/docs/developer-guide/adding-providers.md` | `_source/pages/developer-guide__adding-providers.md` |
| `website/docs/developer-guide/adding-tools.md` | `_source/pages/developer-guide__adding-tools.md` |
| `website/docs/developer-guide/agent-loop.md` | `_source/pages/developer-guide__agent-loop.md` |
| `website/docs/developer-guide/architecture.md` | `_source/pages/developer-guide__architecture.md` |
| `website/docs/developer-guide/codebase-ownership.md` | `_source/pages/developer-guide__codebase-ownership.md` |
| `website/docs/developer-guide/context-compression-and-caching.md` | `_source/pages/developer-guide__context-compression-and-caching.md` |
| `website/docs/developer-guide/context-engine-plugin.md` | `_source/pages/developer-guide__context-engine-plugin.md` |
| `website/docs/developer-guide/cron-internals.md` | `_source/pages/developer-guide__cron-internals.md` |
| `website/docs/developer-guide/desktop-plugin-sdk.md` | `_source/pages/developer-guide__desktop-plugin-sdk.md` |
| `website/docs/developer-guide/egress-internals.md` | `_source/pages/developer-guide__egress-internals.md` |
| `website/docs/developer-guide/extending-the-cli.md` | `_source/pages/developer-guide__extending-the-cli.md` |
| `website/docs/developer-guide/gateway-internals.md` | `_source/pages/developer-guide__gateway-internals.md` |
| `website/docs/developer-guide/image-gen-provider-plugin.md` | `_source/pages/developer-guide__image-gen-provider-plugin.md` |
| `website/docs/developer-guide/memory-provider-plugin.md` | `_source/pages/developer-guide__memory-provider-plugin.md` |
| `website/docs/developer-guide/model-provider-plugin.md` | `_source/pages/developer-guide__model-provider-plugin.md` |
| `website/docs/developer-guide/plugins/index.md` | `_source/pages/developer-guide__plugins__index.md` |
| `website/docs/developer-guide/programmatic-integration.md` | `_source/pages/developer-guide__programmatic-integration.md` |
| `website/docs/developer-guide/prompt-assembly.md` | `_source/pages/developer-guide__prompt-assembly.md` |
| `website/docs/developer-guide/provider-runtime.md` | `_source/pages/developer-guide__provider-runtime.md` |
| `website/docs/developer-guide/secret-source-plugin.md` | `_source/pages/developer-guide__secret-source-plugin.md` |
| `website/docs/developer-guide/session-storage.md` | `_source/pages/developer-guide__session-storage.md` |
| `website/docs/developer-guide/tools-runtime.md` | `_source/pages/developer-guide__tools-runtime.md` |
| `website/docs/developer-guide/trajectory-format.md` | `_source/pages/developer-guide__trajectory-format.md` |
| `website/docs/developer-guide/video-gen-provider-plugin.md` | `_source/pages/developer-guide__video-gen-provider-plugin.md` |
| `website/docs/developer-guide/web-search-provider-plugin.md` | `_source/pages/developer-guide__web-search-provider-plugin.md` |
| `website/docs/developer-guide/worktree-ui-dev.md` | `_source/pages/developer-guide__worktree-ui-dev.md` |
| `website/docs/getting-started/installation.md` | `_source/pages/getting-started__installation.md` |
| `website/docs/getting-started/nix-setup.md` | `_source/pages/getting-started__nix-setup.md` |
| `website/docs/getting-started/quickstart.md` | `_source/pages/getting-started__quickstart.md` |
| `website/docs/getting-started/termux.md` | `_source/pages/getting-started__termux.md` |
| `website/docs/getting-started/updating.md` | `_source/pages/getting-started__updating.md` |
| `website/docs/guides/automate-with-cron.md` | `_source/pages/guides__automate-with-cron.md` |
| `website/docs/guides/aws-bedrock.md` | `_source/pages/guides__aws-bedrock.md` |
| `website/docs/guides/cron-troubleshooting.md` | `_source/pages/guides__cron-troubleshooting.md` |
| `website/docs/guides/delegation-patterns.md` | `_source/pages/guides__delegation-patterns.md` |
| `website/docs/guides/desktop-native-signin.md` | `_source/pages/guides__desktop-native-signin.md` |
| `website/docs/guides/google-gemini.md` | `_source/pages/guides__google-gemini.md` |
| `website/docs/guides/google-vertex.md` | `_source/pages/guides__google-vertex.md` |
| `website/docs/guides/local-llm-on-mac.md` | `_source/pages/guides__local-llm-on-mac.md` |
| `website/docs/guides/local-ollama-setup.md` | `_source/pages/guides__local-ollama-setup.md` |
| `website/docs/guides/migrate-from-openclaw.md` | `_source/pages/guides__migrate-from-openclaw.md` |
| `website/docs/guides/oauth-over-ssh.md` | `_source/pages/guides__oauth-over-ssh.md` |
| `website/docs/guides/tips.md` | `_source/pages/guides__tips.md` |
| `website/docs/integrations/index.md` | `_source/pages/integrations__index.md` |
| `website/docs/integrations/nous-portal.md` | `_source/pages/integrations__nous-portal.md` |
| `website/docs/integrations/providers.md` | `_source/pages/integrations__providers.md` |
| `website/docs/reference/cli-commands.md` | `_source/pages/reference__cli-commands.md` |
| `website/docs/reference/cli-symbols.md` | `_source/pages/reference__cli-symbols.md` |
| `website/docs/reference/environment-variables.md` | `_source/pages/reference__environment-variables.md` |
| `website/docs/reference/faq.md` | `_source/pages/reference__faq.md` |
| `website/docs/reference/mcp-config-reference.md` | `_source/pages/reference__mcp-config-reference.md` |
| `website/docs/reference/model-catalog.md` | `_source/pages/reference__model-catalog.md` |
| `website/docs/reference/optional-skills-catalog.md` | `_source/pages/reference__optional-skills-catalog.md` |
| `website/docs/reference/profile-commands.md` | `_source/pages/reference__profile-commands.md` |
| `website/docs/reference/skills-catalog.md` | `_source/pages/reference__skills-catalog.md` |
| `website/docs/reference/slash-commands.md` | `_source/pages/reference__slash-commands.md` |
| `website/docs/reference/tools-reference.md` | `_source/pages/reference__tools-reference.md` |
| `website/docs/reference/toolsets-reference.md` | `_source/pages/reference__toolsets-reference.md` |
| `website/docs/user-guide/bot-mode.md` | `_source/pages/user-guide__bot-mode.md` |
| `website/docs/user-guide/checkpoints-and-rollback.md` | `_source/pages/user-guide__checkpoints-and-rollback.md` |
| `website/docs/user-guide/cli.md` | `_source/pages/user-guide__cli.md` |
| `website/docs/user-guide/configuration.md` | `_source/pages/user-guide__configuration.md` |
| `website/docs/user-guide/configuring-models.md` | `_source/pages/user-guide__configuring-models.md` |
| `website/docs/user-guide/desktop.md` | `_source/pages/user-guide__desktop.md` |
| `website/docs/user-guide/docker.md` | `_source/pages/user-guide__docker.md` |
| `website/docs/user-guide/features/acp.md` | `_source/pages/user-guide__features__acp.md` |
| `website/docs/user-guide/features/api-server.md` | `_source/pages/user-guide__features__api-server.md` |
| `website/docs/user-guide/features/batch-processing.md` | `_source/pages/user-guide__features__batch-processing.md` |
| `website/docs/user-guide/features/browser.md` | `_source/pages/user-guide__features__browser.md` |
| `website/docs/user-guide/features/built-in-plugins.md` | `_source/pages/user-guide__features__built-in-plugins.md` |
| `website/docs/user-guide/features/code-execution.md` | `_source/pages/user-guide__features__code-execution.md` |
| `website/docs/user-guide/features/computer-use.md` | `_source/pages/user-guide__features__computer-use.md` |
| `website/docs/user-guide/features/context-files.md` | `_source/pages/user-guide__features__context-files.md` |
| `website/docs/user-guide/features/credential-pools.md` | `_source/pages/user-guide__features__credential-pools.md` |
| `website/docs/user-guide/features/cron.md` | `_source/pages/user-guide__features__cron.md` |
| `website/docs/user-guide/features/curator.md` | `_source/pages/user-guide__features__curator.md` |
| `website/docs/user-guide/features/delegation.md` | `_source/pages/user-guide__features__delegation.md` |
| `website/docs/user-guide/features/fallback-providers.md` | `_source/pages/user-guide__features__fallback-providers.md` |
| `website/docs/user-guide/features/goals.md` | `_source/pages/user-guide__features__goals.md` |
| `website/docs/user-guide/features/heartbeat.md` | `_source/pages/user-guide__features__heartbeat.md` |
| `website/docs/user-guide/features/honcho.md` | `_source/pages/user-guide__features__honcho.md` |
| `website/docs/user-guide/features/hooks.md` | `_source/pages/user-guide__features__hooks.md` |
| `website/docs/user-guide/features/image-generation.md` | `_source/pages/user-guide__features__image-generation.md` |
| `website/docs/user-guide/features/kanban.md` | `_source/pages/user-guide__features__kanban.md` |
| `website/docs/user-guide/features/kanban-worker-lanes.md` | `_source/pages/user-guide__features__kanban-worker-lanes.md` |
| `website/docs/user-guide/features/loops.md` | `_source/pages/user-guide__features__loops.md` |
| `website/docs/user-guide/features/lsp.md` | `_source/pages/user-guide__features__lsp.md` |
| `website/docs/user-guide/features/mcp.md` | `_source/pages/user-guide__features__mcp.md` |
| `website/docs/user-guide/features/memory.md` | `_source/pages/user-guide__features__memory.md` |
| `website/docs/user-guide/features/memory-providers.md` | `_source/pages/user-guide__features__memory-providers.md` |
| `website/docs/user-guide/features/mixture-of-agents.md` | `_source/pages/user-guide__features__mixture-of-agents.md` |
| `website/docs/user-guide/features/personality.md` | `_source/pages/user-guide__features__personality.md` |
| `website/docs/user-guide/features/plugins.md` | `_source/pages/user-guide__features__plugins.md` |
| `website/docs/user-guide/features/provider-routing.md` | `_source/pages/user-guide__features__provider-routing.md` |
| `website/docs/user-guide/features/skills.md` | `_source/pages/user-guide__features__skills.md` |
| `website/docs/user-guide/features/skins.md` | `_source/pages/user-guide__features__skins.md` |
| `website/docs/user-guide/features/tool-gateway.md` | `_source/pages/user-guide__features__tool-gateway.md` |
| `website/docs/user-guide/features/tool-search.md` | `_source/pages/user-guide__features__tool-search.md` |
| `website/docs/user-guide/features/tools.md` | `_source/pages/user-guide__features__tools.md` |
| `website/docs/user-guide/features/tts.md` | `_source/pages/user-guide__features__tts.md` |
| `website/docs/user-guide/features/vision.md` | `_source/pages/user-guide__features__vision.md` |
| `website/docs/user-guide/features/voice-mode.md` | `_source/pages/user-guide__features__voice-mode.md` |
| `website/docs/user-guide/features/wake-word.md` | `_source/pages/user-guide__features__wake-word.md` |
| `website/docs/user-guide/features/web-dashboard.md` | `_source/pages/user-guide__features__web-dashboard.md` |
| `website/docs/user-guide/features/web-search.md` | `_source/pages/user-guide__features__web-search.md` |
| `website/docs/user-guide/import-from-other-agents.md` | `_source/pages/user-guide__import-from-other-agents.md` |
| `website/docs/user-guide/messaging/a2a.md` | `_source/pages/user-guide__messaging__a2a.md` |
| `website/docs/user-guide/messaging/buzz.md` | `_source/pages/user-guide__messaging__buzz.md` |
| `website/docs/user-guide/messaging/discord.md` | `_source/pages/user-guide__messaging__discord.md` |
| `website/docs/user-guide/messaging/email.md` | `_source/pages/user-guide__messaging__email.md` |
| `website/docs/user-guide/messaging/feishu.md` | `_source/pages/user-guide__messaging__feishu.md` |
| `website/docs/user-guide/messaging/google_chat.md` | `_source/pages/user-guide__messaging__google_chat.md` |
| `website/docs/user-guide/messaging/index.md` | `_source/pages/user-guide__messaging__index.md` |
| `website/docs/user-guide/messaging/irc.md` | `_source/pages/user-guide__messaging__irc.md` |
| `website/docs/user-guide/messaging/line.md` | `_source/pages/user-guide__messaging__line.md` |
| `website/docs/user-guide/messaging/matrix.md` | `_source/pages/user-guide__messaging__matrix.md` |
| `website/docs/user-guide/messaging/photon.md` | `_source/pages/user-guide__messaging__photon.md` |
| `website/docs/user-guide/messaging/relay.md` | `_source/pages/user-guide__messaging__relay.md` |
| `website/docs/user-guide/messaging/signal.md` | `_source/pages/user-guide__messaging__signal.md` |
| `website/docs/user-guide/messaging/slack.md` | `_source/pages/user-guide__messaging__slack.md` |
| `website/docs/user-guide/messaging/telegram.md` | `_source/pages/user-guide__messaging__telegram.md` |
| `website/docs/user-guide/messaging/webhooks.md` | `_source/pages/user-guide__messaging__webhooks.md` |
| `website/docs/user-guide/messaging/wecom.md` | `_source/pages/user-guide__messaging__wecom.md` |
| `website/docs/user-guide/messaging/whatsapp.md` | `_source/pages/user-guide__messaging__whatsapp.md` |
| `website/docs/user-guide/messaging/whatsapp-cloud.md` | `_source/pages/user-guide__messaging__whatsapp-cloud.md` |
| `website/docs/user-guide/messaging/yuanbao.md` | `_source/pages/user-guide__messaging__yuanbao.md` |
| `website/docs/user-guide/multi-connection-desktop.md` | `_source/pages/user-guide__multi-connection-desktop.md` |
| `website/docs/user-guide/multi-profile-gateways.md` | `_source/pages/user-guide__multi-profile-gateways.md` |
| `website/docs/user-guide/profile-distributions.md` | `_source/pages/user-guide__profile-distributions.md` |
| `website/docs/user-guide/profiles.md` | `_source/pages/user-guide__profiles.md` |
| `website/docs/user-guide/secrets/onepassword.md` | `_source/pages/user-guide__secrets__onepassword.md` |
| `website/docs/user-guide/security.md` | `_source/pages/user-guide__security.md` |
| `website/docs/user-guide/sessions.md` | `_source/pages/user-guide__sessions.md` |
| `website/docs/user-guide/tui.md` | `_source/pages/user-guide__tui.md` |
| `website/docs/user-guide/windows-native.md` | `_source/pages/user-guide__windows-native.md` |

## Added pages

- `website/docs/developer-guide/billing-lifecycle.md` → `_source/pages/developer-guide__billing-lifecycle.md`
- `website/docs/developer-guide/chronos-managed-cron-contract.md` → `_source/pages/developer-guide__chronos-managed-cron-contract.md`
- `website/docs/developer-guide/cli-internals.md` → `_source/pages/developer-guide__cli-internals.md`
- `website/docs/developer-guide/completion-backlog-delivery.md` → `_source/pages/developer-guide__completion-backlog-delivery.md`
- `website/docs/developer-guide/gateway-monitoring.md` → `_source/pages/developer-guide__gateway-monitoring.md`
- `website/docs/developer-guide/gateway-session-lifecycle.md` → `_source/pages/developer-guide__gateway-session-lifecycle.md`
- `website/docs/developer-guide/micro-compaction.md` → `_source/pages/developer-guide__micro-compaction.md`
- `website/docs/developer-guide/middleware.md` → `_source/pages/developer-guide__middleware.md`
- `website/docs/developer-guide/multiplexing-gateway.md` → `_source/pages/developer-guide__multiplexing-gateway.md`
- `website/docs/developer-guide/observer-hooks.md` → `_source/pages/developer-guide__observer-hooks.md`
- `website/docs/developer-guide/relay-connector-contract.md` → `_source/pages/developer-guide__relay-connector-contract.md`
- `website/docs/developer-guide/relay-shared-metrics.md` → `_source/pages/developer-guide__relay-shared-metrics.md`
- `website/docs/developer-guide/state-db-recovery.md` → `_source/pages/developer-guide__state-db-recovery.md`
- `website/docs/developer-guide/streaming-tts.md` → `_source/pages/developer-guide__streaming-tts.md`
- `website/docs/developer-guide/terminal-environment-plugin.md` → `_source/pages/developer-guide__terminal-environment-plugin.md`
- `website/docs/user-guide/egress/network-isolation.md` → `_source/pages/user-guide__egress__network-isolation.md`
- `website/docs/user-guide/features/credential-vault.md` → `_source/pages/user-guide__features__credential-vault.md`
- `website/docs/user-guide/features/kanban-multi-gateway.md` → `_source/pages/user-guide__features__kanban-multi-gateway.md`
- `website/docs/user-guide/features/plugin-catalog.md` → `_source/pages/user-guide__features__plugin-catalog.md`
- `website/docs/user-guide/local-models.md` → `_source/pages/user-guide__local-models.md`

## Removed pages

None.
