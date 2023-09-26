import { createRouter, createWebHistory } from 'vue-router'

import ErrorPage from '@/pages/ErrorPage'
import HomeView from '@/pages/Home'
import LoginPage from '@/pages/Login'
import NoteListView from '@/pages/NoteList'
import TodosView from '@/pages/Todos'

import i18n from '@/shared/translation'

const routes = [
  {
    path: '/auth',
    name: 'auth',
    component: LoginPage,
  },
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/notes',
    name: 'notes',
    component: () => NoteListView,
  },
  {
    path: '/notes/:noteId/todos',
    name: 'todos',
    component: () => TodosView,
  },
  {
    path: '/404',
    name: 'notFound',
    component: ErrorPage,
    props: { title: '404', message: i18n.global.t('main.pageNotFound') },
  },
  {
    path: '/403',
    name: 'forbidden',
    component: ErrorPage,
    props: { title: '403', message: i18n.global.t('main.permissionsDenied') },
  },
  { path: '/:pathMatch(.*)*', redirect: '/404' },
]

const router = createRouter({
  history: createWebHistory(process.env.VUE_APP_ROUTE_PATH),
  routes,
})

export default router
