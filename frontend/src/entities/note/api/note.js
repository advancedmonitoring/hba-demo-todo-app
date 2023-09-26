import transport from '@/shared/api/transport'

class NoteApi {
  appName = 'notes'

  getNotes = (params) => {
    return transport.sendGet(`${this.appName}/`, { params })
  }

  createNote = ({ name }) => {
    return transport.sendPost(`${this.appName}/`, { name })
  }

  getNote = ({ noteId }) => {
    return transport.sendGet(`${this.appName}/${noteId}/`)
  }

  updateNote = ({ noteId, name }) => {
    return transport.sendPatch(`${this.appName}/${noteId}/`, { name })
  }

  deleteNote = ({ noteId }) => {
    return transport.sendDelete(`${this.appName}/${noteId}/`)
  }
}

export default new NoteApi()
