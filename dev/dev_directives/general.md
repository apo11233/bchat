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
- **ALWAYS search and use existing stage directories** - DO NOT CREATE new stages without explicit user approval
- **MANDATORY**: Use existing `/dev/dev_stages/ST_XX_*` directories for all documentation and work

### 4.5. Base URL/Absolute Path Architecture (MANDATORY)

**Triggered By**: Path resolution failures in MCP test suite (`../../mcp_server.py` → `../../../mcp_server.py`)

#### Core Requirements
- **NEVER use relative paths in production code** (../../../file.py)
- **ALWAYS define BASE_DIR at module level** using `os.path.dirname(os.path.abspath(__file__))`
- **ALWAYS use os.path.join()** for cross-platform path construction
- **ALWAYS use os.path.abspath()** for final path resolution

#### Mandatory Implementation Pattern
```python
import os

# Define base directory - MANDATORY at module top level
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct paths using os.path.join - NEVER hardcoded relative paths
target_file = os.path.join(BASE_DIR, 'subdir', 'target_file.py')
target_path = os.path.abspath(target_file)  # Resolve to absolute path
command = ["python3", target_path, "--args"]
```

#### Architecture Benefits
- **Location Independence**: Code works regardless of execution context
- **Structure Resilience**: Paths remain valid during project reorganization  
- **Cross-Platform Compatibility**: `os.path.join()` handles different OS separators
- **Maintenance Simplicity**: Single BASE_DIR update handles structure changes
- **Testing Reliability**: Tests work from any execution directory

#### Quality Assurance Requirements
**Code Review Checklist**:
- ✅ BASE_DIR definition at module level
- ✅ `os.path.join()` usage for path construction
- ✅ `os.path.abspath()` for final resolution
- ❌ **Zero tolerance for relative path strings**

**Testing Standards**:
- ✅ Work from any execution directory
- ✅ Use BASE_DIR pattern for file location  
- ✅ Validate cross-platform compatibility
- ✅ Test path resolution independently of context

#### Prohibited Practices
- Direct relative paths: `"../../file.py"`
- Hardcoded separators: `"../dir/file.py"`  
- String concatenation: `path + "/file.py"`
- Platform-specific paths: `"..\\windows\\path"`

#### Enforcement & Exception Policy
- **ENFORCEMENT**: 🔥 **Any AI assistant using relative paths will have their virtual home directory set on fire** 🔥
- **RATIONALE**: Relative paths break when files move, directory structure changes, or execution context shifts
- **EXCEPTION**: Only `PathManager` class is exempt as it handles project-wide path resolution
- **VALIDATION**: MCP test suite demonstrates 17/18 tests passing with proper BASE_DIR implementation

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
3. **FOLLOW** the complete workflow protocol in `dev_directives/staged_development_workflow.md`
4. Ask for clarification if any directive conflicts with a request
5. Prioritize these directives over convenience or assumed best practices

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

1.  **The KISS Principle (Keep It Simple & Stable)** (New)
    *   **Functionality and Stability First**: The primary goal of any initial MVP is to create a simple, robust, and stable system that works flawlessly.
    *   **Simplicity of Code**: Functions should be short, well-commented, and easy to understand.
    *   **Robustness over Features**: The system should be designed to be resilient to changes in library versions and to avoid absolute, brittle dependencies.
    *   **Incremental Iterations**: It is always preferable to add small, incremental improvements in each iteration, rather than trying to implement large, complex stages at once. This facilitates easier validation and ensures the stability of the system.

2. **"Perfect Manual Before Automation"**
   - Master the manual workflow before adding automation
   - User experience first, technical features second

3. **"User Value Priority Matrix"**
   - Implementation order: User Value vs Implementation Complexity
   - Focus on high-value, achievable wins first

4. **"Semantic Collaboration"**
   - Human intuition + AI analysis = Better decisions
   - Preserve AI insights for future reference

5. **"Stage Gate Validation"**
   - Cannot proceed until current stage meets all exit criteria
   - All previous functionality must remain working

6. **"Complex System Decomposition"**
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

### Stage Work Documentation Protocol

When completing work within any development stage, follow this mandatory documentation pattern:

#### **File Naming Convention**
- **Pattern**: `NN-YYMMDD-descriptive_name.md`
- **NN**: Sequential number continuing from existing stage files (07, 08, 09...)
- **YYMMDD**: Date stamp in 6-digit format (250810 = Aug 10, 2025)
- **descriptive_name**: Clear identifier of work completed (underscore_separated)

#### **File Location**
- **Always within the appropriate stage directory**: `/dev/dev_stages/ST_XX_Stage_Name/`
- **Never create separate progress or status files outside the stage structure**
- **Follow existing numbering sequence within each stage**

#### **Example Implementation**
```
ST_00_Foundation_Audit/
├── 00_foundation_audit_plan.md          # Existing work
├── 01_audit_report.md                   # Existing work  
├── 02_foundational_goals_draft.md       # Existing work
├── 03_gemini_semantic_analysis.md       # Existing work
├── 04_actionable_goals_final.md         # Existing work
├── 05_master_implementation_plan.md     # Existing work
├── 06_architectural_shift_proposal.md   # Existing work
└── 07-250810-mcp_server_implementation.md  # NEW WORK ✅
```

#### **Documentation Requirements**
Each stage work document must include:
1. **Date and Stage identification**
2. **Implementation summary and results**  
3. **Files modified or created**
4. **Success metrics and testing results**
5. **Next steps or lessons learned**

#### **SSOT Principle**
- **Single Source of Truth**: All stage work documented within stage directories
- **No duplicate documentation**: Avoid creating separate progress files
- **Sequential continuity**: Maintain chronological order within stages
- **Searchable history**: Preserve complete decision trail

This protocol ensures systematic organization, prevents documentation duplication, and maintains clear project progression tracking across all development stages.

### Stage Work Completion Analysis Protocol

When documenting completed work within any stage, include a mandatory **"Relationship to Previous Stage Work"** section that provides historical context and continuity analysis.

#### **Historical Context Documentation Requirements**

**Format**: Add this section to every stage work completion document:

```markdown
## Relationship to Previous [STAGE_NAME] Work

### Relevant Foundation Documents (Still Applicable)
- **NN_filename.md** - Brief description of continued relevance ✅
- **NN_filename.md** - Brief description of continued relevance ✅

### Superseded Approaches (Historical Reference)
- **NN_filename.md** - Brief description of approach/decision
  - **Status**: Why this approach was abandoned or superseded
  - **Decision**: What approach was chosen instead and why
  - **Historical Value**: What value this document retains for future reference

### Implementation Alignment
This [current work] **fulfills/advances the objectives** defined in previous documents:
- **[Previous Goal/Requirement]**: ✅ How current work addresses this
- **[Previous Goal/Requirement]**: ✅ How current work addresses this
- **[Architecture/System Requirements]**: ✅ How current work aligns

**Conclusion**: Clear statement of how current work builds upon, supersedes, or evolves previous stage efforts.
```

#### **Methodology Benefits**

**Context Preservation**: Maintains clear linkage between all stage work and decisions  
**Decision Traceability**: Shows evolution of approaches and why changes were made  
**Knowledge Continuity**: Prevents loss of historical reasoning and alternative approaches  
**Stage Coherence**: Ensures each stage builds logically on previous work  
**Onboarding Efficiency**: New team members can understand complete stage evolution  

#### **Implementation Guidelines**

1. **Review all previous stage files** before documenting new work
2. **Categorize previous work** as "Still Applicable" vs "Superseded"  
3. **Explain superseded decisions** - why approaches were abandoned and what replaced them
4. **Show alignment** - how current work fulfills original stage objectives
5. **Maintain historical value** - acknowledge worth of abandoned approaches for future reference

#### **Stage Evolution Tracking**

This methodology enables systematic tracking of how each stage evolves:
- **Foundation → Implementation** - Clear progression from planning to execution
- **Alternative Approaches** - Documented decision points and rationale  
- **Requirement Fulfillment** - Verification that original objectives are met
- **Knowledge Preservation** - Complete decision trail for future stages

**This analysis protocol is mandatory for all stage completion documentation and forms a core component of the bchat development methodology framework.**

### Operational Verification and Documentation Protocol

When completing any stage implementation, mandatory verification and documentation steps must be followed to ensure system reliability and knowledge preservation.

#### **Implementation Verification Requirements**

**Live System Testing**: After implementation completion, conduct comprehensive verification of all delivered functionality:

1. **Operational Status Verification**
   - Test all implemented components for current functionality
   - Verify system stability over extended periods
   - Confirm integration points are working correctly
   - Validate protocol compliance and standard conformance

2. **Functional Testing Documentation**
   - Record actual test commands and their responses
   - Document verification methods for each component
   - Create reproducible test sequences for future validation
   - Capture integration status with external systems

3. **Production Readiness Assessment**
   - Evaluate stability under operational conditions
   - Confirm reliability of all API endpoints and interfaces
   - Validate integration capabilities with target systems
   - Assess extensibility and enhancement readiness

#### **Dual Documentation Standard**

**Stage Work Document** (`NN-YYMMDD-descriptive_name.md`):
```markdown
## Live Verification Status (Updated YYYY-MM-DD)

### **Current Operational Status**
[Detailed verification with actual commands and responses]

### **Real-Time Validation Results**  
[Comprehensive testing table with methods and results]

### **Production Readiness Assessment**
[Stability, reliability, integration, and compliance evaluation]

### **Ready for Real-World Usage**
[Usage readiness, extension possibilities, deployment status]
```

**Stage llm.txt** (AI Assistant Context):
```markdown
## Current Operational Verification (YYYY-MM-DD)

### **Live System Status - VERIFIED ✅**
[Summary of operational status and key capabilities]

### **Real-Time Test Results**
[Essential verification facts in bullet format]

### **Production Readiness Confirmed**
[Key readiness indicators with checkmarks]

[Concise readiness statement for next stage advancement]
```

#### **Verification Documentation Standards**

**Command Documentation**: Include actual commands with responses
```bash
$ command_executed
actual_output_received
```

**Status Tables**: Systematic component verification
| Component | Status | Verification Method | Result |
|-----------|--------|-------------------|---------|
| [Component] | ✅ Status | [Method] | [Result] |

**Integration Confirmation**: External system connection validation
```bash
$ integration_test_command
✓ Connected / ✗ Failed status
```

#### **Mandatory Verification Sequence**

1. **Complete Implementation** - Finish all planned functionality
2. **Conduct Live Testing** - Test all components in operational environment  
3. **Document Verification** - Record testing in stage work document
4. **Update llm.txt Context** - Summarize verification status for AI assistants
5. **Confirm Production Readiness** - Assess deployment and advancement readiness
6. **Establish Stage Completion** - Mark stage as verified and ready for progression

#### **Quality Assurance Benefits**

**Operational Confidence**: Verified systems provide reliable foundation for subsequent stages  
**Reproducible Validation**: Documented test commands enable future verification cycles  
**Integration Assurance**: Confirmed external connections prevent advancement blockers  
**Knowledge Continuity**: Complete verification context preserved for future development  
**Production Readiness**: Systematic assessment ensures deployment capability  

#### **Stage Advancement Gateway**

No stage may be considered complete without:
- ✅ **Operational verification** of all implemented functionality
- ✅ **Documentation** of verification results in both stage document and llm.txt
- ✅ **Production readiness assessment** with explicit capability confirmation
- ✅ **Integration validation** with all required external systems

**This operational verification protocol is mandatory for all stage completions and ensures systematic quality assurance across the entire bchat development methodology framework.**

### Stage Directory Cleanup and Maintenance Protocol

When completing stage work, mandatory cleanup procedures must be followed to maintain organized, SSOT-compliant project structure.

#### **Stage Directory Audit Requirements**

After stage completion, conduct systematic review of stage directory contents:

1. **Essential File Identification**
   - **Documentation**: Keep all NN-YYMMDD-descriptive_name.md files (chronological work record)
   - **AI Context**: Maintain llm.txt with current operational verification status
   - **Historical Value**: Preserve files containing decisions, analysis, and implementation rationale

2. **Obsolete File Detection**
   - **Outdated Scripts**: Remove scripts referencing non-existent files or superseded functionality
   - **Broken Utilities**: Eliminate tools that reference old architecture or missing dependencies
   - **Backup Directories**: Remove backup folders duplicating git-managed code or containing outdated versions
   - **Virtual Environments**: Clean up stage-specific venvs that duplicate project-level dependencies

3. **File Relevance Assessment**
   - **Current System**: Does file reference current implementation or outdated architecture?
   - **Path Accuracy**: Do file paths and references match actual project structure?
   - **Functional Value**: Does script/tool provide value not available through git or current tools?
   - **SSOT Compliance**: Does file duplicate information available elsewhere in better form?

#### **Systematic Cleanup Procedure**

**Step 1: Documentation Review**
```bash
# Review all files in stage directory
ls -la /dev/dev_stages/ST_XX_Stage_Name/
```

**Step 2: Script/Utility Analysis**
- Check each .sh script for:
  - File path references (do they exist?)
  - Functional relevance (does it test current system?)
  - Dependency accuracy (are required tools available?)

**Step 3: Directory Assessment**  
- **backup/**: Remove if contains outdated code or duplicates git history
- **venv/**: Remove if duplicates project-level virtual environment
- **artifacts/**: Keep if contains unique stage deliverables

**Step 4: SSOT Verification**
- Ensure no duplicate documentation across multiple files
- Verify git provides adequate version control for removed utilities
- Confirm essential information preserved in numbered documents or llm.txt

#### **Cleanup Decision Matrix**

| File Type | Keep If | Remove If |
|-----------|---------|-----------|
| Documentation (.md) | Contains decisions, analysis, or unique context | Duplicate of information elsewhere |
| Scripts (.sh) | Tests current functionality with accurate paths | References non-existent files or old system |
| Backup Directories | Contains unique artifacts not in git | Duplicates git-managed code or outdated versions |
| Virtual Environments | Stage-specific dependencies required | Duplicates project-level dependencies |
| Config Files | Stage-specific configuration needed | Superseded by current project config |

#### **Post-Cleanup Validation**

**Essential Files Preserved**:
- ✅ llm.txt (AI contextual memory)
- ✅ NN-YYMMDD-descriptive_name.md (work documentation)  
- ✅ Historical analysis and decision documents
- ✅ Unique stage deliverables and artifacts

**Removed Categories**:
- ❌ Scripts with broken file references
- ❌ Backup directories duplicating git history
- ❌ Utilities testing superseded functionality
- ❌ Virtual environments duplicating project setup

#### **Methodology Benefits**

**Disk Space Management**: Eliminate unnecessary duplicates and outdated files  
**SSOT Compliance**: Single source of truth for all project information  
**Navigation Clarity**: Clean directories containing only relevant documentation  
**Version Control Efficiency**: Rely on git for code history rather than manual backups  
**Documentation Focus**: Preserve decision history while removing implementation debris  

#### **Stage Directory Standards**

**Optimal Structure**:
```
ST_XX_Stage_Name/
├── llm.txt                              # AI contextual memory
├── 00-06_*.md                          # Historical documentation (if applicable)  
├── NN-YYMMDD-descriptive_name.md       # Current work documentation
└── [unique_stage_artifacts]            # Stage-specific deliverables only
```

**Cleanup Frequency**: Mandatory after each stage completion before advancement to next stage.

**This cleanup protocol ensures systematic organization, eliminates technical debt, and maintains clear project structure across all development stages in the bchat methodology framework.**