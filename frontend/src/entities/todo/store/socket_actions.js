import router from '@/shared/router'

export const socket_actions = {
  SOCKET_note_load_end() {
    this.noteLoaded = true
  },
  SOCKET_close_note() {
    this.todos = []
    this.noteLoaded = false
    router.push({ name: 'notes' }).catch()
  },
}
