import { defineStore } from 'pinia'

import { actions } from './actions'
import { getters } from './getters'
import { socket_actions } from './socket_actions'

export const useTodoStore = defineStore({
  id: 'todo',
  state: () => ({
    noteLoaded: false,
    todos: [],
  }),
  getters: getters,
  actions: {
    ...actions,
    ...socket_actions,
  },
  $reset() {
    this.todos = []
    this.noteLoaded = false
  },
  wsRelated: {
    todo: 'todos',
  },
})
