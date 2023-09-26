export const socket_actions = {
  SOCKET_note_added() {
    this.loadNotes()
  },
  SOCKET_note_updated(note) {
    const index = this.notes.findIndex((item) => item.id === note.id)
    if (index !== -1) {
      this.notes[index] = { ...this.notes[index], ...note }
    }

    if (this.note?.id === note.id) {
      this.updateNote(note)
    }
  },
  SOCKET_note_deleted({ noteId }) {
    if (this.note?.id === noteId) {
      this.closeNote()
    }

    this.loadNotes()
  },
  SOCKET_note_data(note) {
    this.note = note
  },
  SOCKET_close_note() {
    this.note = {}
  },
}
