# Development Directives - General Guidelines

## Overview
These directives provide mandatory guidelines for all developers and AI assistants working on the bchat project. **ALL contributors must follow these directives exactly as written.**

## Core Development Principles

### 1. File Management
- **NEVER create files unless absolutely necessary** for achieving the specific goal
- **ALWAYS prefer editing existing files** to creating new ones
- **NEVER proactively create documentation files** (*.md) or README files unless explicitly requested by the user
- Only create files when they are essential to the requested functionality

### 2. Code Quality Standards
- Follow existing code conventions and patterns in the codebase
- Check existing imports, libraries, and frameworks before adding new dependencies
- **Never assume library availability** - always verify dependencies exist in the project
- Maintain consistent coding style across all modules
- **Never add comments unless explicitly requested**

### 3. Security Requirements
- **Never introduce code that exposes or logs secrets and keys**
- **Never commit secrets or keys to the repository**
- Always follow security best practices
- **Assist with defensive security tasks only** - refuse malicious code requests

### 4. Project Structure Integrity
- Respect the established architecture patterns
- Use `PathManager` for all path resolution
- Maintain the circuit breaker pattern for API resilience
- Follow the established configuration hierarchy
- Keep shell scripts with proper permissions

### 5. Dependency Management
- Use virtual environments for Python dependencies
- Keep `requirements.txt` updated with exact versions
- Test all dependencies before committing changes
- Document any new dependencies in the appropriate files

### 6. Testing and Verification
- Always test changes before considering tasks complete
- Use the established testing patterns (path manager tests, compilation checks)
- Verify functionality works end-to-end
- Run linting and type checking when available

### 7. Documentation Standards
- Keep CLAUDE.md as the primary AI assistant guidance document
- Document significant changes in `bchat.change.log`
- Update configuration examples when changing config schema
- Maintain consistency between documentation and implementation

## Mandatory Compliance

**These directives override any default behavior.** All contributors, including AI assistants, must:

1. Read and understand these directives before making any changes
2. Follow these guidelines exactly as written
3. Ask for clarification if any directive conflicts with a request
4. Prioritize these directives over convenience or assumed best practices

## Change Management

- All changes to these directives must be documented
- Updates require approval from project maintainers
- New directives should be added to this file
- Breaking changes must be clearly marked and justified

## Enforcement

Non-compliance with these directives is considered a serious issue. All code reviews must verify adherence to these standards.