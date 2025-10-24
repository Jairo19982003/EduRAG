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
              <router-link to="/courses" class="px-3 py-2 text-sm font-medium text-gray-900 hover:text-blue-600">Cursos</router-link>
              <router-link to="/enrollments" class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600">Inscripciones</router-link>
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
        <!-- Back Button -->
        <button @click="goBack" class="mb-6 flex items-center text-blue-600 hover:text-blue-800">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
          Volver a Cursos
        </button>

        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p class="mt-4 text-gray-600">Cargando información del curso...</p>
        </div>

        <div v-else-if="course">
          <!-- Course Header -->
          <div class="bg-white shadow rounded-lg p-6 mb-6">
            <div class="flex items-start justify-between">
              <div>
                <div class="flex items-center space-x-4 mb-2">
                  <span class="inline-flex items-center px-4 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                    {{ course.code }}
                  </span>
                  <span class="text-sm text-gray-500">{{ course.credits }} créditos</span>
                </div>
                <h2 class="text-3xl font-bold text-gray-900 mb-2">{{ course.name }}</h2>
                <p class="text-gray-600">{{ course.syllabus || 'Sin descripción' }}</p>
              </div>
            </div>
          </div>

          <!-- Statistics Cards -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div class="bg-white shadow rounded-lg p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-blue-100 rounded-md p-3">
                  <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
                  </svg>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-500">Estudiantes Inscritos</p>
                  <p class="text-2xl font-semibold text-gray-900">{{ enrolledStudents.length }}</p>
                </div>
              </div>
            </div>

            <div class="bg-white shadow rounded-lg p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-green-100 rounded-md p-3">
                  <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-500">Materiales</p>
                  <p class="text-2xl font-semibold text-gray-900">{{ materials.length }}</p>
                </div>
              </div>
            </div>

            <div class="bg-white shadow rounded-lg p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-purple-100 rounded-md p-3">
                  <svg class="h-6 w-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-500">Inscritos Activos</p>
                  <p class="text-2xl font-semibold text-gray-900">{{ activeEnrollments }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Enrolled Students Table -->
          <div class="bg-white shadow rounded-lg mb-6">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Estudiantes Inscritos</h3>
            </div>
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estudiante</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cohorte</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha Inscripción</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="enrolledStudents.length === 0">
                    <td colspan="5" class="px-6 py-4 text-center text-sm text-gray-500">
                      No hay estudiantes inscritos en este curso
                    </td>
                  </tr>
                  <tr v-for="enrollment in enrolledStudents" :key="enrollment.id" class="hover:bg-gray-50">
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
                      <span :class="getStatusClass(enrollment.status)">
                        {{ enrollment.status }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ formatDate(enrollment.created_at) }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Materials List -->
          <div class="bg-white shadow rounded-lg">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Materiales del Curso</h3>
            </div>
            <div class="p-6">
              <div v-if="materials.length === 0" class="text-center py-8 text-gray-500">
                No hay materiales disponibles para este curso
              </div>
              <div v-else class="space-y-4">
                <div v-for="material in materials" :key="material.id" class="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition">
                  <div class="flex items-start justify-between">
                    <div class="flex-1">
                      <h4 class="text-lg font-medium text-gray-900 mb-1">{{ material.title }}</h4>
                      <div class="flex items-center space-x-4 text-sm text-gray-500">
                        <span class="flex items-center">
                          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                          </svg>
                          {{ material.mime_type || 'application/pdf' }}
                        </span>
                        <span v-if="material.author">Por: {{ material.author }}</span>
                        <span>{{ formatDate(material.created_at) }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { coursesAPI } from '@/services/api'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const course = ref(null)
const materials = ref([])
const enrolledStudents = ref([])
const loading = ref(true)

const activeEnrollments = computed(() => {
  return enrolledStudents.value.filter(e => e.status === 'active').length
})

const loadCourseData = async () => {
  try {
    const courseId = route.params.id
    
    // Load course details
    const courseResponse = await coursesAPI.getById(courseId)
    course.value = courseResponse.data.data || courseResponse.data
    
    // Load materials
    const materialsResponse = await coursesAPI.getMaterials(courseId)
    materials.value = materialsResponse.data.data || materialsResponse.data
    
    // Load enrollments with student details
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const enrollmentsResponse = await axios.get(`${apiUrl}/api/enrollments`)
    const allEnrollments = enrollmentsResponse.data.data || enrollmentsResponse.data
    enrolledStudents.value = allEnrollments.filter(e => e.course_id === courseId)
    
  } catch (error) {
    console.error('Error loading course data:', error)
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

const goBack = () => {
  router.push('/courses')
}

onMounted(() => {
  loadCourseData()
})
</script>
