import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

export const coursesAPI = {
  getAll: () => api.get('/api/courses'),
  getById: (id) => api.get(`/api/courses/${id}`),
  getMaterials: (id) => api.get(`/api/courses/${id}/materials`),
  enroll: (studentId, courseId) => api.post('/api/enrollments', { student_id: studentId, course_id: courseId, status: 'active' })
}

export const materialsAPI = {
  getAll: () => api.get('/api/materials'),
  getById: (id) => api.get(`/api/materials/${id}`),
  getByCourse: (courseId) => api.get(`/api/courses/${courseId}/materials`),
  uploadPDF: (formData) => api.post('/api/materials/upload-pdf', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  create: (data) => api.post('/api/materials', data),
  delete: (id) => api.delete(`/api/materials/${id}`)
}

export const ragAPI = {
  query: (question, courseId = null, materialId = null) => api.post('/api/rag/query', { 
    question, 
    course_id: courseId,
    material_id: materialId
  }),
  health: () => api.get('/api/rag/health')
}

export const analyticsAPI = {
  getStats: () => api.get('/api/analytics/stats'),
  getDetailed: () => api.get('/api/analytics/detailed'),
  getCourseActivity: () => api.get('/api/analytics/course-activity'),
  getStudentProgress: () => api.get('/api/analytics/student-progress')
}

export const studentsAPI = {
  getAll: () => api.get('/api/students'),
  create: (data) => api.post('/api/students', data),
  getById: (id) => api.get(`/api/students/${id}`),
  update: (id, data) => api.put(`/api/students/${id}`, data),
  delete: (id) => api.delete(`/api/students/${id}`)
}

export default api
