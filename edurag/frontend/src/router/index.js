import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/courses',
      name: 'courses',
      component: () => import('../views/CoursesView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/courses/:id',
      name: 'course-detail',
      component: () => import('../views/CourseDetailView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/courses/:id/manage',
      name: 'course-manage',
      component: () => import('../views/CourseManageView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/enrollments',
      name: 'enrollments',
      component: () => import('../views/EnrollmentsView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('../views/ChatRAGView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: () => import('../views/AnalyticsView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminView.vue'),
      meta: { requiresAuth: false }
    }
  ],
})

export default router
