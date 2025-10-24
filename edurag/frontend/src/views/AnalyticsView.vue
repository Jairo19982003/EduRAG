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
              <router-link to="/enrollments" class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600">Inscripciones</router-link>
              <router-link to="/chat" class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600">Chat RAG</router-link>
              <router-link to="/analytics" class="px-3 py-2 text-sm font-medium text-gray-900 hover:text-blue-600">Analíticas</router-link>
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
        <!-- Header -->
        <div class="flex items-center justify-between mb-6">
          <div>
            <h2 class="text-3xl font-bold text-gray-900">Analíticas del Sistema</h2>
            <p class="text-gray-600 mt-1">Estadísticas detalladas y métricas de rendimiento</p>
          </div>
          <button @click="loadAnalytics" :disabled="loading" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">
            <span v-if="loading">Actualizando...</span>
            <span v-else>🔄 Actualizar</span>
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="loading && !analytics" class="bg-white shadow rounded-lg p-12 text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p class="text-gray-600 mt-4">Cargando analíticas...</p>
        </div>

        <!-- Content -->
        <div v-else-if="analytics">
          <!-- Overview Cards -->
          <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
            <div class="bg-gradient-to-br from-blue-500 to-blue-600 overflow-hidden shadow rounded-lg">
              <div class="p-5 text-white">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                  </div>
                  <div class="ml-5 w-0 flex-1">
                    <dl>
                      <dt class="text-sm font-medium truncate opacity-90">Total Cursos</dt>
                      <dd class="text-3xl font-semibold">{{ analytics.overview.total_courses }}</dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div class="bg-gradient-to-br from-green-500 to-green-600 overflow-hidden shadow rounded-lg">
              <div class="p-5 text-white">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                  </div>
                  <div class="ml-5 w-0 flex-1">
                    <dl>
                      <dt class="text-sm font-medium truncate opacity-90">Total Estudiantes</dt>
                      <dd class="text-3xl font-semibold">{{ analytics.overview.total_students }}</dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div class="bg-gradient-to-br from-purple-500 to-purple-600 overflow-hidden shadow rounded-lg">
              <div class="p-5 text-white">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <div class="ml-5 w-0 flex-1">
                    <dl>
                      <dt class="text-sm font-medium truncate opacity-90">Total Materiales</dt>
                      <dd class="text-3xl font-semibold">{{ analytics.overview.total_materials }}</dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div class="bg-gradient-to-br from-orange-500 to-orange-600 overflow-hidden shadow rounded-lg">
              <div class="p-5 text-white">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                  </div>
                  <div class="ml-5 w-0 flex-1">
                    <dl>
                      <dt class="text-sm font-medium truncate opacity-90">Inscripciones Activas</dt>
                      <dd class="text-3xl font-semibold">{{ analytics.overview.active_enrollments }}</dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Charts Row -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <!-- Top Courses Chart -->
            <div class="bg-white shadow rounded-lg p-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">📊 Cursos Más Populares</h3>
              <div v-if="analytics.course_stats.length > 0" class="space-y-4">
                <div v-for="course in analytics.course_stats.slice(0, 5)" :key="course.id" class="relative">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-sm font-medium text-gray-700">{{ course.code }} - {{ course.name }}</span>
                    <span class="text-sm text-gray-500">{{ course.enrollments_count }} estudiantes</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2.5">
                    <div class="bg-blue-600 h-2.5 rounded-full" :style="{ width: `${getPercentage(course.enrollments_count, analytics.overview.total_enrollments)}%` }"></div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-8 text-gray-500">
                No hay datos de cursos disponibles
              </div>
            </div>

            <!-- Enrollments by Status -->
            <div class="bg-white shadow rounded-lg p-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">📈 Estado de Inscripciones</h3>
              <div class="space-y-4">
                <div class="flex items-center justify-between p-4 bg-green-50 rounded-lg">
                  <div class="flex items-center">
                    <div class="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                    <span class="font-medium text-gray-700">Activas</span>
                  </div>
                  <span class="text-2xl font-bold text-green-600">{{ analytics.enrollments_by_status.activo || 0 }}</span>
                </div>
                <div class="flex items-center justify-between p-4 bg-yellow-50 rounded-lg">
                  <div class="flex items-center">
                    <div class="w-3 h-3 bg-yellow-500 rounded-full mr-3"></div>
                    <span class="font-medium text-gray-700">Completadas</span>
                  </div>
                  <span class="text-2xl font-bold text-yellow-600">{{ analytics.enrollments_by_status.completado || 0 }}</span>
                </div>
                <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div class="flex items-center">
                    <div class="w-3 h-3 bg-gray-500 rounded-full mr-3"></div>
                    <span class="font-medium text-gray-700">Inactivas</span>
                  </div>
                  <span class="text-2xl font-bold text-gray-600">{{ analytics.enrollments_by_status.inactivo || 0 }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Secondary Metrics -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            <div class="bg-white shadow rounded-lg p-6">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-500">Promedio Materiales/Curso</p>
                  <p class="text-3xl font-bold text-blue-600">{{ analytics.overview.avg_materials_per_course }}</p>
                </div>
                <div class="p-3 bg-blue-100 rounded-full">
                  <svg class="h-8 w-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
              </div>
            </div>

            <div class="bg-white shadow rounded-lg p-6">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-500">Promedio Estudiantes/Curso</p>
                  <p class="text-3xl font-bold text-green-600">{{ analytics.overview.avg_enrollments_per_course }}</p>
                </div>
                <div class="p-3 bg-green-100 rounded-full">
                  <svg class="h-8 w-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
              </div>
            </div>

            <div class="bg-white shadow rounded-lg p-6">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-500">Total Inscripciones</p>
                  <p class="text-3xl font-bold text-purple-600">{{ analytics.overview.total_enrollments }}</p>
                </div>
                <div class="p-3 bg-purple-100 rounded-full">
                  <svg class="h-8 w-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                  </svg>
                </div>
              </div>
            </div>
          </div>

          <!-- Enrollments by Cohort -->
          <div class="bg-white shadow rounded-lg p-6 mb-8" v-if="Object.keys(analytics.enrollments_by_cohort).length > 0">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">👥 Inscripciones por Cohorte</h3>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              <div v-for="(count, cohort) in analytics.enrollments_by_cohort" :key="cohort" class="p-4 bg-gradient-to-br from-indigo-50 to-indigo-100 rounded-lg">
                <p class="text-sm font-medium text-gray-600">{{ cohort }}</p>
                <p class="text-2xl font-bold text-indigo-600">{{ count }}</p>
                <p class="text-xs text-gray-500">inscripciones</p>
              </div>
            </div>
          </div>

          <!-- Recent Activity -->
          <div class="bg-white shadow rounded-lg p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">🕒 Actividad Reciente</h3>
            <div v-if="analytics.recent_activity.length > 0" class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estudiante</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Curso</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="(activity, index) in analytics.recent_activity" :key="index" class="hover:bg-gray-50">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ activity.student_name }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ activity.course_name }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="['px-2 inline-flex text-xs leading-5 font-semibold rounded-full', getStatusClass(activity.status)]">
                        {{ activity.status }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(activity.date) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              No hay actividad reciente
            </div>
          </div>

          <!-- Course Statistics Table -->
          <div class="bg-white shadow rounded-lg p-6 mt-8">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">📚 Estadísticas Detalladas por Curso</h3>
            <div v-if="analytics.course_stats.length > 0" class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Código</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
                    <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Materiales</th>
                    <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Estudiantes</th>
                    <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Popularidad</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="course in analytics.course_stats" :key="course.id" class="hover:bg-gray-50">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">{{ course.code }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ course.name }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 text-center">
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                        {{ course.materials_count }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 text-center">
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        {{ course.enrollments_count }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-center">
                      <div class="flex items-center justify-center">
                        <span v-for="n in getStars(course.enrollments_count)" :key="n" class="text-yellow-400">★</span>
                        <span v-for="n in (5 - getStars(course.enrollments_count))" :key="'empty-' + n" class="text-gray-300">★</span>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              No hay cursos disponibles
            </div>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
          <p class="text-red-600">{{ error }}</p>
          <button @click="loadAnalytics" class="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">
            Reintentar
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const analytics = ref(null)
const loading = ref(false)
const error = ref(null)

const loadAnalytics = async () => {
  loading.value = true
  error.value = null
  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const response = await axios.get(`${apiUrl}/api/analytics/detailed`)
    analytics.value = response.data
  } catch (err) {
    console.error('Error loading analytics:', err)
    error.value = 'Error al cargar las analíticas. Por favor, intenta nuevamente.'
  } finally {
    loading.value = false
  }
}

const getPercentage = (value, total) => {
  if (total === 0) return 0
  return Math.round((value / total) * 100)
}

const getStars = (enrollments) => {
  if (enrollments >= 20) return 5
  if (enrollments >= 15) return 4
  if (enrollments >= 10) return 3
  if (enrollments >= 5) return 2
  if (enrollments >= 1) return 1
  return 0
}

const getStatusClass = (status) => {
  const classes = {
    'activo': 'bg-green-100 text-green-800',
    'inactivo': 'bg-gray-100 text-gray-800',
    'completado': 'bg-blue-100 text-blue-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', { year: 'numeric', month: 'short', day: 'numeric' })
}

onMounted(() => {
  loadAnalytics()
})
</script>
