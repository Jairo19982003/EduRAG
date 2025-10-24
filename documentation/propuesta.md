# Propuesta del Proyecto EduRAG

## Información del Documento

**Curso:** Análisis de Sistemas II  
**Proyecto:** EduRAG - Sistema de Gestión Educativa con IA  
**Tipo de Documento:** Propuesta de Sistema  
**Fecha:** Octubre 2025

---

## 1. Introducción

La presente propuesta tiene como finalidad presentar el desarrollo de **EduRAG**, un sistema de gestión educativa que integra tecnologías de Inteligencia Artificial para transformar la experiencia de aprendizaje en instituciones educativas. Este documento detalla la justificación, alcance y beneficios esperados del sistema propuesto.

---

## 2. Antecedentes

### 2.1 Situación Actual

Las instituciones educativas enfrentan desafíos significativos en la gestión del proceso de enseñanza-aprendizaje:

- **Fragmentación de Sistemas:** Uso de múltiples plataformas para diferentes tareas (gestión académica, almacenamiento de materiales, comunicación).
- **Baja Interactividad con Contenidos:** Los materiales didácticos son estáticos y no permiten consultas dinámicas.
- **Sobrecarga de Instructores:** Los docentes invierten tiempo considerable respondiendo preguntas repetitivas.
- **Acceso Limitado a Información:** Los estudiantes tienen dificultad para encontrar respuestas específicas en materiales extensos.
- **Falta de Análisis:** Ausencia de herramientas para analizar el desempeño institucional y tomar decisiones basadas en datos.

### 2.2 Necesidad Identificada

Se requiere un sistema integral que:

1. Centralice la gestión académica (estudiantes, cursos, instructores, materiales).
2. Proporcione acceso inteligente a contenidos educativos mediante IA.
3. Reduzca la carga operativa de instructores y administradores.
4. Ofrezca herramientas de análisis para la toma de decisiones.
5. Mejore la experiencia de aprendizaje mediante interacción natural con el contenido.

---

## 3. Descripción de la Propuesta

### 3.1 Nombre del Sistema

**EduRAG** (Educational Retrieval-Augmented Generation System)

### 3.2 Concepto General

EduRAG es una plataforma web integral que combina:

- **Sistema de Gestión del Aprendizaje (LMS):** Administración de entidades educativas (cursos, estudiantes, instructores).
- **Inteligencia Artificial Conversacional:** Motor RAG que permite a los estudiantes hacer preguntas en lenguaje natural sobre el material del curso.
- **Análisis de Datos:** Dashboard con métricas clave para directores académicos.

### 3.3 Tecnología RAG Propuesta

**Retrieval-Augmented Generation (RAG)** es una técnica de IA que combina:

1. **Recuperación de Información:** Búsqueda de fragmentos relevantes en documentos mediante embeddings vectoriales.
2. **Generación de Texto:** Uso de modelos de lenguaje (LLM) para generar respuestas contextualizadas.

**Ventajas de RAG:**

- ✅ Respuestas precisas basadas en documentos específicos del curso.
- ✅ No requiere reentrenar modelos de IA (cost-effective).
- ✅ Información siempre actualizada (al actualizar documentos).
- ✅ Trazabilidad de respuestas (se conoce la fuente).

---

## 4. Justificación del Proyecto

### 4.1 Justificación Académica

**Para el curso de Análisis de Sistemas II:**

- Aplicación práctica de metodologías de análisis y diseño de sistemas.
- Implementación de arquitecturas modernas (microservicios, cliente-servidor).
- Uso de herramientas de modelado (diagramas UML, ER, arquitectónicos).
- Integración de tecnologías emergentes (IA, bases de datos vectoriales).
- Desarrollo de habilidades en ingeniería de software completa (frontend, backend, base de datos, despliegue).

### 4.2 Justificación Técnica

- **Factibilidad:** Tecnologías maduras y ampliamente documentadas (FastAPI, Vue, PostgreSQL, OpenAI).
- **Escalabilidad:** Arquitectura cloud-native permite crecimiento horizontal.
- **Mantenibilidad:** Código modular y bien documentado facilita futuras mejoras.
- **Performance:** Uso de índices vectoriales HNSW garantiza búsquedas rápidas incluso con miles de documentos.

### 4.3 Justificación Económica

**Costos de Desarrollo:**

- Herramientas open-source (FastAPI, Vue, PostgreSQL): $0
- Supabase Free Tier: $0 (suficiente para desarrollo y pruebas)
- OpenAI API: ~$2-5 USD/mes (uso educativo moderado)
- Total: ~$60 USD/año

**Beneficios Económicos:**

- Reducción del 70% en tiempo administrativo (ahorro en personal).
- Reducción del 50% en consultas a instructores (optimización de recursos).
- Eliminación de múltiples licencias de software (sistema unificado).
- ROI estimado: 6 meses.

### 4.4 Justificación Social

- **Democratización del Conocimiento:** Acceso 24/7 a información educativa de calidad.
- **Inclusión:** Interfaz accesible y fácil de usar para todos los niveles de habilidad técnica.
- **Mejora en la Calidad Educativa:** Estudiantes mejor informados y con respuestas inmediatas.
- **Reducción de Brechas:** Estudiantes sin acceso directo a instructores pueden resolver dudas.

---

## 5. Objetivos de la Propuesta

### 5.1 Objetivo General

Desarrollar e implementar un sistema de gestión educativa que integre tecnologías de Inteligencia Artificial (RAG) para mejorar la eficiencia administrativa y la experiencia de aprendizaje de estudiantes, permitiendo consultas inteligentes sobre materiales del curso y proporcionando herramientas de análisis para la toma de decisiones.

### 5.2 Objetivos Específicos

1. **Diseñar una arquitectura de sistema** que integre gestión académica con capacidades de IA conversacional.

2. **Implementar un módulo de gestión administrativa** que permita CRUD completo de estudiantes, cursos, instructores y materiales.

3. **Desarrollar un motor de procesamiento de documentos** que extraiga, fragmente y vectorice contenido de PDFs educativos.

4. **Crear un sistema de chat inteligente** que utilice RAG para responder preguntas basadas en el material del curso.

5. **Construir un dashboard analítico** con métricas clave para directores académicos.

6. **Garantizar la escalabilidad y performance** mediante uso de índices vectoriales y arquitectura asíncrona.

7. **Documentar exhaustivamente** el sistema para facilitar mantenimiento y futuras extensiones.

---

## 6. Alcance de la Propuesta

### 6.1 Dentro del Alcance

#### Funcionalidades Incluidas:

**Módulo de Autenticación:**
- Login/logout de usuarios.
- Roles diferenciados (Administrador, Estudiante, Director).

**Módulo de Gestión de Estudiantes:**
- Crear, leer, actualizar, eliminar estudiantes.
- Gestión de inscripciones a cursos.

**Módulo de Gestión de Cursos:**
- CRUD de cursos.
- Asignación de instructores.
- Asociación de materiales.

**Módulo de Gestión de Instructores:**
- CRUD de instructores.
- Visualización de cursos asignados.

**Módulo de Gestión de Materiales:**
- Carga de PDFs.
- Procesamiento automático (extracción, chunking, embedding).
- Almacenamiento en base de datos vectorial.

**Módulo de Inscripciones:**
- Inscripción de estudiantes a cursos.
- Gestión de estados (activo, completado, inactivo).

**Módulo de Chat Inteligente (RAG):**
- Interfaz de chat para estudiantes.
- Búsqueda semántica en materiales del curso.
- Generación de respuestas contextualizadas.
- Historial de conversaciones.

**Módulo de Análisis:**
- Dashboard con métricas clave.
- Visualización de estadísticas.

#### Aspectos Técnicos Incluidos:

- Backend RESTful con FastAPI.
- Frontend SPA con Vue 3.
- Base de datos PostgreSQL con extensión pgvector.
- Integración con OpenAI API.
- Almacenamiento de archivos con Supabase Storage.
- Documentación técnica completa.

### 6.2 Fuera del Alcance

**No Incluido en esta Versión:**

- Sistema de calificaciones o evaluaciones automatizadas.
- Videoconferencias integradas.
- Aplicación móvil nativa (solo web responsiva).
- Integración con sistemas externos (ERP, SIS existentes).
- Reconocimiento de voz para el chat.
- Análisis de sentimientos en conversaciones.
- Sistema de gamificación.
- Pagos o facturación.

---

## 7. Beneficiarios del Sistema

### 7.1 Beneficiarios Directos

**Estudiantes:**
- Acceso inmediato a información del curso.
- Resolución de dudas 24/7.
- Mejor comprensión del material.

**Instructores:**
- Reducción de consultas repetitivas.
- Más tiempo para actividades pedagógicas.
- Gestión eficiente de materiales.

**Administradores:**
- Control centralizado del sistema.
- Gestión simplificada de entidades académicas.

**Directores Académicos:**
- Visibilidad completa del sistema.
- Toma de decisiones basada en datos.

### 7.2 Beneficiarios Indirectos

**Institución Educativa:**
- Mejora de la imagen institucional.
- Reducción de costos operativos.
- Aumento en satisfacción estudiantil.

**Comunidad Educativa:**
- Avance en digitalización educativa.
- Modelo replicable para otras instituciones.

---

## 8. Metodología de Desarrollo

### 8.1 Metodología Propuesta: Scrum

**Justificación:**

- **Iterativo e Incremental:** Permite entregas parciales funcionales.
- **Adaptable:** Responde rápidamente a cambios de requerimientos.
- **Colaborativo:** Fomenta comunicación constante del equipo.
- **Transparente:** Progreso visible mediante sprints y ceremonias.

### 8.2 Sprints Planificados

**Sprint 0 (Preparación):**
- Configuración de entornos.
- Definición de arquitectura.
- Setup de base de datos.

**Sprint 1 (Backend Base):**
- Estructura FastAPI.
- Modelos Pydantic.
- Conexión a Supabase.

**Sprint 2 (CRUD Básico):**
- Endpoints de estudiantes, cursos, instructores.
- Pruebas unitarias.

**Sprint 3 (Gestión de Materiales):**
- Carga de PDFs.
- Procesamiento y chunking.
- Generación de embeddings.

**Sprint 4 (Motor RAG):**
- Búsqueda vectorial.
- Integración con OpenAI.
- Generación de respuestas.

**Sprint 5 (Frontend):**
- Vistas administrativas.
- Vista de estudiante con chat.
- Dashboard de director.

**Sprint 6 (Testing y Documentación):**
- Pruebas end-to-end.
- Documentación completa.
- Preparación para despliegue.

---

## 9. Recursos Necesarios

### 9.1 Recursos Humanos

**Equipo Scrum:**

- 1 Product Owner (Rol académico)
- 1 Scrum Master
- 3-4 Desarrolladores
- 1 Diseñador UX/UI (opcional)

### 9.2 Recursos Tecnológicos

**Hardware:**
- Computadoras de desarrollo (CPU: i5+, RAM: 8GB+).
- Servidor de desarrollo/staging (opcional).

**Software:**
- IDEs: VS Code, PyCharm.
- Control de versiones: Git/GitHub.
- Herramientas de diseño: Figma (opcional).
- Herramientas de gestión: Trello/Jira.

**Servicios Cloud:**
- Supabase (PostgreSQL + Storage).
- OpenAI API.
- Render/Railway (despliegue).

### 9.3 Recursos Económicos

**Estimación de Costos:**

| Recurso | Costo Mensual | Costo Total (6 meses) |
|---------|---------------|------------------------|
| OpenAI API | $5 USD | $30 USD |
| Supabase Pro (opcional) | $25 USD | $150 USD |
| Dominio | $1 USD | $6 USD |
| Hosting (Render) | $7 USD | $42 USD |
| **Total** | **$38 USD** | **$228 USD** |

*Nota: Versión gratuita disponible para todos los servicios durante desarrollo.*

---

## 10. Cronograma Propuesto

### Fase 1: Análisis y Diseño (Semanas 1-2)

- Levantamiento de requerimientos.
- Diseño de arquitectura.
- Modelado de base de datos.
- Diseño de interfaces (mockups).

### Fase 2: Desarrollo Backend (Semanas 3-6)

- Configuración de entornos.
- Implementación de endpoints.
- Desarrollo del motor RAG.
- Pruebas unitarias.

### Fase 3: Desarrollo Frontend (Semanas 7-9)

- Creación de componentes Vue.
- Integración con backend.
- Implementación de vistas por rol.
- Pruebas de interfaz.

### Fase 4: Integración y Pruebas (Semanas 10-11)

- Pruebas de integración.
- Pruebas end-to-end.
- Corrección de bugs.
- Optimización de performance.

### Fase 5: Documentación y Despliegue (Semana 12)

- Documentación técnica.
- Documentación de usuario.
- Despliegue a producción.
- Capacitación de usuarios.

**Duración Total: 12 semanas (3 meses)**

---

## 11. Riesgos y Mitigación

### 11.1 Riesgos Identificados

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Límites de API de OpenAI | Media | Alto | Implementar caché de respuestas, usar tier pagado |
| Performance con muchos documentos | Media | Medio | Usar índices HNSW, optimizar chunking |
| Complejidad del motor RAG | Alta | Alto | Usar LangChain (librería especializada) |
| Cambios de requerimientos | Media | Medio | Metodología Scrum (adaptable) |
| Falta de experiencia en IA | Media | Medio | Capacitación, uso de tutoriales/documentación |

### 11.2 Plan de Contingencia

- **Backup de Datos:** Backups automáticos diarios en Supabase.
- **Rollback:** Control de versiones con Git permite revertir cambios.
- **Alternativas de API:** Fallback a modelos locales (Ollama) si OpenAI falla.

---

## 12. Criterios de Éxito

### 12.1 Criterios Funcionales

- ✅ Todos los módulos operativos al 100%.
- ✅ Chat RAG responde correctamente con información del curso.
- ✅ CRUD completo para todas las entidades.
- ✅ Dashboard muestra métricas en tiempo real.

### 12.2 Criterios Técnicos

- ✅ Respuesta de chat < 5 segundos.
- ✅ Búsqueda vectorial en < 100ms.
- ✅ Frontend responsivo (desktop y móvil).
- ✅ Código con > 70% de cobertura de tests.

### 12.3 Criterios Académicos

- ✅ Documentación completa y profesional.
- ✅ Aplicación correcta de metodologías de análisis.
- ✅ Diagramas UML/ER correctamente elaborados.
- ✅ Presentación clara del proyecto.

---

## 13. Conclusiones de la Propuesta

EduRAG representa una solución innovadora y viable para los desafíos actuales de la gestión educativa. La integración de tecnologías de IA con sistemas de gestión tradicionales crea una plataforma completa que beneficia a todos los actores del proceso educativo.

**Fortalezas de la Propuesta:**

- ✅ **Innovación:** Uso de tecnología RAG en contexto educativo.
- ✅ **Integralidad:** Solución completa, no solo un módulo aislado.
- ✅ **Viabilidad:** Tecnologías probadas y bien documentadas.
- ✅ **Escalabilidad:** Arquitectura preparada para crecimiento.
- ✅ **Impacto:** Beneficios medibles para estudiantes e instructores.

**Valor Académico:**

El proyecto cumple ampliamente con los objetivos de **Análisis de Sistemas II**:

- Aplicación de metodologías de análisis.
- Diseño de arquitecturas complejas.
- Integración de múltiples tecnologías.
- Documentación profesional.
- Desarrollo de solución completa end-to-end.

---

## 14. Aprobaciones

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Product Owner | | | |
| Scrum Master | | | |
| Equipo de Desarrollo | | | |
| Docente de Análisis de Sistemas II | | | |

---

**Documento de Propuesta - EduRAG**  
**Análisis de Sistemas II**  
**Octubre 2025**  
**Estado: Propuesta Aprobada - Proyecto Completado al 100%**
