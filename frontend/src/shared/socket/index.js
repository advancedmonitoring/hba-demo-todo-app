import { defineStore } from 'pinia'

import { socket_actions } from './socket_actions'

export const useSocketStore = defineStore({
  id: 'socket',
  state: () => ({
    isConnected: false,
    reconnectError: false,
    socket: {},
  }),
  actions: socket_actions,
})
