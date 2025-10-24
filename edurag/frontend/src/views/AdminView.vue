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
              <router-link to="/chat" class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600">Chat RAG</router-link>
              <router-link to="/analytics" class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600">Analíticas</router-link>
              <router-link to="/admin" class="px-3 py-2 text-sm font-medium text-gray-900 hover:text-blue-600">Administración</router-link>
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
        <h2 class="text-3xl font-bold text-gray-900 mb-2">Panel de Administración</h2>
        <p class="text-gray-600 mb-6">Gestiona estudiantes, cursos, materiales e inscripciones desde aquí</p>

        <!-- Tabs -->
        <div class="border-b border-gray-200 mb-6">
          <nav class="-mb-px flex space-x-8">
            <button @click="activeTab = 'students'" :class="['whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm', activeTab === 'students' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300']">
              👨‍🎓 Estudiantes
            </button>
            <button @click="activeTab = 'courses'" :class="['whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm', activeTab === 'courses' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300']">
              📚 Cursos
            </button>
            <button @click="activeTab = 'materials'" :class="['whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm', activeTab === 'materials' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300']">
              📄 Materiales
            </button>
            <button @click="activeTab = 'enrollments'" :class="['whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm', activeTab === 'enrollments' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300']">
              🎓 Inscripciones
            </button>
          </nav>
        </div>

        <!-- Students Tab -->
        <div v-if="activeTab === 'students'" class="bg-white shadow rounded-lg p-6">
          <h3 class="text-xl font-semibold mb-4">Agregar Nuevo Estudiante</h3>
          
          <div v-if="message" :class="['mb-4 p-4 rounded-md', messageType === 'success' ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800']">
            {{ message }}
          </div>

          <form @submit.prevent="submitStudent" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nombre Completo *</label>
                <input v-model="studentForm.name" type="text" required class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Correo Electrónico *</label>
                <input v-model="studentForm.email" type="email" required class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Cohorte *</label>
              <input v-model="studentForm.cohort" type="text" required placeholder="Ej: 2025-A" class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
            </div>
            <div class="flex gap-2">
              <button type="button" @click="resetForm" class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
                Limpiar
              </button>
              <button type="submit" :disabled="loading" class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50">
                {{ loading ? 'Agregando...' : 'Agregar Estudiante' }}
              </button>
            </div>
          </form>
        </div>

        <!-- Courses Tab -->
        <div v-if="activeTab === 'courses'" class="bg-white shadow rounded-lg p-6">
          <h3 class="text-xl font-semibold mb-4">Agregar Nuevo Curso</h3>
          
          <div v-if="message" :class="['mb-4 p-4 rounded-md', messageType === 'success' ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800']">
            {{ message }}
          </div>

          <form @submit.prevent="submitCourse" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Código del Curso *</label>
                <input v-model="courseForm.code" type="text" required placeholder="Ej: CS-101" class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Créditos *</label>
                <input v-model.number="courseForm.credits" type="number" required min="1" max="10" class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre del Curso *</label>
              <input v-model="courseForm.name" type="text" required class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Programa/Syllabus</label>
              <textarea v-model="courseForm.syllabus" rows="4" class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"></textarea>
            </div>
            <div class="flex gap-2">
              <button type="button" @click="resetForm" class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
                Limpiar
              </button>
              <button type="submit" :disabled="loading" class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50">
                {{ loading ? 'Agregando...' : 'Agregar Curso' }}
              </button>
            </div>
          </form>
        </div>

        <!-- Materials Tab -->
        <div v-if="activeTab === 'materials'" class="bg-white shadow rounded-lg p-6">
          <h3 class="text-xl font-semibold mb-4">Agregar Nuevo Material</h3>
          <p class="text-sm text-gray-600 mb-4">Sube archivos PDF o ingresa texto directamente</p>
          
          <div v-if="message" :class="['mb-4 p-4 rounded-md', messageType === 'success' ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800']">
            {{ message }}
          </div>

          <form @submit.prevent="submitMaterial" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Título *</label>
                <input v-model="materialForm.title" type="text" required class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Curso *</label>
                <select v-model="materialForm.course_id" required class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
                  <option value="">Seleccionar curso</option>
                  <option v-for="course in availableCourses" :key="course.id" :value="course.id">
                    {{ course.code }} - {{ course.name }}
                  </option>
                </select>
              </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Tipo</label>
                <input v-model="materialForm.mime_type" type="text" placeholder="Ej: PDF, Texto, Video" class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Autor</label>
                <input v-model="materialForm.author" type="text" class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">URL del Archivo</label>
              <input v-model="materialForm.file_url" type="url" placeholder="https://" class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500" />
            </div>
            
            <!-- Upload Mode Selection -->
            <div class="border-t pt-4">
              <label class="block text-sm font-medium text-gray-700 mb-3">Método de Carga</label>
              <div class="flex gap-4 mb-4">
                <label class="flex items-center">
                  <input type="radio" v-model="uploadMode" value="pdf" class="mr-2">
                  <span class="text-sm">📄 Subir PDF (Recomendado)</span>
                </label>
                <label class="flex items-center">
                  <input type="radio" v-model="uploadMode" value="text" class="mr-2">
                  <span class="text-sm">📝 Texto Manual</span>
                </label>
              </div>

              <!-- PDF Upload -->
              <div v-if="uploadMode === 'pdf'" class="space-y-3">
                <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
                  <input 
                    type="file" 
                    @change="handleFileSelect" 
                    accept=".pdf"
                    class="hidden" 
                    id="pdf-upload"
                  />
                  <label for="pdf-upload" class="cursor-pointer">
                    <div v-if="!selectedFile" class="space-y-2">
                      <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                      </svg>
                      <div class="text-sm text-gray-600">
                        <span class="font-semibold text-blue-600">Click para seleccionar</span> o arrastra un PDF
                      </div>
                      <p class="text-xs text-gray-500">PDF hasta 50MB</p>
                    </div>
                    <div v-else class="space-y-2">
                      <svg class="mx-auto h-12 w-12 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <p class="text-sm font-medium text-gray-900">{{ selectedFile.name }}</p>
                      <p class="text-xs text-gray-500">{{ formatFileSize(selectedFile.size) }}</p>
                      <button type="button" @click.prevent="clearFile" class="text-sm text-red-600 hover:text-red-800">
                        Cambiar archivo
                      </button>
                    </div>
                  </label>
                </div>
                <div v-if="uploadProgress > 0 && uploadProgress < 100" class="w-full bg-gray-200 rounded-full h-2.5">
                  <div class="bg-blue-600 h-2.5 rounded-full transition-all" :style="{ width: uploadProgress + '%' }"></div>
                </div>
              </div>

              <!-- Text Input (Legacy) -->
              <div v-else>
                <label class="block text-sm font-medium text-gray-700 mb-1">Contenido/Texto *</label>
                <textarea v-model="materialForm.raw_text" rows="6" required placeholder="Ingresa el contenido del material aquí..." class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"></textarea>
                <p class="mt-1 text-xs text-gray-500">⚠️ Método antiguo: Para materiales largos, se recomienda usar PDF</p>
              </div>
            </div>

            <div class="flex gap-2">
              <button type="button" @click="resetForm" class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
                Limpiar
              </button>
              <button type="submit" :disabled="loading || (uploadMode === 'pdf' && !selectedFile)" class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50">
                {{ loading ? 'Procesando...' : (uploadMode === 'pdf' ? 'Subir PDF' : 'Agregar Material') }}
              </button>
            </div>
          </form>

          <!-- Materials List -->
          <div class="mt-8">
            <h4 class="text-lg font-semibold mb-4">📚 Materiales Existentes</h4>
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Título</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Curso</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Autor</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Chunks</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="material in materialsList" :key="material.id">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {{ material.title }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ getCourseNameById(material.course_id) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ material.author || 'N/A' }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm">
                      <span v-if="material.processing_status === 'completed'" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        ✓ Completado
                      </span>
                      <span v-else-if="material.processing_status === 'processing'" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                        ⏳ Procesando
                      </span>
                      <span v-else-if="material.processing_status === 'failed'" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                        ❌ Error
                      </span>
                      <span v-else class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                        ⏸ Pendiente
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ material.chunks_count || 0 }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button 
                        @click="deleteMaterial(material.id, material.title)" 
                        class="text-red-600 hover:text-red-900"
                        :disabled="loading"
                      >
                        🗑️ Eliminar
                      </button>
                    </td>
                  </tr>
                  <tr v-if="materialsList.length === 0">
                    <td colspan="6" class="px-6 py-4 text-center text-sm text-gray-500">
                      No hay materiales agregados todavía
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Enrollments Tab -->
        <div v-if="activeTab === 'enrollments'" class="bg-white shadow rounded-lg p-6">
          <h3 class="text-xl font-semibold mb-4">Agregar Nueva Inscripción</h3>
          
          <div v-if="message" :class="['mb-4 p-4 rounded-md', messageType === 'success' ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800']">
            {{ message }}
          </div>

          <form @submit.prevent="submitEnrollment" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Estudiante *</label>
                <select v-model="enrollmentForm.student_id" required class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
                  <option value="">Seleccionar estudiante</option>
                  <option v-for="student in availableStudents" :key="student.id" :value="student.id">
                    {{ student.name }} ({{ student.email }})
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Curso *</label>
                <select v-model="enrollmentForm.course_id" required class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
                  <option value="">Seleccionar curso</option>
                  <option v-for="course in availableCourses" :key="course.id" :value="course.id">
                    {{ course.code }} - {{ course.name }}
                  </option>
                </select>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado *</label>
              <select v-model="enrollmentForm.status" required class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
                <option value="active">Activo</option>
                <option value="completed">Completado</option>
                <option value="dropped">Abandonado</option>
              </select>
            </div>
            <div class="flex gap-2">
              <button type="button" @click="resetForm" class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
                Limpiar
              </button>
              <button type="submit" :disabled="loading" class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50">
                {{ loading ? 'Inscribiendo...' : 'Inscribir Estudiante' }}
              </button>
            </div>
          </form>
        </div>

        <!-- Statistics -->
        <div class="mt-8 grid grid-cols-1 gap-5 sm:grid-cols-4">
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <dt class="text-sm font-medium text-gray-500 truncate">Total Estudiantes</dt>
              <dd class="mt-1 text-3xl font-semibold text-gray-900">{{ stats.students }}</dd>
            </div>
          </div>
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <dt class="text-sm font-medium text-gray-500 truncate">Total Cursos</dt>
              <dd class="mt-1 text-3xl font-semibold text-gray-900">{{ stats.courses }}</dd>
            </div>
          </div>
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <dt class="text-sm font-medium text-gray-500 truncate">Total Materiales</dt>
              <dd class="mt-1 text-3xl font-semibold text-gray-900">{{ stats.materials }}</dd>
            </div>
          </div>
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <dt class="text-sm font-medium text-gray-500 truncate">Total Inscripciones</dt>
              <dd class="mt-1 text-3xl font-semibold text-gray-900">{{ stats.enrollments }}</dd>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { studentsAPI, coursesAPI, materialsAPI } from '@/services/api'
import api from '@/services/api'

const activeTab = ref('students')
const loading = ref(false)
const message = ref('')
const messageType = ref('success')

const studentForm = ref({ name: '', email: '', cohort: '' })
const courseForm = ref({ code: '', name: '', syllabus: '', credits: 3 })
const materialForm = ref({ title: '', course_id: '', mime_type: '', author: '', file_url: '', raw_text: '' })
const enrollmentForm = ref({ student_id: '', course_id: '', status: 'active' })

// PDF Upload state
const uploadMode = ref('pdf')  // 'pdf' or 'text'
const selectedFile = ref(null)
const uploadProgress = ref(0)

const availableStudents = ref([])
const availableCourses = ref([])
const materialsList = ref([])
const stats = ref({ students: 0, courses: 0, materials: 0, enrollments: 0 })

const loadData = async () => {
  try {
    const [studentsRes, coursesRes, materialsRes] = await Promise.all([
      studentsAPI.getAll(),
      coursesAPI.getAll(),
      materialsAPI.getAll()
    ])
    availableStudents.value = studentsRes.data.data || studentsRes.data
    availableCourses.value = coursesRes.data.data || coursesRes.data
    materialsList.value = materialsRes.data.data || materialsRes.data
    stats.value = {
      students: availableStudents.value.length,
      courses: availableCourses.value.length,
      materials: materialsList.value.length,
      enrollments: 0
    }
  } catch (error) {
    console.error('Error loading data:', error)
  }
}

const submitStudent = async () => {
  loading.value = true
  message.value = ''
  try {
    await studentsAPI.create(studentForm.value)
    message.value = '✅ Estudiante agregado exitosamente'
    messageType.value = 'success'
    resetForm()
    loadData()
  } catch (error) {
    message.value = `❌ Error: ${error.response?.data?.detail || error.message}`
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}

const submitCourse = async () => {
  loading.value = true
  message.value = ''
  try {
    await api.post('/api/courses', courseForm.value)
    message.value = '✅ Curso agregado exitosamente'
    messageType.value = 'success'
    resetForm()
    loadData()
  } catch (error) {
    message.value = `❌ Error: ${error.response?.data?.detail || error.message}`
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}

const submitMaterial = async () => {
  loading.value = true
  message.value = ''
  uploadProgress.value = 0
  
  try {
    if (uploadMode.value === 'pdf') {
      // PDF Upload Mode
      if (!selectedFile.value) {
        message.value = '❌ Por favor selecciona un archivo PDF'
        messageType.value = 'error'
        loading.value = false
        return
      }

      // Create FormData for file upload
      const formData = new FormData()
      formData.append('file', selectedFile.value)
      formData.append('title', materialForm.value.title)
      formData.append('course_id', materialForm.value.course_id)
      if (materialForm.value.author) {
        formData.append('author', materialForm.value.author)
      }

      // Upload PDF
      const response = await materialsAPI.uploadPDF(formData)
      
      message.value = `✅ ${response.data.message}\n📊 Tamaño: ${response.data.file_size_mb}MB\n⏳ El PDF se está procesando en segundo plano (chunking + embeddings)`
      messageType.value = 'success'
      uploadProgress.value = 100
      
    } else {
      // Text Mode (Legacy)
      await materialsAPI.create(materialForm.value)
      message.value = '✅ Material agregado exitosamente'
      messageType.value = 'success'
    }
    
    resetForm()
    loadData()
    
  } catch (error) {
    const errorDetail = error.response?.data?.detail || error.message
    message.value = `❌ Error: ${errorDetail}`
    messageType.value = 'error'
    uploadProgress.value = 0
  } finally {
    loading.value = false
  }
}

// PDF Upload Helpers
const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    if (file.type !== 'application/pdf') {
      message.value = '❌ Por favor selecciona un archivo PDF válido'
      messageType.value = 'error'
      return
    }
    
    const maxSize = 50 * 1024 * 1024 // 50MB
    if (file.size > maxSize) {
      message.value = `❌ El archivo es demasiado grande. Máximo 50MB, actual: ${formatFileSize(file.size)}`
      messageType.value = 'error'
      return
    }
    
    selectedFile.value = file
    message.value = ''
  }
}

const clearFile = () => {
  selectedFile.value = null
  uploadProgress.value = 0
  const fileInput = document.getElementById('pdf-upload')
  if (fileInput) fileInput.value = ''
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const submitEnrollment = async () => {
  loading.value = true
  message.value = ''
  try {
    // Send IDs as strings (UUIDs) - no conversion needed
    const enrollmentData = {
      student_id: enrollmentForm.value.student_id,
      course_id: enrollmentForm.value.course_id,
      status: enrollmentForm.value.status
    }
    await api.post('/api/enrollments', enrollmentData)
    message.value = '✅ Inscripción creada exitosamente'
    messageType.value = 'success'
    resetForm()
    loadData()
  } catch (error) {
    message.value = `❌ Error: ${error.response?.data?.detail || error.message}`
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  studentForm.value = { name: '', email: '', cohort: '' }
  courseForm.value = { code: '', name: '', syllabus: '', credits: 3 }
  materialForm.value = { title: '', course_id: '', mime_type: '', author: '', file_url: '', raw_text: '' }
  enrollmentForm.value = { student_id: '', course_id: '', status: 'active' }
  message.value = ''
  
  // Clear PDF upload state
  clearFile()
  uploadProgress.value = 0
}

// Delete material
const deleteMaterial = async (materialId, materialTitle) => {
  if (!confirm(`¿Estás seguro de que quieres eliminar "${materialTitle}"?\n\nEsto también eliminará todos sus chunks y embeddings asociados.`)) {
    return
  }
  
  loading.value = true
  message.value = ''
  
  try {
    await materialsAPI.delete(materialId)
    message.value = `✅ Material "${materialTitle}" eliminado exitosamente`
    messageType.value = 'success'
    loadData()
  } catch (error) {
    message.value = `❌ Error al eliminar: ${error.response?.data?.detail || error.message}`
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}

// Helper to get course name by ID
const getCourseNameById = (courseId) => {
  const course = availableCourses.value.find(c => c.id === courseId)
  return course ? `${course.code} - ${course.name}` : 'N/A'
}

onMounted(() => {
  loadData()
})
</script>
