import { defineStore } from 'pinia'

import { actions } from './actions'
import { getters } from './getters'
import { socket_actions } from './socket_actions'

export const useNotesStore = defineStore({
  id: 'note',
  state: () => ({
    page: 1,
    itemsPerPage: 25,
    totalItems: 0,
    filters: {},
    sortBy: [{ key: 'id', order: 'desc' }],
    searchText: null,

    isLoading: false,

    note: {},
    notes: [],
  }),
  getters: getters,
  actions: {
    ...socket_actions,
    ...actions,
  },
  $reset() {
    this.note = {}
    this.notes = []
  },
})
