# 🎨 Guía de Desarrollo del Frontend - EduRAG

## 📋 Contenido

1. [Arquitectura Frontend](#arquitectura-frontend)
2. [Vue 3 Composition API](#vue-3-composition-api)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Servicios API](#servicios-api)
5. [Componentes y Vistas](#componentes-y-vistas)
6. [Routing](#routing)
7. [State Management](#state-management)
8. [Styling con Tailwind](#styling-con-tailwind)

---

## 🏗️ Arquitectura Frontend

### Stack Tecnológico

```
Vue 3.5 (Composition API)
    ↓
Vite 5.0 (Build Tool)
    ↓
Axios (HTTP Client)
    ↓
Vue Router (SPA Routing)
    ↓
Tailwind CSS (Styling)
```

### ¿Por Qué Esta Stack?

**Vue 3:**
- Composition API más limpia que Options API
- Better TypeScript support (aunque no lo usemos aquí)
- Performance mejorado (Virtual DOM optimizado)
- Reactivity system más robusto

**Vite:**
- **10-100x más rápido** que Webpack en dev
- Hot Module Replacement (HMR) instantáneo
- Build de producción optimizado (Rollup)
- Zero-config para Vue

**Axios:**
- Interceptors para auth tokens (futuro)
- Manejo de errores centralizado
- Transformaciones de request/response
- Cancelación de requests

**Tailwind CSS:**
- Utility-first (sin CSS custom)
- Purge automático (solo CSS usado)
- Responsive design fácil
- Dark mode ready (futuro)

---

## 🎯 Vue 3 Composition API

### Options API vs Composition API

**Options API (Vue 2 style):**

```javascript
export default {
  data() {
    return {
      students: [],
      loading: false
    }
  },
  methods: {
    async fetchStudents() {
      this.loading = true;
      const response = await fetch('/api/students');
      this.students = await response.json();
      this.loading = false;
    }
  },
  mounted() {
    this.fetchStudents();
  }
}
```

**Composition API (Vue 3 style - usado en EduRAG):**

```javascript
<script setup>
import { ref, onMounted } from 'vue';

const students = ref([]);
const loading = ref(false);

async function fetchStudents() {
  loading.value = true;
  const response = await fetch('/api/students');
  students.value = await response.json();
  loading.value = false;
}

onMounted(() => {
  fetchStudents();
});
</script>
```

### Ventajas de Composition API

1. **Organización Lógica:**
   ```javascript
   // Toda la lógica de "students" junta
   const students = ref([]);
   const loadStudents = async () => { /* ... */ };
   const deleteStudent = async (id) => { /* ... */ };
   
   // Toda la lógica de "courses" junta
   const courses = ref([]);
   const loadCourses = async () => { /* ... */ };
   ```

2. **Reutilización (Composables):**
   ```javascript
   // composables/useStudents.js
   export function useStudents() {
     const students = ref([]);
     const loading = ref(false);
     
     async function fetch() { /* ... */ }
     async function create(data) { /* ... */ }
     
     return { students, loading, fetch, create };
   }
   
   // En cualquier componente:
   const { students, loading, fetch } = useStudents();
   ```

3. **Better Tree-Shaking:**
   - Solo importas lo que usas (`ref`, `onMounted`)
   - Código más pequeño en producción

---

## 📁 Estructura del Proyecto

```
frontend/
├── src/
│   ├── main.js                 # Entry point
│   ├── App.vue                 # Root component
│   │
│   ├── views/                  # Page components (Routes)
│   │   ├── DashboardView.vue   # 🏠 Dashboard principal
│   │   ├── AdminView.vue       # 👨‍💼 Panel administración (tabs)
│   │   ├── ChatRAGView.vue     # 💬 Chat inteligente RAG
│   │   ├── CoursesView.vue     # 📚 Catálogo de cursos
│   │   ├── CourseDetailView.vue # 🔍 Detalle de curso
│   │   ├── CourseManageView.vue # ⚙️ Gestión de cursos
│   │   ├── EnrollmentsView.vue  # 📝 Gestión inscripciones
│   │   └── AnalyticsView.vue    # 📊 Dashboard analytics
│   │
│   ├── components/             # Reusable components (futuro)
│   │   ├── common/
│   │   │   ├── Button.vue
│   │   │   ├── Input.vue
│   │   │   └── Modal.vue
│   │   └── layout/
│   │       ├── Navbar.vue
│   │       └── Footer.vue
│   │
│   ├── services/               # API client
│   │   └── api.js              # Axios config + endpoints
│   │
│   ├── router/                 # Vue Router
│   │   └── index.js            # Route definitions
│   │
│   ├── composables/            # Reusable logic (futuro)
│   │   ├── useAuth.js
│   │   ├── useStudents.js
│   │   └── useCourses.js
│   │
│   ├── assets/                 # Static assets
│   │   └── main.css            # Global CSS + Tailwind imports
│   │
│   └── utils/                  # Utility functions
│       ├── formatters.js       # Date, number formatters
│       └── validators.js       # Form validation
│
├── public/                     # Static files (copied as-is)
│   └── favicon.ico
│
├── index.html                  # HTML template
├── package.json                # Dependencies
├── vite.config.js              # Vite configuration
├── tailwind.config.js          # Tailwind configuration
└── postcss.config.js           # PostCSS configuration
```

---

## 🔌 Servicios API

### api.js - Cliente HTTP Centralizado

```javascript
/**
 * API Service - Centralized HTTP client with Axios
 */

import axios from 'axios';

// ============================================================================
// AXIOS INSTANCE
// ============================================================================

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',  // Backend URL
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,  // 30 segundos (importante para RAG queries)
});


// ============================================================================
// REQUEST INTERCEPTOR
// ============================================================================

apiClient.interceptors.request.use(
  (config) => {
    // Futuro: Agregar auth token
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    
    console.log(`🚀 ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ Request error:', error);
    return Promise.reject(error);
  }
);


// ============================================================================
// RESPONSE INTERCEPTOR
// ============================================================================

apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ ${response.config.method.toUpperCase()} ${response.config.url} - ${response.status}`);
    return response;
  },
  (error) => {
    // Manejo centralizado de errores
    if (error.response) {
      // Server respondió con error
      const status = error.response.status;
      const message = error.response.data?.detail || error.response.data?.message || 'Error desconocido';
      
      console.error(`❌ ${status}: ${message}`);
      
      // Casos específicos
      if (status === 401) {
        // Unauthorized - redirigir a login
        // router.push('/login');
      } else if (status === 403) {
        // Forbidden
        alert('No tienes permisos para esta acción');
      } else if (status === 404) {
        // Not found
        console.warn('Recurso no encontrado');
      } else if (status >= 500) {
        // Server error
        alert('Error del servidor. Por favor intenta más tarde.');
      }
    } else if (error.request) {
      // Request se envió pero no hubo respuesta
      console.error('❌ No response from server');
      alert('No se pudo conectar al servidor. Verifica tu conexión.');
    } else {
      // Algo falló al configurar el request
      console.error('❌ Request setup error:', error.message);
    }
    
    return Promise.reject(error);
  }
);


// ============================================================================
// API ENDPOINTS
// ============================================================================

export const studentsAPI = {
  getAll: () => apiClient.get('/students'),
  getById: (id) => apiClient.get(`/students/${id}`),
  create: (data) => apiClient.post('/students', data),
  update: (id, data) => apiClient.put(`/students/${id}`, data),
  delete: (id) => apiClient.delete(`/students/${id}`),
};

export const coursesAPI = {
  getAll: () => apiClient.get('/courses'),
  getById: (id) => apiClient.get(`/courses/${id}`),
  create: (data) => apiClient.post('/courses', data),
  update: (id, data) => apiClient.put(`/courses/${id}`, data),
  delete: (id) => apiClient.delete(`/courses/${id}`),
};

export const materialsAPI = {
  getAll: () => apiClient.get('/materials'),
  getById: (id) => apiClient.get(`/materials/${id}`),
  uploadPDF: (formData) => apiClient.post('/materials/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    timeout: 60000,  // 60s para uploads grandes
  }),
  delete: (id) => apiClient.delete(`/materials/${id}`),
};

export const enrollmentsAPI = {
  getAll: () => apiClient.get('/enrollments'),
  create: (data) => apiClient.post('/enrollments', data),
  delete: (id) => apiClient.delete(`/enrollments/${id}`),
};

export const ragAPI = {
  chat: (query, courseId, materialId = null) => apiClient.post('/rag/chat', {
    query,
    course_id: courseId,
    material_id: materialId,
  }),
  health: () => apiClient.get('/rag/health'),
};

export const analyticsAPI = {
  getStats: () => apiClient.get('/analytics/stats'),
  getDetailed: () => apiClient.get('/analytics/detailed'),
};

export const authAPI = {
  login: (email, password) => apiClient.post('/auth/login', { email, password }),
  logout: () => apiClient.post('/auth/logout'),
};


// ============================================================================
// EXPORT DEFAULT
// ============================================================================

export default apiClient;
```

### Uso en Componentes

```javascript
<script setup>
import { ref } from 'vue';
import { studentsAPI } from '@/services/api';

const students = ref([]);
const loading = ref(false);
const error = ref(null);

async function loadStudents() {
  try {
    loading.value = true;
    error.value = null;
    
    const response = await studentsAPI.getAll();
    students.value = response.data;
    
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar estudiantes';
    console.error(err);
  } finally {
    loading.value = false;
  }
}
</script>
```

---

## 🎨 Componentes y Vistas

### Anatomía de un Componente Vue 3

**Estructura de AdminView.vue (simplificada):**

```vue
<template>
  <!-- ========== NAVIGATION ========== -->
  <nav class="bg-white shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <h1 class="text-2xl font-bold text-blue-600">EduRAG - Admin</h1>
      </div>
    </div>
  </nav>

  <!-- ========== TABS ========== -->
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="flex space-x-4 border-b mb-6">
      <button 
        @click="activeTab = 'students'"
        :class="tabClass('students')"
      >
        👥 Estudiantes
      </button>
      <button 
        @click="activeTab = 'courses'"
        :class="tabClass('courses')"
      >
        📚 Cursos
      </button>
      <!-- Más tabs... -->
    </div>

    <!-- ========== TAB CONTENT ========== -->
    
    <!-- Estudiantes Tab -->
    <div v-if="activeTab === 'students'" class="space-y-6">
      <!-- Formulario de Creación -->
      <div class="bg-white shadow rounded-lg p-6">
        <h3 class="text-lg font-semibold mb-4">Crear Nuevo Estudiante</h3>
        <form @submit.prevent="createStudent" class="grid grid-cols-3 gap-4">
          <input 
            v-model="studentForm.name" 
            placeholder="Nombre completo"
            required
            class="border rounded px-3 py-2"
          />
          <input 
            v-model="studentForm.email"
            type="email"
            placeholder="Email"
            required
            class="border rounded px-3 py-2"
          />
          <input 
            v-model="studentForm.cohort"
            placeholder="Cohorte (ej: 2024-A)"
            required
            class="border rounded px-3 py-2"
          />
          <button 
            type="submit"
            :disabled="creating"
            class="col-span-3 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {{ creating ? 'Creando...' : 'Crear Estudiante' }}
          </button>
        </form>
      </div>

      <!-- Tabla de Estudiantes -->
      <div class="bg-white shadow rounded-lg overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cohorte</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="student in students" :key="student.id">
              <td class="px-6 py-4">{{ student.name }}</td>
              <td class="px-6 py-4">{{ student.email }}</td>
              <td class="px-6 py-4">
                <span class="px-2 py-1 text-xs rounded bg-blue-100 text-blue-800">
                  {{ student.cohort }}
                </span>
              </td>
              <td class="px-6 py-4 space-x-2">
                <button 
                  @click="editStudent(student)"
                  class="text-blue-600 hover:text-blue-800"
                >
                  ✏️ Editar
                </button>
                <button 
                  @click="deleteStudent(student.id)"
                  class="text-red-600 hover:text-red-800"
                >
                  🗑️ Eliminar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Otros tabs... -->
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { studentsAPI, coursesAPI } from '@/services/api';

// ============================================================================
// REACTIVE STATE
// ============================================================================

const activeTab = ref('students');

// Students
const students = ref([]);
const studentForm = ref({
  name: '',
  email: '',
  cohort: ''
});
const creating = ref(false);

// ============================================================================
// COMPUTED PROPERTIES
// ============================================================================

function tabClass(tab) {
  return activeTab.value === tab
    ? 'px-4 py-2 border-b-2 border-blue-600 text-blue-600 font-medium'
    : 'px-4 py-2 text-gray-600 hover:text-blue-600';
}

// ============================================================================
// METHODS
// ============================================================================

async function loadStudents() {
  try {
    const response = await studentsAPI.getAll();
    students.value = response.data;
  } catch (error) {
    alert('Error al cargar estudiantes');
    console.error(error);
  }
}

async function createStudent() {
  if (!studentForm.value.name || !studentForm.value.email || !studentForm.value.cohort) {
    alert('Todos los campos son requeridos');
    return;
  }
  
  try {
    creating.value = true;
    
    await studentsAPI.create(studentForm.value);
    
    // Reset form
    studentForm.value = { name: '', email: '', cohort: '' };
    
    // Reload list
    await loadStudents();
    
    alert('Estudiante creado exitosamente');
    
  } catch (error) {
    alert(error.response?.data?.detail || 'Error al crear estudiante');
  } finally {
    creating.value = false;
  }
}

async function deleteStudent(id) {
  if (!confirm('¿Estás seguro de eliminar este estudiante?')) {
    return;
  }
  
  try {
    await studentsAPI.delete(id);
    await loadStudents();
    alert('Estudiante eliminado');
  } catch (error) {
    alert(error.response?.data?.detail || 'Error al eliminar');
  }
}

// ============================================================================
// LIFECYCLE
// ============================================================================

onMounted(() => {
  loadStudents();
});
</script>

<style scoped>
/* Estilos específicos del componente (si es necesario) */
</style>
```

### Patrones de Vue 3

#### 1. Reactive State con `ref`

```javascript
// Para primitivos y objetos
const count = ref(0);
const user = ref({ name: 'Juan' });

// Acceso al valor con .value
count.value++;
user.value.name = 'Pedro';

// En template, no necesitas .value
<template>
  <p>{{ count }}</p>  <!-- No {{ count.value }} -->
</template>
```

#### 2. Reactive Objects con `reactive`

```javascript
import { reactive } from 'vue';

const state = reactive({
  students: [],
  loading: false,
  error: null
});

// Sin .value
state.loading = true;
state.students.push(newStudent);
```

**¿Cuándo usar `ref` vs `reactive`?**

- `ref`: Valores primitivos (string, number, boolean)
- `reactive`: Objetos complejos que no cambiarán de referencia
- **Preferencia:** `ref` para todo (más consistente)

#### 3. Computed Properties

```javascript
import { ref, computed } from 'vue';

const students = ref([
  { name: 'Juan', cohort: '2024-A' },
  { name: 'María', cohort: '2024-B' },
  { name: 'Pedro', cohort: '2024-A' }
]);

// Computed - se recalcula automáticamente cuando students cambia
const students2024A = computed(() => {
  return students.value.filter(s => s.cohort === '2024-A');
});

// En template
<template>
  <p>Estudiantes 2024-A: {{ students2024A.length }}</p>
</template>
```

#### 4. Watchers

```javascript
import { ref, watch } from 'vue';

const searchQuery = ref('');
const students = ref([]);

// Watch - ejecuta cuando searchQuery cambia
watch(searchQuery, async (newQuery) => {
  if (newQuery.length >= 3) {
    const response = await studentsAPI.search(newQuery);
    students.value = response.data;
  }
});
```

---

## 🧭 Routing con Vue Router

### router/index.js

```javascript
import { createRouter, createWebHistory } from 'vue-router';

// Lazy loading de componentes
const DashboardView = () => import('@/views/DashboardView.vue');
const AdminView = () => import('@/views/AdminView.vue');
const ChatRAGView = () => import('@/views/ChatRAGView.vue');
const CoursesView = () => import('@/views/CoursesView.vue');
const CourseDetailView = () => import('@/views/CourseDetailView.vue');
const EnrollmentsView = () => import('@/views/EnrollmentsView.vue');
const AnalyticsView = () => import('@/views/AnalyticsView.vue');

const routes = [
  {
    path: '/',
    redirect: '/dashboard'  // Redirigir / a /dashboard
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: {
      title: 'Dashboard - EduRAG'
    }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminView,
    meta: {
      title: 'Administración - EduRAG',
      requiresAuth: true  // Futuro: guard de autenticación
    }
  },
  {
    path: '/chat',
    name: 'ChatRAG',
    component: ChatRAGView,
    meta: {
      title: 'Chat RAG - EduRAG'
    }
  },
  {
    path: '/courses',
    name: 'Courses',
    component: CoursesView,
    meta: {
      title: 'Cursos - EduRAG'
    }
  },
  {
    path: '/courses/:id',
    name: 'CourseDetail',
    component: CourseDetailView,
    meta: {
      title: 'Detalle de Curso - EduRAG'
    }
  },
  {
    path: '/enrollments',
    name: 'Enrollments',
    component: EnrollmentsView,
    meta: {
      title: 'Inscripciones - EduRAG'
    }
  },
  {
    path: '/analytics',
    name: 'Analytics',
    component: AnalyticsView,
    meta: {
      title: 'Analíticas - EduRAG'
    }
  },
  {
    path: '/:pathMatch(.*)*',  // 404 catch-all
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Navigation guard para títulos de página
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'EduRAG';
  next();
});

// Futuro: Navigation guard para autenticación
// router.beforeEach((to, from, next) => {
//   if (to.meta.requiresAuth && !isAuthenticated()) {
//     next('/login');
//   } else {
//     next();
//   }
// });

export default router;
```

### Uso en Componentes

**Navegación programática:**

```javascript
import { useRouter } from 'vue-router';

const router = useRouter();

// Navegar a otra ruta
router.push('/courses');
router.push({ name: 'Courses' });
router.push({ name: 'CourseDetail', params: { id: '123' } });

// Navegar y reemplazar historial
router.replace('/dashboard');

// Volver atrás
router.back();
router.go(-1);
```

**Acceder a parámetros:**

```javascript
import { useRoute } from 'vue-router';

const route = useRoute();

// /courses/123
const courseId = route.params.id;

// /courses?search=redes
const searchQuery = route.query.search;
```

---

## 🎨 Styling con Tailwind CSS

### Configuración

**tailwind.config.js:**

```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          // ...
          600: '#2563eb',  // Azul principal
          // ...
        }
      }
    },
  },
  plugins: [],
}
```

**src/assets/main.css:**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom styles */
@layer components {
  .btn-primary {
    @apply bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50;
  }
  
  .input-field {
    @apply border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500;
  }
  
  .card {
    @apply bg-white shadow rounded-lg p-6;
  }
}
```

### Clases Utility Más Usadas

**Layout:**
```html
<!-- Flexbox -->
<div class="flex items-center justify-between">
<div class="flex flex-col space-y-4">

<!-- Grid -->
<div class="grid grid-cols-3 gap-4">
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4">

<!-- Spacing -->
<div class="p-6 m-4">  <!-- padding 1.5rem, margin 1rem -->
<div class="px-4 py-2">  <!-- padding horizontal/vertical -->
<div class="space-x-2">  <!-- gap horizontal entre children -->
```

**Typography:**
```html
<h1 class="text-3xl font-bold text-gray-900">
<p class="text-sm text-gray-600">
<span class="text-xs font-medium uppercase tracking-wide">
```

**Colors:**
```html
<div class="bg-blue-600 text-white">
<div class="bg-gray-50 text-gray-900">
<button class="bg-red-600 hover:bg-red-700">
```

**Borders & Shadows:**
```html
<div class="border border-gray-300 rounded-lg shadow-sm">
<div class="rounded-full shadow-lg">
```

**Responsive:**
```html
<div class="hidden md:block">  <!-- Oculto en móvil, visible en tablet+ -->
<div class="w-full md:w-1/2 lg:w-1/3">  <!-- Ancho responsive -->
<div class="text-sm md:text-base lg:text-lg">  <!-- Tamaño responsive -->
```

---

## 🔗 Continuación

Ver documentos:
- [DATABASE_ARCHITECTURE.md](DATABASE_ARCHITECTURE.md) - Arquitectura de base de datos
- [RAG_IMPLEMENTATION.md](RAG_IMPLEMENTATION.md) - Implementación del sistema RAG
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Guía de despliegue

---

*Última actualización: Octubre 23, 2025*
*Versión: 1.0.0*
