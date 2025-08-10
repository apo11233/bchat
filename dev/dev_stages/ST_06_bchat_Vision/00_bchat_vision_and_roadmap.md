# BChat MCP - Sistema de Meta-Workflow para Desarrollo Colaborativo con IA

## 🎯 Visión del Proyecto

BChat es un sistema ambicioso que integra múltiples IAs (Claude, Gemini, y potencialmente Grok) para crear un meta-workflow inteligente de desarrollo de software. El sistema aprende de la experiencia, refina directivas de desarrollo automáticamente, y facilita la colaboración machine-to-machine para optimizar metodologías de trabajo.

## 🏗️ Arquitectura del Sistema

### Componentes Core

```
bchat_mcp/
├── README.md                          # Este archivo
├── bchat_core.py                      # Sistema central BChat MVP
├── claude_memory_mvp.py               # Memoria cross-workspace Claude
├── llm_shared_memory.py               # Memoria compartida Claude-Gemini
├── mcp_server.py                      # Servidor MCP (próximo)
├── tests/                             # Tests de prueba de concepto
│   ├── test_core.sh
│   ├── test_directives.sh
│   └── test_integration.sh
└── examples/                          # Ejemplos de uso
    ├── sample_project/
    └── demo_workflow.md
```

### Capas del Sistema (Iterative Development Architecture)

#### **Layered LLM Context System**
```
/project_root/
├── llm.txt                           # Global AI-generated context
├── .bchat/
│   ├── stages/
│   │   ├── ST_00_core/
│   │   │   ├── llm.txt              # Stage-specific AI context
│   │   │   ├── ST_00_01_init.md     # Auto-numbered artifacts
│   │   │   └── ST_00_02_structure.py
│   │   ├── ST_01_memory/
│   │   │   ├── llm.txt              # Inherits from global + adds specifics
│   │   │   └── ST_01_01_indexing.py
│   │   └── ST_XX_advanced/
│   │       └── llm.txt              # Progressively richer context
│   └── iterations/
│       ├── ITER_01_mvp_core/        # First iteration: MVP
│       ├── ITER_02_enhanced_core/   # Second iteration: Revisit ST_00
│       └── ITER_03_full_system/     # Third iteration: Complete
```

#### **Iterative Development Layers**
1. **ITER_01: MVP Core** - Stages ST_00 to ST_03 (basic functionality)
2. **ITER_02: Enhanced Core** - Revisit ST_00, strengthen foundation, extend to ST_06
3. **ITER_03: Full System** - Complete all checkpoints, machine-to-machine collaboration
4. **ITER_XX: Future** - Advanced capabilities, new paradigms

## 📁 Scripts Incluidos en esta Propuesta

### 1. `claude_memory_mvp.py`
**Propósito**: Sistema de memoria cross-workspace para Claude Code CLI sin dependencias externas.

**Funcionalidades**:
- Indexación automática de directorios `.claude`
- Búsqueda inteligente en contextos de múltiples proyectos
- Cache en JSON para persistencia simple
- Sistema de scoring por relevancia

### 2. `llm_shared_memory.py`
**Propósito**: Sistema de memoria compartida entre Claude y Gemini con APIs.

**Funcionalidades**:
- Conversaciones unificadas entre múltiples IAs
- Contexto automático basado en historial
- Tags automáticos por contenido técnico
- Búsqueda cross-LLM por workspace

### 3. `bchat_core.py`
**Propósito**: Sistema central integrado de meta-workflow con todas las funcionalidades core.

**Funcionalidades**:
- **Dev Directives**: Gestión y refinamiento automático de directivas
- **Dev Stages**: Fases numeradas con contexto específico (ST_xx)
- **Memoria Layered**: Contexto global + contexto por stage
- **Checkpoints**: Snapshots del estado del proyecto
- **Métricas de Efectividad**: Aprendizaje basado en resultados
- **PRP Integration**: Auto-generación de llm.txt por IAs

### 4. `bchat_mcp_server.py`
**Propósito**: Servidor MCP que expone capabilities de BChat para integración con herramientas.

**Funcionalidades**:
- **MCP Protocol**: Implementación estándar del protocolo MCP
- **Capability Discovery**: Auto-exposición de funcionalidades BChat
- **Tool Integration**: Conexión con Claude Code CLI, IDEs, etc.
- **Resource Management**: Gestión de recursos y contextos
- **Session Management**: Manejo de sesiones colaborativas IA-IA

### 5. `bchat_integration.py`
**Propósito**: Capa de integración que unifica todos los sistemas anteriores.

**Funcionalidades**:
- **Unified API**: Punto único de acceso a todas las funcionalidades
- **Cross-System Context**: Contexto unificado desde múltiples fuentes
- **Workflow Orchestration**: Orquestación de flujos iterativos
- **Machine-to-Machine**: Facilitador de colaboración automática IA-IA

## 🔄 **PRP (Prompt-Response-Process) Methodology**

BChat implementa el ciclo **PRP** donde las IAs no solo responden, sino que **generan contexto activamente**:

### PRP Cycle
```
1. PROMPT: Usuario/IA formula consulta con contexto layered
2. RESPONSE: IA procesa y responde
3. PROCESS: IA actualiza llm.txt relevantes automáticamente
   ├── Global llm.txt (insights cross-project)
   ├── Stage llm.txt (learnings específicos)
   └── Iteration llm.txt (progreso iterativo)
```

### Contexto Auto-Generado por IAs
```python
# Las IAs escriben directamente en llm.txt
def ai_update_context(self, stage_id: str, insight: str, ai_model: str):
    """IA actualiza contexto automáticamente después de cada respuesta"""
    timestamp = datetime.now().isoformat()
    
    # Formato estándar para llm.txt
    context_entry = f"""
## {timestamp} | {ai_model.upper()} Insight
{insight}

### Aplicable a:
- Current stage: {stage_id}
- Related stages: [auto-detected]
- Future iterations: [yes/no]

### Confidence: [0.0-1.0]
### Impact: [low/medium/high]
---
"""
    
    # Escribir en múltiples capas según relevancia
    self.append_to_stage_llm(stage_id, context_entry)
    if self.is_global_insight(insight):
        self.append_to_global_llm(context_entry)
```

## 🎯 **Iterative Development Roadmap**

### **ITERATION 1: MVP Core Foundation**

#### STAGE ST_00: Core Architecture
- **Goal**: Establish fundamental BChat structure
- **AI-Generated Context**: Architecture decisions, trade-offs, learnings
- **Artifacts**: `ST_00_01_core.py`, `ST_00_02_memory.py`, `ST_00_03_directives.py`
- **llm.txt Updates**: AIs document why each architectural choice was made

#### STAGE ST_01: Basic Memory System  
- **Goal**: Cross-workspace memory without dependencies
- **Inherits**: ST_00 context + adds memory-specific insights
- **AI-Generated Context**: Indexing strategies, search optimization
- **Artifacts**: `ST_01_01_indexing.py`, `ST_01_02_search.py`

#### STAGE ST_02: Simple Directives
- **Goal**: Basic directive management
- **AI-Generated Context**: Effectiveness patterns, usage analytics
- **Artifacts**: `ST_02_01_directive_core.py`, `ST_02_02_scoring.py`

#### STAGE ST_03: MVP Integration
- **Goal**: Integrate all MVP components
- **AI-Generated Context**: Integration challenges, solutions found
- **Iteration Checkpoint**: Review global llm.txt, prepare for ITER_02

### **ITERATION 2: Enhanced Core + MCP Foundation**

#### STAGE ST_00_v2: Strengthen Core Architecture
- **Goal**: Revisit ST_00 with learnings from ST_01-03
- **AI-Generated Context**: What worked, what needs refactoring
- **New Insights**: Performance optimizations, better patterns
- **Artifacts**: `ST_00_04_optimized_core.py`, `ST_00_05_patterns.py`

#### STAGE ST_04: Advanced Memory Features
- **Goal**: Add semantic search, cross-project insights
- **Builds on**: Enhanced ST_00 + original ST_01
- **AI-Generated Context**: Advanced search patterns, performance metrics

#### STAGE ST_05: Smart Directives
- **Goal**: Auto-refinement, effectiveness learning
- **AI-Generated Context**: ML insights, pattern recognition in directive success

#### STAGE ST_06: MCP Server Foundation
- **Goal**: Basic MCP protocol implementation
- **AI-Generated Context**: MCP patterns, capability discovery insights
- **Artifacts**: `ST_06_01_mcp_server.py`, `ST_06_02_protocol.py`

#### STAGE ST_07: BChat Integration Layer
- **Goal**: Unified API connecting all systems
- **AI-Generated Context**: Integration challenges, orchestration patterns
- **Artifacts**: `ST_07_01_integration.py`, `ST_07_02_unified_api.py`

### **ITERATION 3: Full System + Machine Collaboration**

#### STAGE ST_08: Cross-LLM Communication
- **Goal**: Claude-Gemini collaboration via MCP
- **AI-Generated Context**: Communication protocols, consensus mechanisms
- **Builds on**: MCP foundation + integration layer

#### STAGE ST_09: Machine-to-Machine Workflows
- **Goal**: Autonomous IA-IA collaboration sessions
- **AI-Generated Context**: Collaboration patterns, conflict resolution
- **Integration**: Full BChat ecosystem working together

#### STAGE ST_10: Meta-Learning System
- **Goal**: AIs analyze their own context generation effectiveness
- **AI-Generated Context**: Meta-insights about AI learning patterns
- **Ultimate Goal**: Self-improving system

### **ITERATION 3: Full System Capabilities**
- **Revisit All Previous Stages**: With accumulated learnings
- **Add Advanced Stages**: ST_07-ST_10 (MCP, Machine-to-Machine, etc.)
- **Meta-Learning**: AIs analyze their own context generation patterns

## 🧠 **Layered LLM Context in Practice**

### **Global llm.txt** (Project Root)
```markdown
# BChat Global AI Context

## 2025-01-15 | CLAUDE Architectural Insight
The layered context approach proves superior to flat memory.
Each stage should inherit from global but add specifics.

### Confidence: 0.9
### Impact: high
### Applies to: All future stages

## 2025-01-15 | GEMINI Memory Optimization
JSON indexing with hash deduplication reduces memory usage by 60%.
Consider implementing incremental updates for large projects.

### Confidence: 0.8
### Impact: medium
### Applies to: Memory-related stages
---
```

### **Stage llm.txt** (ST_01/llm.txt)
```markdown
# Stage ST_01: Memory System - AI Context

## Inherited from Global
[Auto-populated from global llm.txt relevant sections]

## Stage-Specific Insights

## 2025-01-15 | CLAUDE Memory Implementation
Hash-based deduplication works well for detecting unchanged files.
Next iteration should consider content similarity, not just exact matches.

### Stage Impact: Critical for ST_01 performance
### Future Stages: Applicable to ST_04 advanced memory

## 2025-01-15 | GEMINI Search Optimization  
Search scoring algorithm needs refinement. Current approach:
- Exact match: +10 points
- Partial match: +3 points
- Tag match: +5 points

Suggested improvement: Add recency weighting.
---
```

### **PRP-Driven Development Example**

```bash
# ITER_01, ST_00: User starts core development
user: "Initialize BChat core architecture"

# PROMPT: User request + empty global llm.txt
# RESPONSE: Claude designs architecture  
# PROCESS: Claude writes to ST_00/llm.txt:
#   "Chose modular design because... Trade-offs considered... 
#    Recommended next steps for ST_01..."

# ITER_01, ST_01: Memory system development
user: "Implement cross-workspace memory"

# PROMPT: User request + ST_00 context + global context
# RESPONSE: Claude implements memory system
# PROCESS: Claude updates both ST_01/llm.txt and global llm.txt:
#   "Memory indexing strategy works well... Performance considerations...
#    This pattern should be reused in ST_04..."

# ITER_02, ST_00_v2: Revisiting core with accumulated wisdom
user: "Revisit and strengthen core architecture"

# PROMPT: User request + ALL accumulated llm.txt contexts
# RESPONSE: Claude sees patterns across all stages, proposes improvements
# PROCESS: Claude writes enhanced insights:
#   "After implementing ST_01-03, I realize the core should be refactored...
#    The memory patterns from ST_01 suggest the core needs..."
```

## 🧪 **Iterative Tests & Validation**

### **ITER_01 Tests: MVP Foundation**
```bash
# Test ST_00: Core architecture
./tests/iter01_st00_core.sh
# Validates: Basic structure, AI context generation

# Test ST_01: Memory system  
./tests/iter01_st01_memory.sh
# Validates: Cross-workspace indexing, AI learning documentation

# Test ST_02: Basic directives
./tests/iter01_st02_directives.sh
# Validates: Directive management, effectiveness tracking

# Integration test ITER_01
./tests/iter01_integration.sh
# Validates: All components work together, llm.txt coherence
```

### **ITER_02 Tests: Enhanced Core**
```bash
# Test ST_00_v2: Strengthened core
./tests/iter02_st00_enhanced.sh  
# Validates: Improvements over v1, AI-documented reasoning

# Test ST_04: Advanced memory
./tests/iter02_st04_advanced_memory.sh
# Validates: Semantic search, performance improvements

# Cross-iteration consistency test
./tests/iter02_consistency.sh
# Validates: Context inheritance, learning propagation
```

### **llm.txt Quality Metrics**
```bash
# Validate AI-generated context quality
python validate_llm_context.py --stage ST_01
# Checks: Coherence, actionable insights, confidence levels

# Cross-reference context accuracy  
python cross_reference_context.py --iteration ITER_01
# Validates: Consistency between global and stage contexts
```

## 🔄 **Integración Completa BChat Ecosystem**

### **Arquitectura de Integración Unificada**

```python
# bchat_integration.py - Orquestador principal
class BChatEcosystem:
    def __init__(self):
        # Sistemas core
        self.core = BChatCore()                    # Directivas, stages, contexto
        self.claude_memory = ClaudeMemoryMVP()     # Memoria cross-workspace
        self.llm_memory = LLMSharedMemory()        # Memoria compartida Claude-Gemini
        
        # Nuevos componentes
        self.mcp_server = BChatMCPServer()         # Servidor MCP
        self.workflow_engine = WorkflowEngine()    # Orquestación iterativa
        
    def unified_context_query(self, query: str, stage_id: str = None) -> str:
        """Contexto unificado desde TODAS las fuentes"""
        contexts = []
        
        # 1. Contexto layered BChat (llm.txt generados por IAs)
        contexts.append(self.core.get_layered_context(stage_id))
        
        # 2. Memoria Claude Code (.claude directories)
        claude_results = self.claude_memory.search_memory(query, limit=3)
        contexts.append(self.format_claude_context(claude_results))
        
        # 3. Memoria compartida LLM (conversaciones previas)
        llm_results = self.llm_memory.search_memory(query, limit=3)
        contexts.append(self.format_llm_context(llm_results))
        
        # 4. MCP resources (herramientas externas)
        mcp_context = self.mcp_server.get_relevant_resources(query)
        contexts.append(mcp_context)
        
        return self.synthesize_unified_context(contexts)
    
    def ai_collaboration_session(self, task: str, stage_id: str) -> Dict:
        """Sesión colaborativa IA-IA completa con toda la memoria"""
        
        # 1. Obtener contexto unificado
        unified_context = self.unified_context_query(task, stage_id)
        
        # 2. Consulta a Claude con contexto completo
        claude_response = self.llm_memory.chat_with_llm(
            f"Context: {unified_context}\n\nTask: {task}",
            'claude',
            workspace=self.core.project.name
        )
        
        # 3. Gemini revisa propuesta de Claude
        gemini_response = self.llm_memory.chat_with_llm(
            f"Review Claude's approach: {claude_response}\n\nTask: {task}",
            'gemini', 
            workspace=self.core.project.name
        )
        
        # 4. Síntesis y actualización automática de contexto
        synthesis = self.synthesize_ai_collaboration(claude_response, gemini_response)
        
        # 5. Actualizar llm.txt automáticamente
        self.core.ai_update_context(stage_id, synthesis['insights'], 'collaboration')
        
        # 6. Actualizar directivas si aplicable
        if synthesis['directive_updates']:
            self.core.update_directives_from_ai_insights(synthesis['directive_updates'])
        
        return synthesis
```

### **MCP Server Integration**

```python
# bchat_mcp_server.py
class BChatMCPServer:
    """Servidor MCP que expone capabilities de BChat"""
    
    def __init__(self, bchat_core: BChatCore):
        self.bchat = bchat_core
        self.capabilities = {
            "memory/search": self.search_unified_memory,
            "directives/manage": self.manage_directives,
            "stages/workflow": self.manage_workflow,
            "ai/collaborate": self.facilitate_ai_collaboration,
            "context/layered": self.provide_layered_context,
            "learning/meta": self.meta_learning_insights
        }
    
    def handle_mcp_request(self, request: Dict) -> Dict:
        """Maneja requests MCP estándar"""
        capability = request.get('capability')
        params = request.get('params', {})
        
        if capability in self.capabilities:
            return self.capabilities[capability](params)
        else:
            return {"error": f"Capability {capability} not supported"}
    
    def search_unified_memory(self, params: Dict) -> Dict:
        """MCP endpoint para búsqueda unificada"""
        query = params.get('query')
        workspace = params.get('workspace')
        
        # Buscar en todas las fuentes
        results = {
            'claude_memory': self.bchat.claude_memory.search_memory(query),
            'llm_shared': self.bchat.llm_memory.search_memory(query, workspace),
            'layered_context': self.bchat.get_layered_context(),
            'directives': self.bchat.get_applicable_directives(query)
        }
        
        return {"status": "success", "results": results}
    
    def facilitate_ai_collaboration(self, params: Dict) -> Dict:
        """MCP endpoint para colaboración IA-IA"""
        task = params.get('task')
        stage_id = params.get('stage_id', self.bchat.project.current_stage)
        
        # Ejecutar sesión colaborativa completa
        collaboration_result = self.bchat.ai_collaboration_session(task, stage_id)
        
        return {
            "status": "success", 
            "collaboration": collaboration_result,
            "updated_contexts": self.get_updated_contexts(stage_id)
        }
```

### **Workflow Engine para Desarrollo Iterativo**

```python
# En bchat_integration.py
class WorkflowEngine:
    """Orquesta el desarrollo iterativo con PRP methodology"""
    
    def execute_iteration(self, iteration_id: str, stages: List[str]) -> Dict:
        """Ejecuta una iteración completa"""
        iteration_results = {
            'iteration_id': iteration_id,
            'stages_completed': [],
            'ai_insights_generated': [],
            'directives_refined': [],
            'next_iteration_recommendations': []
        }
        
        for stage_id in stages:
            # Ejecutar stage con PRP
            stage_result = self.execute_stage_with_prp(stage_id)
            iteration_results['stages_completed'].append(stage_result)
            
            # Las IAs actualizan contexto automáticamente
            ai_insights = self.collect_ai_generated_insights(stage_id)
            iteration_results['ai_insights_generated'].extend(ai_insights)
        
        # Al final de iteración, meta-análisis
        meta_insights = self.analyze_iteration_effectiveness(iteration_id)
        iteration_results['next_iteration_recommendations'] = meta_insights
        
        return iteration_results
    
    def execute_stage_with_prp(self, stage_id: str) -> Dict:
        """Ejecuta stage individual con metodología PRP"""
        
        # PROMPT: Contexto unificado + stage requirements
        unified_context = self.bchat.unified_context_query("", stage_id)
        
        # RESPONSE: IA(s) resuelven el stage
        ai_responses = self.get_ai_responses_for_stage(stage_id, unified_context)
        
        # PROCESS: IAs actualizan llm.txt automáticamente
        for ai_model, response in ai_responses.items():
            insights = self.extract_insights_from_response(response)
            self.bchat.core.ai_update_context(stage_id, insights, ai_model)
        
        return {
            'stage_id': stage_id,
            'ai_responses': ai_responses,
            'context_updates': self.get_context_updates(stage_id),
            'artifacts_created': self.get_stage_artifacts(stage_id)
        }
```

## 🛠️ Configuración Inicial

### 1. Preparar Entorno
```bash
# Crear estructura de proyecto
mkdir bchat_mcp
cd bchat_mcp

# Copiar scripts
cp claude_memory_mvp.py .
cp llm_shared_memory.py .
cp bchat_core.py .
```

### 2. Configurar APIs
```bash
# Crear archivo .env
echo "ANTHROPIC_API_KEY=tu_claude_key" > .env
echo "GOOGLE_API_KEY=tu_gemini_key" >> .env
```

### 3. Inicializar Proyecto
```bash
# Inicializar BChat en proyecto existente
python bchat_core.py init

# Verificar estructura
ls -la .bchat/
```

### 4. Configuración Inicial de Directivas
```bash
# Agregar directivas fundamentales
python bchat_core.py directive add \
    --title "Code Review Required" \
    --content "All code changes must be reviewed before merging" \
    --tags review git quality

python bchat_core.py directive add \
    --title "Test Coverage" \
    --content "Maintain >80% test coverage for all modules" \
    --tags testing coverage quality

python bchat_core.py directive add \
    --title "Documentation First" \
    --content "Document design decisions before implementation" \
    --tags documentation design
```

## 🎮 Casos de Uso Demostrativos

### Caso 1: Inicio de Proyecto Nuevo
```bash
# 1. Inicializar BChat
python bchat_core.py init

# 2. Crear stage de planning
python bchat_core.py stage create --name "Planning" --description "Requirements and design"

# 3. Consultar experiencia previa
python claude_memory_mvp.py search -q "project setup best practices"

# 4. Actualizar contexto con hallazgos
python bchat_core.py context update --content "Based on previous projects, focus on..."
```

### Caso 2: Consulta Cross-Workspace
```bash
# Usuario en proyecto 'meli' pregunta sobre implementación en 'qualia'
python claude_memory_mvp.py search -q "JWT authentication" -w qualia

# Usar contexto encontrado para consulta actual
python llm_shared_memory.py chat \
    --model claude \
    --message "Implementa autenticación similar a qualia project" \
    --workspace meli
```

### Caso 3: Refinamiento de Directivas
```bash
# Después de completar un stage
python bchat_core.py stage complete --id ST_00

# Ver sugerencias de mejora
python bchat_core.py directive suggest

# Refinamiento colaborativo (futuro)
python bchat_core.py ai-collaborate --task "refine testing directives"
```

## 🔮 Visión Futura

### Integración con Grok
Aunque actualmente no tenemos acceso a API de Grok, el sistema está diseñado para ser extensible:

```python
# Futuro: grok_integration.py
def call_grok_api(message: str, context: str = "") -> str:
    """Integración futura con Grok API"""
    # Implementar cuando esté disponible
    pass

# En llm_shared_memory.py, agregar soporte para 'grok' model
```

### Machine-to-Machine Collaboration
Sesiones automáticas donde las IAs colaboran sin intervención humana:

```python
def ai_collaboration_session(task: str) -> Dict:
    """
    1. Claude analiza y propone solución
    2. Gemini revisa y sugiere mejoras  
    3. Grok valida desde perspectiva diferente
    4. Síntesis automática de consenso
    5. Actualización de directivas
    """
```

### MCP Server Completo
Servidor MCP que expone capabilities de BChat:

```python
# mcp_server.py (próximo)
class BChatMCPServer:
    capabilities = [
        "memory/search",
        "directives/manage", 
        "stages/workflow",
        "ai/collaborate"
    ]
```

## 🤝 Solicitud de Revisión

### Para Claude
- Revisar arquitectura de memoria layered
- Validar integración con Claude Code CLI
- Sugerir optimizaciones en búsqueda de contexto

### Para Gemini  
- Evaluar sistema de directivas auto-refinables
- Revisar protocolo de colaboración machine-to-machine
- Proponer métricas adicionales de efectividad

### Para Grok (consulta externa)
- Perspectiva sobre meta-workflows en desarrollo
- Validación de enfoque de aprendizaje automático
- Sugerencias de integración futura

## 📊 Métricas de Éxito

### Métricas Técnicas
- **Precisión de búsqueda**: >85% de contexto relevante
- **Velocidad de indexación**: <2s para workspaces grandes
- **Efectividad de directivas**: Promedio >0.7 después de 10 usos

### Métricas de Productividad
- **Reducción en tiempo de setup**: 50% menos tiempo en nuevos proyectos
- **Mejora en decisiones**: Decisiones técnicas más consistentes
- **Reutilización de conocimiento**: 80% de consultas resueltas con contexto interno

### Métricas de Aprendizaje
- **Refinamiento automático**: 1+ directiva refinada por semana
- **Consenso IA**: >90% de acuerdo en decisiones técnicas
- **Propagación de mejores prácticas**: Automática entre proyectos

## 🚀 Próximos Pasos

1. **Implementar CHECKPOINT 1** - Validar core básico
2. **Tests exhaustivos** - Verificar cada componente
3. **Iteración rápida** - Feedback loop con IAs
4. **Expansión gradual** - Agregar capabilities progresivamente
5. **Documentación continua** - Mantener README actualizado

---

**Nota**: Este es un MVP ambicioso pero estructurado para permitir iteración e integración progresiva. Cada checkpoint es independiente y testeable, permitiendo validación continua del enfoque.

**Estructura completa del repositorio**:
```
bchat_mcp/
├── README.md                           # Este archivo completo
├── bchat_core.py                      # Sistema central con stages/directivas
├── claude_memory_mvp.py               # Memoria cross-workspace Claude
├── llm_shared_memory.py               # Memoria compartida Claude-Gemini  
├── bchat_mcp_server.py               # Servidor MCP con capabilities
├── bchat_integration.py              # Capa unificada + workflow engine
├── requirements.txt                   # Sin dependencias externas (stdlib only)
├── .env.example                      # Template APIs (Claude, Gemini, futuro Grok)
├── tests/                            # Tests iterativos por checkpoint
│   ├── iter01_st00_core.sh
│   ├── iter01_integration.sh  
│   ├── iter02_mcp_foundation.sh
│   └── iter03_full_collaboration.sh
├── examples/                         # Casos de uso demostrativos
│   ├── sample_project_iter01/
│   ├── mcp_integration_demo/
│   └── ai_collaboration_session.md
└── docs/                            # Documentación específica
    ├── mcp_protocol_implementation.md
    ├── prp_methodology_guide.md
    └── ai_context_generation_patterns.md
```