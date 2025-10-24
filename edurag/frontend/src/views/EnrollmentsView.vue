<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center space-x-8">
            <h1 class="text-2xl font-bold text-blue-600">EduRAG</h1>
            <div class="hidden md:flex space-x-4">
              <router-link to="/dashboard" class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600">Dashboard</router-link>
              <router-link to="/courses" class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600">Cursos</router-link>
              <router-link to="/enrollments" class="px-3 py-2 text-sm font-medium text-gray-900 hover:text-blue-600">Inscripciones</router-link>
              <router-link to="/chat" class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600">Chat RAG</router-link>
              <router-link to="/admin" class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600">Administración</router-link>
            </div>
          </div>
          <div class="flex items-center">
            <span class="text-sm text-gray-700">Bienvenido, Usuario Demo</span>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="mb-6">
          <h2 class="text-3xl font-bold text-gray-900">Gestión de Inscripciones</h2>
          <p class="mt-2 text-sm text-gray-600">Vista completa de estudiantes y sus cursos inscritos</p>
        </div>

        <!-- Statistics Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
          <div class="bg-white shadow rounded-lg p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-blue-100 rounded-md p-3">
                <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-500">Total Inscripciones</p>
                <p class="text-2xl font-semibold text-gray-900">{{ totalEnrollments }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white shadow rounded-lg p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-green-100 rounded-md p-3">
                <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-500">Activas</p>
                <p class="text-2xl font-semibold text-gray-900">{{ activeEnrollments }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white shadow rounded-lg p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-purple-100 rounded-md p-3">
                <svg class="h-6 w-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-500">Estudiantes</p>
                <p class="text-2xl font-semibold text-gray-900">{{ uniqueStudents }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white shadow rounded-lg p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-yellow-100 rounded-md p-3">
                <svg class="h-6 w-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-500">Cursos</p>
                <p class="text-2xl font-semibold text-gray-900">{{ uniqueCourses }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Filters -->
        <div class="bg-white shadow rounded-lg p-6 mb-6">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Buscar Estudiante</label>
              <input 
                v-model="searchStudent" 
                type="text" 
                placeholder="Nombre o email..."
                class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Filtrar por Curso</label>
              <select v-model="filterCourse" class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
                <option value="">Todos los cursos</option>
                <option v-for="course in courses" :key="course.id" :value="course.id">
                  {{ course.code }} - {{ course.name }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Filtrar por Estado</label>
              <select v-model="filterStatus" class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
                <option value="">Todos los estados</option>
                <option value="active">Activo</option>
                <option value="inactive">Inactivo</option>
                <option value="completed">Completado</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Enrollments Table -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
            <h3 class="text-lg font-medium text-gray-900">Lista de Inscripciones</h3>
            <span class="text-sm text-gray-500">{{ filteredEnrollments.length }} resultados</span>
          </div>

          <div v-if="loading" class="text-center py-12">
            <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p class="mt-4 text-gray-600">Cargando inscripciones...</p>
          </div>

          <div v-else class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estudiante</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cohorte</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Curso</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-if="filteredEnrollments.length === 0">
                  <td colspan="7" class="px-6 py-8 text-center text-sm text-gray-500">
                    <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
                    </svg>
                    No se encontraron inscripciones con los filtros aplicados
                  </td>
                </tr>
                <tr v-for="enrollment in filteredEnrollments" :key="enrollment.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900">{{ enrollment.students?.name || 'N/A' }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-500">{{ enrollment.students?.email || 'N/A' }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-500">{{ enrollment.students?.cohort || 'N/A' }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">
                      <div class="font-medium">{{ enrollment.courses?.code || 'N/A' }}</div>
                      <div class="text-gray-500">{{ enrollment.courses?.name || 'N/A' }}</div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getStatusClass(enrollment.status)">
                      {{ enrollment.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatDate(enrollment.created_at) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button 
                      @click="viewCourse(enrollment.course_id)" 
                      class="text-blue-600 hover:text-blue-900 mr-3"
                      title="Ver curso"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                      </svg>
                    </button>
                    <button 
                      @click="deleteEnrollment(enrollment.id)" 
                      class="text-red-600 hover:text-red-900"
                      title="Eliminar inscripción"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                      </svg>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { coursesAPI } from '@/services/api'

const router = useRouter()
const enrollments = ref([])
const courses = ref([])
const loading = ref(true)
const searchStudent = ref('')
const filterCourse = ref('')
const filterStatus = ref('')

const api = axios.create({
  baseURL: 'http://localhost:8000'
})

const totalEnrollments = computed(() => enrollments.value.length)
const activeEnrollments = computed(() => enrollments.value.filter(e => e.status === 'active').length)
const uniqueStudents = computed(() => {
  const studentIds = new Set(enrollments.value.map(e => e.student_id))
  return studentIds.size
})
const uniqueCourses = computed(() => {
  const courseIds = new Set(enrollments.value.map(e => e.course_id))
  return courseIds.size
})

const filteredEnrollments = computed(() => {
  let result = enrollments.value

  // Filter by student search
  if (searchStudent.value) {
    const search = searchStudent.value.toLowerCase()
    result = result.filter(e => 
      e.students?.name?.toLowerCase().includes(search) ||
      e.students?.email?.toLowerCase().includes(search)
    )
  }

  // Filter by course
  if (filterCourse.value) {
    result = result.filter(e => e.course_id === filterCourse.value)
  }

  // Filter by status
  if (filterStatus.value) {
    result = result.filter(e => e.status === filterStatus.value)
  }

  return result
})

const loadData = async () => {
  try {
    // Load enrollments
    const enrollmentsResponse = await api.get('/api/enrollments')
    enrollments.value = enrollmentsResponse.data.data || enrollmentsResponse.data
    
    // Load courses for filter
    const coursesResponse = await coursesAPI.getAll()
    courses.value = coursesResponse.data.data || coursesResponse.data
  } catch (error) {
    console.error('Error loading data:', error)
  } finally {
    loading.value = false
  }
}

const getStatusClass = (status) => {
  const classes = {
    'active': 'inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800',
    'inactive': 'inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800',
    'completed': 'inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800',
  }
  return classes[status] || classes.active
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', { year: 'numeric', month: 'short', day: 'numeric' })
}

const viewCourse = (courseId) => {
  router.push(`/courses/${courseId}/manage`)
}

const deleteEnrollment = async (enrollmentId) => {
  if (!confirm('¿Estás seguro de eliminar esta inscripción?')) return
  
  try {
    await api.delete(`/api/enrollments/${enrollmentId}`)
    alert('Inscripción eliminada exitosamente')
    loadData()
  } catch (error) {
    console.error('Error deleting enrollment:', error)
    alert('Error al eliminar la inscripción')
  }
}

onMounted(() => {
  loadData()
})
</script>
