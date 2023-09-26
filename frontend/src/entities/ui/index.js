import { defineStore } from 'pinia'

import { actions } from './actions'
import { socket_actions } from './socket_actions'

export const useUiStore = defineStore('ui', {
  state: () => ({
    releaseVersion: 'No data',
    dataLoaded: false,
    sidebarOpened: false,
    languages: {
      ru: {
        lang: 'ru',
        name: 'Русский',
      },
      en: {
        lang: 'en',
        name: 'English',
      },
    },
  }),
  actions: {
    ...socket_actions,
    ...actions,
  },
  $reset() {
    this.sidebarOpened = false
  },
})
