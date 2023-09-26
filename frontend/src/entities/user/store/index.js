import { defineStore } from 'pinia'

import { actions } from './actions'
import { getters } from './getters'
import { socket_actions } from './socket_actions'

export const useUserStore = defineStore('user', {
  state: () => ({
    userData: {},
    isLogged: false,
  }),
  getters: getters,
  actions: {
    ...socket_actions,
    ...actions,
  },
  $reset() {
    this.isLogged = false
    this.userData = {}
  },
})
