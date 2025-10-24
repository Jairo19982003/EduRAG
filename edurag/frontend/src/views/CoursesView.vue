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
              <router-link to="/chat" class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600">Chat RAG</router-link>
              <router-link to="/analytics" class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600">Analíticas</router-link>
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
        <h2 class="text-3xl font-bold text-gray-900 mb-6">Cursos Disponibles</h2>
        
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p class="mt-4 text-gray-600">Cargando cursos...</p>
        </div>

        <div v-else-if="courses.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No hay cursos disponibles</h3>
          <p class="mt-1 text-sm text-gray-500">Comienza agregando cursos desde el panel de administración.</p>
        </div>

        <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <div v-for="course in courses" :key="course.id" class="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition">
            <div class="p-6">
              <div class="flex items-center justify-between mb-4">
                <span class="inline-flex items-center px-3 py-0.5 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                  {{ course.code }}
                </span>
                <span class="text-sm text-gray-500">{{ course.credits }} créditos</span>
              </div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">{{ course.name }}</h3>
              <p class="text-sm text-gray-600 line-clamp-3 mb-4">{{ course.syllabus || 'Sin descripción' }}</p>
              <div class="flex space-x-2">
                <button @click="goToCourse(course.id)" class="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition">
                  Ver Detalles
                </button>
                <button @click="goToManage(course.id)" class="flex-1 bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700 transition">
                  Gestionar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { coursesAPI } from '@/services/api'

const router = useRouter()
const courses = ref([])
const loading = ref(true)

const loadCourses = async () => {
  try {
    const response = await coursesAPI.getAll()
    courses.value = response.data.data || response.data
  } catch (error) {
    console.error('Error loading courses:', error)
  } finally {
    loading.value = false
  }
}

const goToCourse = (courseId) => {
  router.push(`/courses/${courseId}`)
}

const goToManage = (courseId) => {
  router.push(`/courses/${courseId}/manage`)
}

onMounted(() => {
  loadCourses()
})
</script>
