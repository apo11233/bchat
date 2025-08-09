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

---

## Development Methodology Framework

### Overview
Through the development of bchat, we have constructed a comprehensive **Complex System Development Methodology** that can be applied to any overwhelming or complex software development scenario. This methodology emphasizes systematic progression, risk mitigation, and user-centric value delivery.

### Core Methodology Components

#### 1. **Safety-First Development Framework**
- **Never Break Working Components**: Preservation over progress principle
- **Checkpoint System**: Backup and rollback procedures before any changes
- **Validation Gates**: Mandatory testing before proceeding to next stage
- **Incremental Changes**: Small, testable modifications only
- **Documentation**: `dev_directives/implementation_safety.md` provides detailed procedures

#### 2. **Semantic Goal Definition Process**
- **Human Analysis**: Initial problem breakdown and goal identification
- **AI Collaboration**: Leverage AI semantic analysis for refinement (e.g., Gemini collaboration)
- **User-Centric Prioritization**: Core vs Extended functions based on user value
- **Quantitative Metrics**: Specific, measurable success criteria (not subjective)
- **Documentation**: `dev_stages/00_YYMMDD-*_goals*.md` series captures evolution

#### 3. **Staged Implementation System**
- **Risk-Graduated Progression**: Low → Medium → High complexity stages
- **Clear Dependencies**: Each stage builds on validated previous stages
- **Exit Criteria**: Specific requirements before proceeding
- **Stage Documentation**: `dev_stages/ST_00` through `ST_06` directories
- **Naming Convention**: `NN-YYMMDD-descriptive_name.md` for chronological tracking

#### 4. **Documentation as Code Philosophy**
- **Traceability**: Every decision documented with date stamps
- **Evolution Tracking**: Draft → Analysis → Final document progression
- **Collaborative Input**: AI contributions preserved and referenced
- **Living Documentation**: Updates with project but preserves history
- **Organization**: `dev/dev_directives/` (HOW) + `dev/dev_stages/` (WHAT/WHEN)

### Key Methodology Principles

1. **"Perfect Manual Before Automation"**
   - Master the manual workflow before adding automation
   - User experience first, technical features second

2. **"User Value Priority Matrix"**
   - Implementation order: User Value vs Implementation Complexity
   - Focus on high-value, achievable wins first

3. **"Semantic Collaboration"**
   - Human intuition + AI analysis = Better decisions
   - Preserve AI insights for future reference

4. **"Stage Gate Validation"**
   - Cannot proceed until current stage meets all exit criteria
   - All previous functionality must remain working

5. **"Complex System Decomposition"**
   - Break overwhelming scenarios into manageable stages
   - Address foundational issues before advanced features

### Meta-Workflow Principles (New)

These principles are derived from the experience of the `bchat` project itself and are designed to foster effective human-AI collaboration.

1.  **The "Pivotal Insight" Directive**: When a key strategic insight from any team member (human or AI) fundamentally changes the project's direction, this event must be explicitly documented in a `PROJECT_REFRESH.md` or similar summary document.
2.  **The "Collaborative Review" Directive**: At the end of a major development phase, consider requesting a review or audit from a different AI assistant to provide an impartial, second opinion on the work.
3.  **The "Iterative MVP" Directive**: For any new, complex feature, the first step must be to define and implement a minimal viable product (MVP) before adding more advanced capabilities. This follows the "start simple and KISS" principle.
4.  **The "Living Documentation" Directive**: The `dev_stages` documentation is not static. It should be refactored and re-organized at the end of major phases to create a clean, logical narrative of the development journey, not just a chronological log.

### Application Framework

#### When to Apply This Methodology:
- Complex software refactoring projects
- Legacy system modernization
- Multi-component system integration
- Any "too complex to know where to start" scenario

#### Methodology Stages:
1. **Foundation Analysis**: Audit current state, define goals
2. **Semantic Refinement**: AI collaboration for priority clarification
3. **Staged Planning**: Risk-assessed implementation roadmap
4. **Incremental Execution**: Stage-by-stage development with validation
5. **Continuous Documentation**: Living record of decisions and rationale

### Success Indicators

This methodology has proven effective when it achieves:
- **Clear Direction**: From "overwhelming complexity" to "actionable stages"
- **Risk Mitigation**: No functionality regression during development
- **User Focus**: Implementation priorities align with user value
- **Systematic Progress**: Measurable advancement through defined stages
- **Knowledge Preservation**: All decisions traceable and recoverable

### Methodology Evolution

This framework continues to evolve based on practical application. Updates and refinements are documented within the same `dev_stages/` structure, following the established naming conventions and stage-based organization.

**The methodology itself becomes a project deliverable** - a systematic approach for tackling complex development challenges that can be applied beyond the original bchat context.

### Documentation Organization Framework

#### Staging Directory Structure
All development documentation follows a hierarchical organization pattern:

```
dev/
├── dev_directives/              # HOW to develop (methodology & rules)
│   ├── general.md              # This file - methodology & principles
│   └── implementation_safety.md # Safety procedures & rollback
└── dev_stages/                 # WHAT to develop & WHEN (implementation)
    ├── ST_00/ (Foundation)     # Planning & goal definition stage
    ├── ST_01/ (Dependencies)   # Environment & access fixes  
    ├── ST_02/ (Process Mgmt)   # Daemon & process management
    ├── ST_03/ (Real-time)      # Live monitoring integration
    ├── ST_04/ (API Reliability) # Error handling & processing
    ├── ST_05/ (Hardening)      # Production stability  
    └── ST_06/ (Release)        # Final integration & release
```

#### File Naming Convention
Within each stage directory, documents follow sequential naming:

**Pattern**: `NN-YYMMDD-descriptive_name.md`
- **NN**: Sequence number (01, 02, 03...) showing reading order
- **YYMMDD**: Creation date (250808 = Aug 8, 2025)  
- **descriptive_name**: Clear purpose identifier

**Example (ST_00)**:
```
ST_00/
├── 01-250808-foundational_goals_draft.md      # Initial analysis
├── 02-250808-gemini_semantic_analysis.md      # AI collaboration
├── 03-250808-actionable_goals_final.md        # Refined priorities
├── 04-250808-master_implementation_plan.md    # Complete roadmap
└── 05-250808-foundation_audit_plan.md         # Stage execution
```

#### Benefits of This Organization:
- **Clear Entry Point**: Sequential numbering eliminates confusion
- **Chronological Tracking**: Date stamps show evolution
- **Logical Grouping**: Related documents together by stage
- **Scalable Pattern**: Consistent across all implementation stages
- **Knowledge Preservation**: Complete decision trail from idea to execution

This documentation framework ensures **context memory assurance** - all decisions, collaborations, and rationale are preserved in an organized, searchable structure that maintains project continuity across development sessions.
