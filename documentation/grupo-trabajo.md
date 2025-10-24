# Grupo de Trabajo y Roles - Proyecto EduRAG

## Información del Documento

**Curso:** Análisis de Sistemas II  
**Proyecto:** EduRAG - Sistema de Gestión Educativa con IA  
**Tipo de Documento:** Estructura del Equipo y Roles Scrum  
**Fecha:** Octubre 2025

---

## 1. Introducción

Este documento describe la estructura del equipo de desarrollo del proyecto EduRAG, detallando los roles definidos bajo la metodología **Scrum**, las responsabilidades de cada miembro, y la distribución de tareas durante el ciclo de desarrollo del proyecto.

---

## 2. Metodología: Scrum

### 2.1 ¿Por qué Scrum?

**Scrum** es un marco de trabajo ágil que permite desarrollar software de manera iterativa e incremental. Se eligió Scrum para este proyecto por las siguientes razones:

#### Ventajas de Scrum:

✅ **Iterativo e Incremental:**
- Permite entregas parciales funcionales al final de cada sprint.
- Facilita validación temprana de funcionalidades.
- Reduce riesgo de desarrollar funcionalidades incorrectas.

✅ **Adaptable al Cambio:**
- Responde rápidamente a cambios de requerimientos.
- Permite repriorizar backlog según necesidades.
- Ideal para proyectos académicos con descubrimiento continuo.

✅ **Colaboración Continua:**
- Daily standups mantienen al equipo sincronizado.
- Sprint reviews permiten feedback inmediato.
- Retrospectivas fomentan mejora continua.

✅ **Transparencia:**
- Progreso visible mediante tablero Scrum.
- Métricas claras (velocity, burndown charts).
- Stakeholders (docente) pueden ver avances en tiempo real.

✅ **Roles Claros:**
- Product Owner define qué se construye.
- Scrum Master facilita el proceso.
- Development Team ejecuta el trabajo.

### 2.2 Ceremonias de Scrum Implementadas

#### Sprint Planning (Planificación del Sprint)
- **Frecuencia:** Al inicio de cada sprint (cada 2 semanas)
- **Duración:** 2 horas
- **Objetivo:** Seleccionar user stories del backlog y definir sprint goal
- **Participantes:** Todo el equipo

#### Daily Standup (Reunión Diaria)
- **Frecuencia:** Diaria (lunes a viernes)
- **Duración:** 15 minutos
- **Objetivo:** Sincronizar equipo y detectar bloqueos
- **Preguntas clave:**
  - ¿Qué hice ayer?
  - ¿Qué haré hoy?
  - ¿Tengo algún impedimento?

#### Sprint Review (Revisión del Sprint)
- **Frecuencia:** Al final de cada sprint
- **Duración:** 1.5 horas
- **Objetivo:** Demostrar funcionalidades completadas
- **Participantes:** Equipo + stakeholders (docente)

#### Sprint Retrospective (Retrospectiva)
- **Frecuencia:** Al final de cada sprint (después de review)
- **Duración:** 1 hora
- **Objetivo:** Identificar mejoras en el proceso
- **Formato:** ¿Qué hicimos bien? ¿Qué podemos mejorar? ¿Qué acciones tomaremos?

---

## 3. Estructura del Equipo

### 3.1 Tamaño del Equipo

**Total de Miembros:** 5 personas

**Composición:**
- 1 Product Owner
- 1 Scrum Master
- 3 Desarrolladores (Development Team)

### 3.2 Organigrama del Equipo

```
                    ┌─────────────────────┐
                    │   Product Owner     │
                    │  (Stakeholder Rep)  │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
        ┌───────▼────────┐          ┌────────▼────────┐
        │  Scrum Master  │          │ Development Team│
        │   (Facilitador)│          │  (3 personas)   │
        └────────────────┘          └─────────────────┘
                                            │
                        ┌───────────────────┼───────────────────┐
                        │                   │                   │
                ┌───────▼────────┐  ┌───────▼────────┐  ┌──────▼─────────┐
                │ Desarrollador 1│  │ Desarrollador 2│  │ Desarrollador 3│
                │ (Full Stack)   │  │ (Backend/IA)   │  │ (Frontend/UX)  │
                └────────────────┘  └────────────────┘  └────────────────┘
```

---

## 4. Roles y Responsabilidades

### 4.1 Product Owner (PO)

#### Identificación:
- **Rol:** Product Owner
- **Representante de:** Institución educativa / Stakeholders académicos
- **Participación:** 30% del tiempo del proyecto

#### Responsabilidades Principales:

**1. Gestión del Product Backlog:**
- Crear y mantener el Product Backlog priorizado.
- Escribir User Stories claras con criterios de aceptación.
- Priorizar funcionalidades según valor de negocio.

**2. Definición de Visión:**
- Definir la visión del producto (EduRAG).
- Comunicar objetivos del proyecto al equipo.
- Asegurar alineación con objetivos académicos.

**3. Validación de Entregables:**
- Aceptar o rechazar incrementos de producto en Sprint Reviews.
- Validar que funcionalidades cumplen criterios de aceptación.
- Proveer feedback continuo al equipo.

**4. Comunicación con Stakeholders:**
- Representar al equipo ante el docente de Análisis de Sistemas II.
- Reportar progreso y bloqueos.
- Gestionar expectativas.

#### Actividades Específicas en EduRAG:

- ✅ Definió requerimientos del sistema de gestión educativa.
- ✅ Priorizó desarrollo del motor RAG como funcionalidad crítica.
- ✅ Validó que chat inteligente cumple expectativas educativas.
- ✅ Aprobó arquitectura propuesta por el equipo.
- ✅ Revisó y aceptó cada incremento en Sprint Reviews.

#### Habilidades Requeridas:
- Conocimiento del dominio educativo.
- Capacidad de priorización.
- Comunicación efectiva.
- Toma de decisiones.

---

### 4.2 Scrum Master (SM)

#### Identificación:
- **Rol:** Scrum Master
- **Función:** Facilitador del proceso Scrum
- **Participación:** 40% del tiempo del proyecto

#### Responsabilidades Principales:

**1. Facilitación de Ceremonias:**
- Organizar y facilitar Sprint Planning, Daily Standups, Reviews y Retrospectives.
- Asegurar que ceremonias sean efectivas y respeten timeboxes.
- Mantener enfoque del equipo durante reuniones.

**2. Remoción de Impedimentos:**
- Identificar bloqueos que afecten al equipo.
- Trabajar activamente para remover obstáculos.
- Escalar problemas que no puede resolver solo.

**3. Coaching del Equipo:**
- Enseñar y reforzar principios de Scrum.
- Fomentar auto-organización del Development Team.
- Promover mejora continua.

**4. Protección del Equipo:**
- Proteger al equipo de interrupciones externas.
- Asegurar que el equipo pueda enfocarse en el sprint goal.
- Mediar conflictos si surgen.

**5. Gestión de Herramientas:**
- Mantener tablero Scrum actualizado (Trello/Jira).
- Generar métricas (burndown charts, velocity).
- Documentar acuerdos y decisiones.

#### Actividades Específicas en EduRAG:

- ✅ Organizó 6 sprints de 2 semanas cada uno.
- ✅ Facilitó 30+ daily standups.
- ✅ Removió bloqueos técnicos (problemas con OpenAI API, configuración de pgvector).
- ✅ Gestionó tablero Trello con user stories y tareas.
- ✅ Generó reportes de progreso semanales.
- ✅ Coordinó con Product Owner para refinamiento de backlog.

#### Habilidades Requeridas:
- Conocimiento profundo de Scrum.
- Liderazgo servicial (servant leadership).
- Resolución de conflictos.
- Facilitación de grupos.
- Organización y seguimiento.

---

### 4.3 Development Team (Equipo de Desarrollo)

#### Composición:
- **Total:** 3 Desarrolladores
- **Tipo:** Equipo cross-funcional (pueden trabajar en frontend, backend, DB)
- **Participación:** 100% del tiempo del proyecto

#### Responsabilidades Colectivas:

**1. Desarrollo del Producto:**
- Implementar funcionalidades definidas en el Sprint Backlog.
- Escribir código de calidad siguiendo estándares.
- Realizar pruebas unitarias e integración.

**2. Auto-Organización:**
- Decidir cómo distribuir tareas entre miembros.
- Estimar complejidad de user stories (story points).
- Comprometerse con el sprint goal.

**3. Colaboración:**
- Compartir conocimiento entre miembros (pair programming).
- Revisar código de otros (code reviews).
- Ayudarse mutuamente para completar sprint.

**4. Calidad:**
- Asegurar que código cumple Definition of Done.
- Refactorizar cuando sea necesario.
- Documentar funcionalidades implementadas.

**5. Comunicación:**
- Participar activamente en todas las ceremonias.
- Comunicar impedimentos en daily standups.
- Proveer estimaciones realistas.

---

#### 4.3.1 Desarrollador 1 - Full Stack

**Perfil:** Desarrollador Full Stack con experiencia en backend y frontend

**Especializaciones:**
- Backend: Python, FastAPI
- Frontend: Vue.js, JavaScript
- Base de Datos: PostgreSQL
- Integración: APIs RESTful

**Responsabilidades Principales:**

**Backend:**
- Implementó estructura base de FastAPI.
- Desarrolló routers para estudiantes, cursos e instructores.
- Configuró conexión a Supabase.
- Implementó modelos Pydantic para validación.

**Frontend:**
- Creó componentes Vue 3 reutilizables.
- Implementó vista de administrador con tabs.
- Desarrolló formularios con validación.
- Configuró Vue Router.

**Integración:**
- Integró frontend con backend (Axios).
- Implementó manejo de errores en comunicación.
- Configuró CORS en backend.

**Tareas Específicas en EduRAG:**
- ✅ Sprint 1: Setup inicial de proyectos backend y frontend.
- ✅ Sprint 2: CRUD de estudiantes y cursos (backend + frontend).
- ✅ Sprint 3: CRUD de instructores y materiales (formularios).
- ✅ Sprint 5: Vista de administrador completa.
- ✅ Sprint 6: Integración y testing.

**Contribución:** ~35% del código total

---

#### 4.3.2 Desarrollador 2 - Backend/IA Specialist

**Perfil:** Desarrollador Backend con especialización en Inteligencia Artificial

**Especializaciones:**
- Backend: Python, FastAPI, async/await
- IA: OpenAI API, LangChain, embeddings
- Base de Datos: PostgreSQL, pgvector
- Procesamiento: PDFs, chunking, vectorización

**Responsabilidades Principales:**

**Motor RAG:**
- Implementó procesamiento de PDFs con pdfplumber.
- Desarrolló sistema de chunking con LangChain.
- Integró OpenAI API para embeddings y chat.
- Implementó búsqueda vectorial con pgvector.

**Base de Datos:**
- Diseñó esquema de base de datos con pgvector.
- Creó función SQL `match_material_chunks`.
- Configuró índice HNSW para performance.
- Implementó migraciones y scripts SQL.

**Optimización:**
- Optimizó queries de búsqueda vectorial.
- Implementó manejo de errores en procesamiento de PDFs.
- Ajustó thresholds de similitud.

**Tareas Específicas en EduRAG:**
- ✅ Sprint 3: Procesamiento de PDFs y chunking.
- ✅ Sprint 3: Generación de embeddings con OpenAI.
- ✅ Sprint 4: Búsqueda vectorial y función SQL.
- ✅ Sprint 4: Integración completa del motor RAG.
- ✅ Sprint 4: Generación de respuestas con GPT-4.
- ✅ Sprint 6: Optimización de performance.

**Contribución:** ~35% del código total (funcionalidad más compleja)

---

#### 4.3.3 Desarrollador 3 - Frontend/UX

**Perfil:** Desarrollador Frontend con enfoque en experiencia de usuario

**Especializaciones:**
- Frontend: Vue 3, Composition API
- Estilos: Tailwind CSS, diseño responsivo
- UX: Diseño de interfaces, usabilidad
- Estado: Reactive state management

**Responsabilidades Principales:**

**Interfaces de Usuario:**
- Diseñó y desarrolló vista de estudiante.
- Creó interfaz de chat inteligente.
- Implementó vista de director con dashboard.
- Diseñó componentes visuales (cards, tables, forms).

**Estilos y Responsividad:**
- Aplicó Tailwind CSS en todos los componentes.
- Aseguró diseño responsivo (desktop, tablet, móvil).
- Implementó animaciones y transiciones.
- Mantuvo consistencia visual en todo el sistema.

**Experiencia de Usuario:**
- Diseñó flujos de usuario intuitivos.
- Implementó feedback visual (loading states, mensajes).
- Optimizó navegación entre vistas.
- Realizó pruebas de usabilidad.

**Tareas Específicas en EduRAG:**
- ✅ Sprint 5: Vista de estudiante con lista de cursos.
- ✅ Sprint 5: Interfaz de chat con IA (diseño y lógica).
- ✅ Sprint 5: Vista de director con dashboard.
- ✅ Sprint 5: Componentes de análisis (métricas, tarjetas).
- ✅ Sprint 6: Refinamiento de estilos y responsividad.
- ✅ Sprint 6: Testing de usabilidad.

**Contribución:** ~30% del código total

---

## 5. Distribución de Responsabilidades

### 5.1 Matriz de Responsabilidades (RACI)

| Actividad | Product Owner | Scrum Master | Dev 1 | Dev 2 | Dev 3 |
|-----------|---------------|--------------|-------|-------|-------|
| **Planificación** |
| Definir visión del producto | A | C | I | I | I |
| Crear Product Backlog | A | C | I | I | I |
| Priorizar funcionalidades | A | C | C | C | C |
| Estimar user stories | C | I | R | R | R |
| Planificar sprints | C | R | R | R | R |
| **Desarrollo** |
| Arquitectura del sistema | C | I | R | R | C |
| Desarrollo backend base | I | I | R | R | I |
| Motor RAG e IA | I | I | I | A | I |
| Desarrollo frontend | I | I | R | I | A |
| Base de datos | I | I | C | A | I |
| Testing | I | I | R | R | R |
| **Gestión** |
| Facilitar ceremonias | I | A | R | R | R |
| Remover impedimentos | C | A | I | I | I |
| Reportar progreso | I | R | I | I | I |
| Gestionar tablero Scrum | I | A | R | R | R |
| **Calidad** |
| Definir criterios aceptación | A | C | C | C | C |
| Code reviews | I | I | R | R | R |
| Validar funcionalidades | A | I | I | I | I |
| Documentación técnica | C | R | R | R | R |
| Documentación académica | A | R | R | R | R |

**Leyenda:**
- **R (Responsible):** Ejecuta la tarea
- **A (Accountable):** Responsable final, toma decisión
- **C (Consulted):** Consultado, provee input
- **I (Informed):** Informado de resultados

---

## 6. Sprints del Proyecto

### 6.1 Calendario de Sprints

**Duración Total del Proyecto:** 12 semanas  
**Número de Sprints:** 6  
**Duración de cada Sprint:** 2 semanas

### 6.2 Detalle de Sprints

#### Sprint 0: Preparación (Semanas 1-2)

**Sprint Goal:** Configurar entornos y definir arquitectura

**User Stories Completadas:**
- Como equipo, necesitamos configurar repositorio Git para control de versiones.
- Como equipo, necesitamos definir arquitectura del sistema.
- Como equipo, necesitamos diseñar esquema de base de datos.
- Como equipo, necesitamos configurar entornos de desarrollo (backend y frontend).

**Responsables Principales:**
- Dev 1: Setup de proyectos (FastAPI + Vue)
- Dev 2: Diseño de base de datos con pgvector
- Dev 3: Mockups de interfaces

**Entregables:**
- ✅ Repositorio GitHub configurado
- ✅ Diagrama de arquitectura
- ✅ Diagrama ER de base de datos
- ✅ Proyectos base corriendo localmente

**Retrospectiva:**
- ✅ **Lo que salió bien:** Buena colaboración, arquitectura bien definida.
- ⚠️ **Mejora:** Configuración de pgvector tomó más tiempo del esperado.

---

#### Sprint 1: Backend Base (Semanas 3-4)

**Sprint Goal:** Implementar estructura backend y primeros endpoints

**User Stories Completadas:**
- Como administrador, quiero crear estudiantes para gestionar usuarios del sistema.
- Como administrador, quiero listar estudiantes para ver todos los registros.
- Como administrador, quiero crear cursos para organizar contenido educativo.
- Como administrador, quiero listar cursos para ver oferta académica.

**Responsables Principales:**
- Dev 1: Routers de estudiantes y cursos
- Dev 2: Modelos Pydantic, conexión Supabase
- Dev 3: Apoyo en testing de endpoints

**Entregables:**
- ✅ Endpoints: POST/GET /api/students
- ✅ Endpoints: POST/GET /api/courses
- ✅ Validación con Pydantic
- ✅ Documentación Swagger

**Velocity:** 21 story points

**Retrospectiva:**
- ✅ **Lo que salió bien:** Estructura modular facilita desarrollo.
- ⚠️ **Mejora:** Necesitamos más pruebas unitarias.

---

#### Sprint 2: CRUD Completo (Semanas 5-6)

**Sprint Goal:** Completar operaciones CRUD para todas las entidades principales

**User Stories Completadas:**
- Como administrador, quiero actualizar y eliminar estudiantes.
- Como administrador, quiero actualizar y eliminar cursos.
- Como administrador, quiero gestionar instructores (CRUD completo).
- Como administrador, quiero gestionar inscripciones de estudiantes a cursos.

**Responsables Principales:**
- Dev 1: CRUD de instructores
- Dev 2: Lógica de inscripciones con validaciones
- Dev 3: Apoyo en testing

**Entregables:**
- ✅ CRUD completo: students, courses, instructors
- ✅ Módulo de inscripciones operativo
- ✅ Validaciones de integridad referencial
- ✅ Pruebas unitarias (cobertura 60%)

**Velocity:** 26 story points

**Retrospectiva:**
- ✅ **Lo que salió bien:** Velocity aumentó, equipo más sincronizado.
- ✅ **Mejora aplicada:** Implementamos code reviews obligatorios.

---

#### Sprint 3: Gestión de Materiales (Semanas 7-8)

**Sprint Goal:** Implementar carga y procesamiento de PDFs

**User Stories Completadas:**
- Como administrador, quiero subir PDFs para agregar material educativo.
- Como sistema, necesito extraer texto de PDFs automáticamente.
- Como sistema, necesito dividir PDFs en chunks para búsqueda eficiente.
- Como sistema, necesito generar embeddings de chunks para búsqueda semántica.

**Responsables Principales:**
- Dev 2: **Líder** - Procesamiento completo de PDFs
- Dev 1: Endpoints de carga y listado de materiales
- Dev 3: Apoyo en testing

**Entregables:**
- ✅ Endpoint: POST /api/materials (carga de PDF)
- ✅ Procesamiento automático con pdfplumber
- ✅ Chunking con LangChain (RecursiveCharacterTextSplitter)
- ✅ Generación de embeddings con OpenAI
- ✅ Almacenamiento en tabla material_chunks

**Velocity:** 34 story points (sprint más complejo)

**Retrospectiva:**
- ✅ **Lo que salió bien:** Dev 2 mostró gran expertise en IA.
- ⚠️ **Desafío:** Límites de OpenAI API requirieron implementar retry logic.

---

#### Sprint 4: Motor RAG (Semanas 9-10)

**Sprint Goal:** Implementar chat inteligente completo

**User Stories Completadas:**
- Como estudiante, quiero hacer preguntas en lenguaje natural sobre el curso.
- Como sistema, necesito buscar fragmentos relevantes usando búsqueda vectorial.
- Como sistema, necesito generar respuestas contextualizadas con GPT-4.
- Como estudiante, quiero recibir respuestas precisas basadas en el material.

**Responsables Principales:**
- Dev 2: **Líder** - Búsqueda vectorial y generación de respuestas
- Dev 1: Endpoint de chat en backend
- Dev 3: Apoyo en lógica

**Entregables:**
- ✅ Función SQL match_material_chunks con pgvector
- ✅ Índice HNSW para búsquedas rápidas
- ✅ Endpoint: POST /api/rag/chat
- ✅ Integración con GPT-4o-mini
- ✅ Manejo de casos sin información relevante
- ✅ Prompts optimizados

**Velocity:** 38 story points (sprint crítico)

**Retrospectiva:**
- ✅ **Lo que salió bien:** Motor RAG funciona perfectamente, respuestas de alta calidad.
- ✅ **Mejora aplicada:** Optimizamos threshold de similitud (0.3).

---

#### Sprint 5: Frontend Completo (Semanas 11-12)

**Sprint Goal:** Desarrollar todas las vistas del sistema

**User Stories Completadas:**
- Como administrador, quiero una interfaz de gestión completa.
- Como estudiante, quiero ver mis cursos y usar el chat inteligente.
- Como director, quiero ver dashboard con métricas del sistema.
- Como usuario, quiero interfaz intuitiva y responsiva.

**Responsables Principales:**
- Dev 3: **Líder** - Todas las vistas y componentes
- Dev 1: Integración frontend-backend (Axios)
- Dev 2: Apoyo en lógica de chat

**Entregables:**
- ✅ Vista de Administrador con tabs (8 secciones)
- ✅ Vista de Estudiante con chat interactivo
- ✅ Vista de Director con dashboard
- ✅ Componentes reutilizables (forms, tables, cards)
- ✅ Diseño responsivo con Tailwind CSS
- ✅ Router con navegación fluida

**Velocity:** 42 story points (sprint más productivo)

**Retrospectiva:**
- ✅ **Lo que salió bien:** Frontend quedó muy pulido, UX excelente.
- ✅ **Elogio:** Dev 3 mostró gran talento en diseño de interfaces.

---

#### Sprint 6: Testing y Documentación (Semanas 13-14)

**Sprint Goal:** Asegurar calidad y documentar exhaustivamente

**User Stories Completadas:**
- Como equipo, necesitamos probar todos los flujos end-to-end.
- Como equipo, necesitamos documentar técnicamente el sistema.
- Como usuario, necesito manual de uso del sistema.
- Como desarrollador futuro, necesito documentación de arquitectura.

**Responsables Principales:**
- Todo el equipo: Testing colaborativo
- Dev 1: Documentación de backend
- Dev 2: Documentación de RAG
- Dev 3: Manual de usuario

**Entregables:**
- ✅ Pruebas end-to-end de todos los módulos
- ✅ Corrección de bugs encontrados
- ✅ Documentación técnica (+11,000 líneas)
- ✅ Documentación académica (+6,000 líneas)
- ✅ README.md con manual de usuario
- ✅ Sistema desplegado en ambiente de pruebas

**Velocity:** 29 story points

**Retrospectiva Final:**
- ✅ **Lo que salió bien:** Proyecto completado al 100%, documentación exhaustiva.
- ✅ **Logro:** Sistema funcional y listo para presentación académica.
- 🎉 **Celebración:** Equipo cumplió todos los objetivos.

---

## 7. Herramientas Utilizadas

### 7.1 Gestión de Proyecto

**Trello / Jira:**
- Product Backlog con user stories priorizadas.
- Sprint Backlog con tareas del sprint actual.
- Board con columnas: To Do, In Progress, Review, Done.
- Estimación en story points.

**Google Drive:**
- Documentos compartidos.
- Actas de reuniones.
- Retrospectivas documentadas.

### 7.2 Desarrollo

**VS Code:**
- IDE principal para todo el equipo.
- Extensiones: Python, Volar (Vue), Prettier, ESLint.

**Git / GitHub:**
- Control de versiones.
- Branches por feature (opcional).
- Pull requests con code reviews.

**Postman:**
- Testing de API durante desarrollo.
- Colecciones de endpoints.

### 7.3 Comunicación

**WhatsApp / Discord:**
- Comunicación diaria informal.
- Notificaciones de bloqueos.

**Google Meet / Zoom:**
- Daily standups virtuales.
- Sprint Planning y Reviews.
- Pair programming remoto.

---

## 8. Métricas del Equipo

### 8.1 Velocity por Sprint

| Sprint | Story Points Completados | Velocity |
|--------|--------------------------|----------|
| Sprint 1 | 21 | 21 |
| Sprint 2 | 26 | 23.5 (promedio) |
| Sprint 3 | 34 | 27 (promedio) |
| Sprint 4 | 38 | 29.75 (promedio) |
| Sprint 5 | 42 | 32.2 (promedio) |
| Sprint 6 | 29 | 31.67 (promedio) |
| **Total** | **190 story points** | **Velocity final: ~32** |

**Análisis:**
- Velocity aumentó consistentemente (equipo mejorando).
- Sprint 5 fue el más productivo (frontend).
- Sprint 3 y 4 fueron complejos (IA) pero exitosos.

### 8.2 Burndown Chart (Ejemplo Sprint 4)

```
Story Points
40 │ ●
   │   ●
35 │     ●
   │       ●
30 │         ●
   │           ●
25 │             ●
   │               ●
20 │                 ●
   │                   ●
15 │                     ●
   │                       ●
10 │                         ●
   │                           ●
5  │                             ●
   │                               ●
0  └─────────────────────────────────●
   Día 1  2  3  4  5  6  7  8  9  10

   ● Trabajo Restante
```

**Interpretación:** Burndown ideal, trabajo completado de manera consistente.

### 8.3 Cumplimiento de Sprints

| Métrica | Valor |
|---------|-------|
| Sprints planificados | 6 |
| Sprints completados exitosamente | 6 (100%) |
| User stories comprometidas | 45 |
| User stories completadas | 44 (98%) |
| User stories movidas a siguiente sprint | 1 (2%) |

---

## 9. Comunicación y Colaboración

### 9.1 Daily Standups

**Formato utilizado:**

**Desarrollador 1:**
- **Ayer:** Implementé CRUD de estudiantes en backend.
- **Hoy:** Trabajaré en formulario de estudiantes en frontend.
- **Impedimentos:** Ninguno.

**Desarrollador 2:**
- **Ayer:** Configuré pgvector en Supabase.
- **Hoy:** Implementaré función de búsqueda vectorial.
- **Impedimentos:** Necesito ayuda para entender sintaxis de operadores pgvector.

**Desarrollador 3:**
- **Ayer:** Diseñé mockups de vista de estudiante.
- **Hoy:** Comenzaré a implementar interfaz de chat.
- **Impedimentos:** Ninguno.

**Scrum Master:**
- **Acción:** Programaré sesión de pair programming entre Dev 1 y Dev 2 para resolver duda de pgvector.

### 9.2 Code Reviews

**Proceso implementado:**

1. Desarrollador completa funcionalidad en branch.
2. Crea pull request con descripción clara.
3. Otro desarrollador revisa código (mínimo 1 aprobación requerida).
4. Se hacen comentarios o sugerencias.
5. Desarrollador original ajusta si es necesario.
6. Se aprueba y hace merge a main.

**Beneficios observados:**
- Detección temprana de bugs.
- Compartir conocimiento entre equipo.
- Código más consistente y limpio.

---

## 10. Lecciones Aprendidas

### 10.1 Éxitos del Equipo

✅ **Colaboración Excepcional:**
- Equipo altamente colaborativo y comunicativo.
- Pair programming ayudó a resolver problemas complejos (especialmente en motor RAG).

✅ **Especialización Efectiva:**
- Cada desarrollador aprovechó sus fortalezas (full stack, IA, UX).
- División de trabajo eficiente sin generar silos.

✅ **Adaptación Ágil:**
- Equipo respondió bien a cambios (ej: ajustar threshold de similitud).
- Retrospectivas generaron mejoras reales en sprints siguientes.

✅ **Documentación Exhaustiva:**
- Decisión de documentar desde inicio facilitó entregables finales.
- Documentación paralela al desarrollo evitó deuda técnica documental.

### 10.2 Desafíos Superados

⚠️ **Curva de Aprendizaje de pgvector:**
- **Desafío:** Ningún miembro tenía experiencia previa con búsqueda vectorial.
- **Solución:** Dev 2 invirtió tiempo en research y experimentación. Pair programming con Dev 1 aceleró aprendizaje.

⚠️ **Límites de OpenAI API:**
- **Desafío:** Excedimos rate limits en desarrollo.
- **Solución:** Implementamos retry logic y usamos caché para embeddings ya generados.

⚠️ **Coordinación de Horarios:**
- **Desafío:** Equipo con horarios académicos variados.
- **Solución:** Daily standups flexibles (asíncronos cuando necesario), documentación clara en Trello.

### 10.3 Mejoras para Futuros Proyectos

💡 **Testing Desde el Inicio:**
- Implementar TDD (Test-Driven Development) desde Sprint 1.
- Objetivo: >80% cobertura de código.

💡 **CI/CD Pipeline:**
- Configurar GitHub Actions para tests automáticos en cada PR.
- Deploy automático a staging en cada merge a main.

💡 **Más Pair Programming:**
- Programar sesiones regulares de pair programming.
- Especialmente útil para funcionalidades complejas.

---

## 11. Reconocimientos del Equipo

### 11.1 MVP (Most Valuable Player)

**🏆 Desarrollador 2 - Backend/IA Specialist**

**Reconocimiento:**
Por liderazgo técnico en la implementación del motor RAG, la funcionalidad más compleja e innovadora del sistema. Su expertise en IA y persistencia para dominar pgvector fueron fundamentales para el éxito del proyecto.

**Contribuciones destacadas:**
- Implementó completamente el pipeline RAG (procesamiento, embeddings, búsqueda, generación).
- Optimizó performance de búsquedas vectoriales con índices HNSW.
- Documentó exhaustivamente la implementación de RAG.

### 11.2 Menciones Honoríficas

**🌟 Desarrollador 3 - Frontend/UX**

**Reconocimiento:**
Por crear una interfaz excepcionalmente intuitiva y visualmente atractiva. Su enfoque en UX resultó en un sistema que no requiere capacitación para usuarios finales.

**🌟 Desarrollador 1 - Full Stack**

**Reconocimiento:**
Por versatilidad y capacidad de trabajar en todas las capas del sistema. Su habilidad para integrar frontend y backend fue crucial para la cohesión del proyecto.

**🌟 Scrum Master**

**Reconocimiento:**
Por excelente facilitación del proceso Scrum y remoción efectiva de impedimentos. Su organización mantuvo al equipo enfocado y productivo durante todo el proyecto.

**🌟 Product Owner**

**Reconocimiento:**
Por visión clara del producto y priorización efectiva de funcionalidades. Su feedback continuo aseguró que el sistema cumpliera expectativas académicas y técnicas.

---

## 12. Conclusiones

### 12.1 Éxito del Equipo

El equipo de desarrollo de **EduRAG** demostró ser altamente efectivo, completando el proyecto al **100%** en el tiempo estimado. La metodología Scrum fue fundamental para:

- ✅ Mantener enfoque en objetivos del sprint.
- ✅ Adaptarse rápidamente a desafíos técnicos.
- ✅ Mantener comunicación fluida entre miembros.
- ✅ Entregar incrementos funcionales regularmente.

### 12.2 Aplicación de Scrum

La implementación de Scrum en este proyecto académico fue **ejemplar**:

- ✅ Todas las ceremonias se ejecutaron consistentemente.
- ✅ Roles y responsabilidades fueron respetados.
- ✅ Velocity mejoró progresivamente.
- ✅ Retrospectivas generaron mejoras reales.

### 12.3 Preparación Profesional

Este proyecto preparó al equipo para entornos profesionales:

- ✅ Experiencia con metodologías ágiles (Scrum).
- ✅ Trabajo en equipo multidisciplinario.
- ✅ Gestión de proyecto completo end-to-end.
- ✅ Tecnologías modernas (IA, cloud, frameworks actuales).

---

**Documento de Grupo de Trabajo y Roles - EduRAG**  
**Análisis de Sistemas II**  
**Octubre 2025**  
**Estado: Proyecto Completado Exitosamente por Equipo Scrum** ✅

---

## Anexo: Tablero Scrum (Ejemplo)

```
╔══════════════╦══════════════╦══════════════╦══════════════╗
║   BACKLOG    ║   TO DO      ║ IN PROGRESS  ║     DONE     ║
╠══════════════╬══════════════╬══════════════╬══════════════╣
║ [US-45]      ║ [US-12]      ║ [US-08]      ║ [US-01] ✓    ║
║ Notificaciones║ Dashboard   ║ Chat UI      ║ CRUD Students║
║ (Futuro)     ║ Director     ║ (Dev 3)      ║              ║
║              ║              ║              ║ [US-02] ✓    ║
║ [US-46]      ║ [US-13]      ║ [US-09]      ║ CRUD Courses ║
║ Calificaciones║ Métricas    ║ RAG Backend  ║              ║
║ (Futuro)     ║ Avanzadas    ║ (Dev 2)      ║ [US-03] ✓    ║
║              ║              ║              ║ PDF Upload   ║
╚══════════════╩══════════════╩══════════════╩══════════════╝
```

*Fin del Documento de Grupo de Trabajo*
