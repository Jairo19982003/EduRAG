<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center space-x-8">
            <h1 class="text-2xl font-bold text-blue-600">EduRAG</h1>
            <div class="hidden md:flex space-x-4">
              <router-link to="/dashboard" class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600">Dashboard</router-link>
              <router-link to="/courses" class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600">Cursos</router-link>
              <router-link to="/chat" class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600">Chat RAG</router-link>
              <router-link to="/analytics" class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600">Analíticas</router-link>
              <router-link to="/admin" class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600">Administración</router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="mb-6">
          <router-link to="/courses" class="text-blue-600 hover:text-blue-800 flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Volver a Cursos
          </router-link>
        </div>

        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>

        <div v-else-if="course">
          <h2 class="text-3xl font-bold text-gray-900 mb-2">{{ course.name }}</h2>
          <p class="text-gray-600 mb-6">{{ course.syllabus }}</p>
          
          <div class="bg-white shadow rounded-lg p-6">
            <h3 class="text-xl font-semibold mb-4">Materiales del Curso</h3>
            <div v-if="materials.length === 0" class="text-center py-8 text-gray-500">
              No hay materiales disponibles
            </div>
            <div v-else class="space-y-4">
              <div v-for="material in materials" :key="material.id" class="border-l-4 border-blue-500 pl-4 py-2">
                <h4 class="font-medium text-gray-900">{{ material.title }}</h4>
                <p class="text-sm text-gray-600">{{ material.author || 'Sin autor' }}</p>
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
import { useRoute } from 'vue-router'
import { coursesAPI } from '@/services/api'

const route = useRoute()
const course = ref(null)
const materials = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const [courseRes, materialsRes] = await Promise.all([
      coursesAPI.getById(route.params.id),
      coursesAPI.getMaterials(route.params.id)
    ])
    course.value = courseRes.data.data || courseRes.data
    materials.value = materialsRes.data.data || materialsRes.data
  } catch (error) {
    console.error('Error loading course:', error)
  } finally {
    loading.value = false
  }
})
</script>
