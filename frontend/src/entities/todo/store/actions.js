import { dispatch } from '@/shared/utils/dispatch'

export const actions = {
  openNote(noteId) {
    const params = {
      event: 'open_note',
      data: {
        noteId,
      },
    }
    dispatch('socket', 'sendData', params)
  },
  closeNote() {
    const params = {
      event: 'close_note',
      data: {},
    }
    dispatch('socket', 'sendData', params)
  },
}
