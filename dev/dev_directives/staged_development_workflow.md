# Staged Development Workflow - Complete AI Assistant Protocol

## Overview

This directive provides a complete, actionable workflow protocol for AI assistants working on the bchat project. It defines the **Layered Contextual Memory Development Methodology** - a systematic approach to stage-based development that ensures safety, continuity, and user control throughout the development process.

**MANDATORY**: All AI assistants must follow this protocol exactly as written. No exceptions.

## Core Methodology: Layered Contextual Memory Development

### Philosophy
- **Iterative Progression**: Each stage builds incrementally on validated previous work
- **Contextual Memory**: Complete decision history preserved at each layer
- **User Control**: Explicit approval required before any structural changes
- **Safety First**: Never break working functionality during development
- **Documentation as Code**: Every action documented for future context

### Layer Structure
1. **Stage Layer** (`/dev/dev_stages/ST_XX_*`) - WHAT to implement and WHEN
2. **Directive Layer** (`/dev/dev_directives/`) - HOW to implement safely
3. **Context Layer** (`CLAUDE.md`, `llm.txt`) - WHY decisions were made
4. **System Layer** (logs, filemap, git) - Operational memory and traceability

## Complete Workflow Protocol

### Phase 1: Stage Discovery and Context Loading

#### Step 1.1: Stage Identification **[MANDATORY]**
```bash
# Always start by discovering existing stages
ls -la /dev/dev_stages/
```

**Actions**:
1. **NEVER CREATE** new stage directories without explicit user approval
2. **ALWAYS USE** existing stage directories for documentation
3. **IDENTIFY** which existing stage best fits the current work
4. **ASK USER** if unsure about stage selection

#### Step 1.2: Context Loading **[MANDATORY]**
```bash
# Load existing stage context
cat /dev/dev_stages/ST_XX_*/llm.txt  # AI contextual memory
ls -la /dev/dev_stages/ST_XX_*/      # All stage files
```

**Actions**:
1. **READ** all existing stage files in chronological order (00, 01, 02...)
2. **UNDERSTAND** current stage status and previous work
3. **IDENTIFY** what's already been completed vs what remains
4. **PRESERVE** context continuity from previous sessions

#### Step 1.3: System Status Verification **[MANDATORY]**
```bash
# Verify current system state
./bchat --status
git status
```

**Actions**:
1. **CONFIRM** system is operational before making changes
2. **DOCUMENT** current system status in stage work
3. **IDENTIFY** any broken functionality that needs addressing
4. **ESTABLISH** baseline for change impact assessment

### Phase 2: Work Planning and User Approval

#### Step 2.1: Task Analysis **[MANDATORY]**
**Process**:
1. **ANALYZE** user request against existing stage objectives
2. **IDENTIFY** required changes (CREATE/READ/UPDATE/DELETE operations)
3. **ASSESS** impact on existing functionality
4. **DETERMINE** if work fits in current stage or requires new stage

#### Step 2.2: TodoWrite Planning **[MANDATORY for complex tasks]**
**Criteria for TodoWrite usage**:
- Multi-step tasks (3+ distinct actions)
- CRUD operations affecting multiple files
- Complex implementations requiring coordination
- User explicitly requests task tracking

```markdown
TodoWrite Format:
1. [Specific actionable task]
2. [Specific actionable task] 
3. [Verify implementation]
4. [Update documentation]
5. [Run cascade procedures]
```

#### Step 2.3: Explicit User Approval **[MANDATORY for CRUD]**
**Before ANY Create/Update/Delete operations**:

```markdown
I need to perform the following CRUD operations:
- CREATE: [file/directory path] - [purpose]
- UPDATE: [file path] - [what will change]
- DELETE: [file path] - [reason for removal]

This will impact:
- [System component 1]
- [System component 2]

May I proceed with these changes?
```

**WAIT FOR EXPLICIT USER APPROVAL** before proceeding.

### Phase 3: Implementation with Safety Measures

#### Step 3.1: Pre-Implementation Safety **[MANDATORY]**
```bash
# Create checkpoint
git status
git stash push -m "Pre-implementation checkpoint"
```

**Actions**:
1. **VERIFY** git status is clean or changes are staged
2. **CREATE** checkpoint for rollback capability
3. **DOCUMENT** current working state
4. **CONFIRM** system functionality before changes

#### Step 3.2: Incremental Implementation **[MANDATORY]**
**Process**:
1. **IMPLEMENT** one TodoWrite task at a time
2. **TEST** each change immediately after implementation
3. **MARK** TodoWrite tasks as completed immediately upon finishing
4. **DOCUMENT** any issues or unexpected results
5. **NEVER** batch multiple tasks before testing

#### Step 3.3: Continuous Validation **[MANDATORY]**
```bash
# After each significant change
python3 -m py_compile [modified_files]  # Syntax check
./bchat --status                        # Functionality check
```

**Actions**:
1. **VALIDATE** syntax of modified code
2. **CONFIRM** system functionality remains intact
3. **TEST** new functionality works as expected
4. **ROLLBACK** immediately if any issues detected

### Phase 4: Post-Implementation Cascade Procedures

#### Step 4.1: Code Quality Verification **[MANDATORY]**
```bash
# Run available linting/type checking
black --check core/src/     # If available
flake8 core/src/           # If available  
python3 -m py_compile core/src/*.py  # Always run
```

**Actions**:
1. **RUN** all available code quality tools
2. **FIX** any issues detected
3. **DOCUMENT** if tools are not available
4. **ENSURE** Python syntax compilation passes

#### Step 4.2: System Functionality Verification **[MANDATORY]**
```bash
./bchat --status
```

**Actions**:
1. **CONFIRM** bchat system remains operational
2. **TEST** all core functionality still works
3. **VERIFY** no regression in existing features
4. **DOCUMENT** operational status in stage work

#### Step 4.3: Documentation Updates **[MANDATORY]**
```bash
# Update system logs
echo "YYYY-MM-DD HH:MM:SS - [Change description]" >> data/logs/bchat.log
```

**Actions**:
1. **LOG** all changes in `data/logs/bchat.log`
2. **UPDATE** stage work document with implementation details
3. **DOCUMENT** verification results and testing outcomes
4. **PRESERVE** decision rationale for future context

#### Step 4.4: Filemap Maintenance **[MANDATORY after CRUD]**
```bash
# Update filemap after any file structure changes
vi filemap.md  # Add/remove/update entries
```

**Actions**:
1. **UPDATE** filemap.md for any new files created
2. **REMOVE** entries for deleted files
3. **MODIFY** descriptions for updated files
4. **MAINTAIN** consistent tagging and categorization

#### Step 4.5: Git Management **[MANDATORY]**
```bash
git add [modified_files]
git status  # Verify staging
```

**Actions**:
1. **STAGE** all modified files
2. **VERIFY** staging is correct
3. **ENSURE** no unintended files are staged
4. **PREPARE** for potential commit (but don't commit unless asked)

### Phase 5: Stage Documentation and Context Preservation

#### Step 5.1: Stage Work Documentation **[MANDATORY]**
Create or update stage work document:
- **File Pattern**: `NN-YYMMDD-descriptive_name.md`
- **Location**: `/dev/dev_stages/ST_XX_*/`
- **Sequential Numbering**: Continue from existing stage files

**Required Content**:
```markdown
# NN-YYMMDD [Work Description]

**Date**: YYYY-MM-DD
**Stage**: ST_XX_Stage_Name  
**Status**: [COMPLETED/IN_PROGRESS/BLOCKED]
**Phase**: [Planning/Implementation/Verification]

## Work Summary
[What was accomplished]

## Implementation Details
[Technical details of changes made]

## Files Modified/Created
- `/path/to/file` - [description of changes]

## Verification Results
[Testing outcomes and functionality confirmation]

## Relationship to Previous Stage Work
[How this builds on or supersedes previous work]

## Next Steps
[What should happen next]
```

#### Step 5.2: Context Memory Updates **[MANDATORY]**
Update or create `llm.txt` in stage directory:

**Required Content**:
```markdown
## Current Stage Status (YYYY-MM-DD)

### **Implementation Status - [STATUS] ✅/⚠️/❌**
[Brief summary of current operational state]

### **Key Capabilities**
- [Capability 1] ✅
- [Capability 2] ✅  

### **Verification Confirmed**
[Testing results and operational confirmation]

[Concise readiness statement for next stage advancement]
```

#### Step 5.3: Methodology Compliance Verification **[MANDATORY]**
**Checklist - All must be ✅**:
- ✅ User approval obtained for all CRUD operations
- ✅ Existing stage directories used (no new stages created)
- ✅ TodoWrite used for complex/multi-step tasks
- ✅ All implementation tested and verified functional
- ✅ System functionality confirmed via `./bchat --status`
- ✅ Code quality checks completed
- ✅ Documentation updated (logs, stage work, llm.txt)
- ✅ Filemap updated for any CRUD operations
- ✅ Git staging completed
- ✅ Context preserved for future sessions

## Emergency Rollback Procedures

### If Implementation Fails
```bash
# Immediate rollback
git stash pop  # If changes were stashed
git checkout HEAD -- [modified_files]  # Reset specific files
./bchat --status  # Verify system recovery
```

### If System Becomes Unstable
1. **STOP** all implementation immediately
2. **ROLLBACK** using git procedures
3. **VERIFY** system functionality restored
4. **DOCUMENT** failure in stage work
5. **REQUEST** user guidance before proceeding

## Protocol Enforcement

### AI Assistant Requirements
1. **FOLLOW** this protocol exactly as written
2. **ASK** for clarification if any step is unclear
3. **NEVER** skip steps for efficiency or convenience  
4. **OBTAIN** explicit user approval for all CRUD operations
5. **DOCUMENT** all work using established patterns

### User Override Authority
- Users can override any protocol step with explicit instruction
- Document any protocol overrides in stage work
- Maintain safety measures unless explicitly instructed otherwise

### Violation Consequences
Non-compliance with this protocol constitutes:
- Breaking project methodology standards
- Potentially damaging system stability  
- Creating context discontinuity for future sessions
- Requiring corrective action and re-work

## Integration with Existing Directives

This workflow protocol **extends and operationalizes** existing directives:
- **general.md**: Core principles and file management rules
- **implementation_safety.md**: Safety procedures and rollback methods
- **gemini_specific_guidelines.md**: AI-specific development patterns

**Hierarchy**: This workflow protocol governs **HOW** to implement the **WHAT** defined in general.md principles.

## Success Metrics

### Immediate Indicators
- No system functionality regression during development
- Complete documentation trail for all changes
- Successful verification of all modifications
- Proper git staging and file organization

### Long-term Indicators  
- Context continuity preserved across sessions
- Stage progression follows logical dependency chain
- User maintains control and visibility over all changes
- Knowledge base grows incrementally without information loss

---

## Protocol Summary for Quick Reference

**Every AI Assistant Must**:
1. **DISCOVER** existing stages (never create new ones)
2. **LOAD** context from stage files and llm.txt
3. **PLAN** work with TodoWrite for complex tasks  
4. **OBTAIN** user approval for all CRUD operations
5. **IMPLEMENT** incrementally with continuous testing
6. **VERIFY** system functionality after each change
7. **DOCUMENT** all work in stage files and logs
8. **UPDATE** filemap for any file structure changes
9. **STAGE** changes in git
10. **PRESERVE** context for future sessions

**This is the complete bchat Layered Contextual Memory Development Methodology. Follow it exactly.**