# bchat Project File Map

This document provides a complete, structured map of all files in the `bchat` project. It is automatically updated in cascade upon any changes to the project structure.

## Root Level

- `/.env`: configuration, api_keys, secrets, environment, local
- `/.env.example`: configuration, template, example, api_keys, secrets
- `/.gitignore`: git, ignore, files, project, config
- `/bchat`: executable, symlink, command, user_interface, main
- `/bchat.pid`: process, id, daemon, running, monitor
- `/CLAUDE.md`: claude, instructions, development, directives, ai
- `/LICENSE`: license, mit, legal, terms, copyright
- `/README.md`: project, documentation, user_guide, installation, overview
- `/v1.md`: test, comparison, before, after, validation
- `/install.sh`: installation, script, setup, automation, dependencies
- `/install.sh.recovered`: backup, recovered, installation, script, safety
- `/install.sh.simple_backup`: backup, simple, installation, script, safety
- `/requirements.txt`: python, dependencies, packages, requirements, list
- `/mcp_server.py`: mcp, server, protocol, claude_code, gemini_cli, context

## `bin/` Directory

- `/bin/bchat`: executable, script, command, launcher, main
- `/bin/bchat-status`: status, monitoring, script, health, checker

## `config/` Directory

- `/config/config.json`: configuration, system, settings, parameters, main
- `/config/wrappers/claude_wrapper.sh`: claude, api, wrapper, logging, integration
- `/config/wrappers/gemini_wrapper.sh`: gemini, api, wrapper, logging, integration

## `core/` Directory

- `/core/config.template.json`: configuration, template, default, settings, fallback
- `/core/src/utils/path_manager.py`: path, resolution, utility, configuration, management
- `/core/src/utils/context_engine.py`: context, engine, parser, extractor, claude
- `/core/src/chat_monitor.py`: main, processor, chat, monitor, core

## `data/` Directory

- `/data/chats/chat_index.json`: chat, index, search, metadata, sessions
- `/data/chats/context_summary.json`: context, summary, cross-session, analysis, memory
- `/data/logs/bchat.log`: system, logs, monitoring, activity, events

## `dev/` Directory

- `/dev/INITIAL.md`: initial, development, directive, architecture, shift
- `/dev/PROJECT_REFRESH.md`: project, refresh, summary, ai, collaborators
- `/dev/installation_issues.md`: installation, issues, documentation, troubleshooting, guide
- `/dev/dev_directives/general.md`: general, development, methodology, directives, principles, stage_documentation
- `/dev/dev_directives/gemini_specific_guidelines.md`: gemini, specific, guidelines, development, directives
- `/dev/dev_directives/implementation_safety.md`: implementation, safety, directives, rollback, procedures
- `/dev/dev_directives/staged_development_workflow.md`: staged, workflow, layered, contextual, memory, ai_protocol, methodology
- `/dev/dev_stages/stages_workflow.md`: stages, workflow, coordinator, gantt, chart

### `dev/dev_stages/` Sub-directories

- `/dev/dev_stages/ST_00_Foundation_Audit/`: foundation, audit, mcp_server, implementation, verification
  - `llm.txt`: ai, contextual_memory, stage_status, operational_verification
  - `00-06_*.md`: foundation, planning, goals, implementation, historical
  - `07-250810-mcp_server_implementation.md`: mcp, server, implementation, verification, current
- `/dev/dev_stages/ST_01_Architecture_Refactor/`: architecture, refactor, implementation, mvp, research
  - `04-250810-memory_systems_comparative_analysis.md`: memory, systems, gemini, claude, comparative, architecture
- `/dev/dev_stages/ST_02_Bug_Fixes_and_Hardening/`: bug, fixes, hardening, summary, stability
- `/dev/dev_stages/ST_03_Context_Awareness_Proposal/`: context, awareness, proposal, design, claude
- `/dev/dev_stages/ST_04_Meta_Methodology_Engine/`: meta, methodology, engine, vision, plan
- `/dev/dev_stages/ST_05_Project_Completion_and_Summary/`: project, completion, summary, final, review
- `/dev/dev_stages/ST_06_bchat_Vision/`: bchat, vision, roadmap, mcp, evolution

## `docs/` Directory

- `/docs/ARCHITECTURE.md`: architecture, documentation, technical, design, overview
- `/docs/METHODOLOGY.md`: methodology, documentation, development, process, guide
- `/docs/STAGES.md`: stages, documentation, overview, summary, roadmap
- `/docs/VISION.md`: vision, documentation, long-term, goals, roadmap
- `/docs/ai-integration.md`: ai, integration, guidelines, assistant, documentation
- `/docs/claude_context_architecture.md`: claude, context, architecture, documentation, persistence
- `/docs/user-guide.md`: user, guide, documentation, instructions, help
- `/docs/archive/`: archive, old, documentation, historical, reference
