import { defineStore } from 'pinia'

import { actions } from './actions'
import { getters } from './getters'
import { socket_actions } from './socket_actions'

export const useAlertsStore = defineStore('alert', {
  state: () => ({
    alerts: [],
    paused: false,
  }),
  getters: getters,
  actions: {
    ...socket_actions,
    ...actions,
  },
  $reset() {
    this.alerts = []
    this.paused = false
  },
})
