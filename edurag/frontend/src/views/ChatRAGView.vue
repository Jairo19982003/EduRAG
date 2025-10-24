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
              <router-link to="/chat" class="px-3 py-2 text-sm font-medium text-gray-900 hover:text-blue-600">Chat RAG</router-link>
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
    <main class="max-w-5xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h2 class="text-3xl font-bold text-gray-900">Chat RAG</h2>
            <p class="text-gray-600 mt-1">Consulta los materiales del curso usando IA</p>
          </div>
          <button @click="clearChat" class="px-4 py-2 text-sm bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">
            🗑️ Limpiar Chat
          </button>
        </div>

        <!-- Context Filters -->
        <div class="bg-white shadow rounded-lg p-4 mb-4">
          <h3 class="text-sm font-semibold text-gray-700 mb-3">🎯 Contexto de Búsqueda</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Filtrar por Curso (Opcional)</label>
              <select v-model="selectedCourse" @change="onCourseChange" class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
                <option value="">Todos los cursos</option>
                <option v-for="course in courses" :key="course.id" :value="course.id">
                  {{ course.code }} - {{ course.name }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Filtrar por Material (Opcional)</label>
              <select v-model="selectedMaterial" :disabled="!availableMaterials.length" class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50">
                <option value="">Todos los materiales</option>
                <option v-for="material in availableMaterials" :key="material.id" :value="material.id">
                  {{ material.title }}
                </option>
              </select>
            </div>
          </div>
          <p class="text-xs text-gray-500 mt-2">
            💡 <strong>Tip:</strong> Selecciona un curso o material específico para búsquedas más precisas, o déjalo en "Todos" para buscar en toda la base de conocimiento.
          </p>
        </div>

        <!-- Chat Container -->
        <div class="bg-white shadow rounded-lg overflow-hidden">
          <!-- Messages Area -->
          <div class="h-96 overflow-y-auto p-6 space-y-4 bg-gray-50">
            <!-- Welcome Message -->
            <div v-if="messages.length === 0" class="text-center py-12">
              <div class="text-6xl mb-4">🤖</div>
              <h3 class="text-xl font-semibold text-gray-900 mb-2">¡Hola! Soy tu asistente RAG</h3>
              <p class="text-gray-600 mb-4">Puedo ayudarte a encontrar información en los materiales del curso</p>
              <div class="text-left max-w-md mx-auto bg-white rounded-lg p-4 shadow-sm">
                <p class="text-sm font-semibold text-gray-700 mb-2">Ejemplos de preguntas:</p>
                <ul class="text-sm text-gray-600 space-y-1">
                  <li>• ¿Qué es una base de datos relacional?</li>
                  <li>• Explícame el concepto de normalización</li>
                  <li>• Resume los puntos principales del material</li>
                  <li>• ¿Qué diferencias hay entre SQL y NoSQL?</li>
                </ul>
              </div>
            </div>

            <!-- Message History -->
            <div v-for="(msg, index) in messages" :key="index" :class="['flex', msg.role === 'user' ? 'justify-end' : 'justify-start']">
              <div :class="['max-w-lg px-4 py-3 rounded-lg shadow-sm', msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white text-gray-900 border border-gray-200']">
                <!-- User Message -->
                <div v-if="msg.role === 'user'" class="flex items-start">
                  <span class="mr-2">👤</span>
                  <p class="whitespace-pre-wrap">{{ msg.content }}</p>
                </div>
                
                <!-- Assistant Message -->
                <div v-else class="space-y-2">
                  <div class="flex items-start">
                    <span class="mr-2 text-blue-600">🤖</span>
                    <p class="whitespace-pre-wrap text-sm">{{ msg.content }}</p>
                  </div>
                  
                  <!-- Sources -->
                  <div v-if="msg.sources && msg.sources.length > 0" class="mt-3 pt-3 border-t border-gray-200">
                    <p class="text-xs font-semibold text-gray-500 mb-2">📚 Fuentes consultadas:</p>
                    <div class="space-y-1">
                      <div v-for="(source, idx) in msg.sources" :key="idx" class="text-xs text-gray-600 bg-gray-50 rounded p-2">
                        <p class="font-medium">{{ source.title }}</p>
                        <p class="text-gray-500">{{ source.course }} • {{ source.author }}</p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Context Info -->
                  <p v-if="msg.context" class="text-xs text-gray-400 italic mt-2">{{ msg.context }}</p>
                </div>
              </div>
            </div>

            <!-- Loading Indicator -->
            <div v-if="loading" class="flex justify-start">
              <div class="bg-white text-gray-900 border border-gray-200 px-4 py-3 rounded-lg shadow-sm">
                <div class="flex items-center space-x-2">
                  <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                  <span class="text-sm">Procesando pregunta...</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Input Area -->
          <div class="bg-white border-t border-gray-200 p-4">
            <div class="flex gap-2">
              <input 
                v-model="question" 
                @keyup.enter="sendQuestion" 
                type="text" 
                placeholder="Escribe tu pregunta sobre los materiales..." 
                class="flex-1 rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                :disabled="loading"
              />
              <button 
                @click="sendQuestion" 
                :disabled="loading || !question.trim()" 
                class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                <span v-if="loading">⏳</span>
                <span v-else>Enviar</span>
              </button>
            </div>
            <p class="text-xs text-gray-500 mt-2">
              Presiona <kbd class="px-1 py-0.5 bg-gray-100 border border-gray-300 rounded text-xs">Enter</kbd> para enviar
            </p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ragAPI, coursesAPI, materialsAPI } from '@/services/api'

const messages = ref([])
const question = ref('')
const loading = ref(false)

const courses = ref([])
const materials = ref([])
const selectedCourse = ref('')
const selectedMaterial = ref('')

const availableMaterials = computed(() => {
  if (!selectedCourse.value) return materials.value
  return materials.value.filter(m => m.course_id === selectedCourse.value)
})

const loadCourses = async () => {
  try {
    const response = await coursesAPI.getAll()
    courses.value = response.data || []
  } catch (error) {
    console.error('Error loading courses:', error)
  }
}

const loadMaterials = async () => {
  try {
    const response = await materialsAPI.getAll()
    materials.value = response.data || []
  } catch (error) {
    console.error('Error loading materials:', error)
  }
}

const onCourseChange = () => {
  selectedMaterial.value = '' // Reset material selection when course changes
}

const sendQuestion = async () => {
  if (!question.value.trim() || loading.value) return
  
  messages.value.push({ role: 'user', content: question.value })
  const q = question.value
  question.value = ''
  loading.value = true
  
  try {
    const response = await ragAPI.query(q, selectedCourse.value || null, selectedMaterial.value || null)
    messages.value.push({ 
      role: 'assistant', 
      content: response.data.answer,
      sources: response.data.sources || [],
      context: response.data.context || ''
    })
  } catch (error) {
    console.error('Error:', error)
    messages.value.push({ 
      role: 'assistant', 
      content: 'Error al procesar la pregunta. Por favor, verifica que haya materiales disponibles e intenta nuevamente.',
      sources: [],
      context: 'Error del servidor'
    })
  } finally {
    loading.value = false
    // Auto scroll to bottom
    setTimeout(() => {
      const chatContainer = document.querySelector('.overflow-y-auto')
      if (chatContainer) chatContainer.scrollTop = chatContainer.scrollHeight
    }, 100)
  }
}

const clearChat = () => {
  if (confirm('¿Estás seguro de que quieres limpiar el historial del chat?')) {
    messages.value = []
    question.value = ''
  }
}

onMounted(() => {
  loadCourses()
  loadMaterials()
})
</script>
