import transport from '@/shared/api/transport'

class TodoApi {
  appName = 'notes'

  getTodos = ({ noteId }) => {
    return transport.sendGet(`${this.appName}/${noteId}/todos/`)
  }

  createTodo = ({ noteId, text }) => {
    return transport.sendPost(`${this.appName}/${noteId}/todos/`, { text })
  }

  getTodo = ({ noteId, todoId }) => {
    return transport.sendGet(`${this.appName}/${noteId}/todos/${todoId}/`)
  }

  updateTodo = ({ todoId, noteId, text, done }) => {
    return transport.sendPatch(`${this.appName}/${noteId}/todos/${todoId}/`, { text, done })
  }

  deleteTodo = ({ noteId, todoId }) => {
    return transport.sendDelete(`${this.appName}/${noteId}/todos/${todoId}/`)
  }
}

export default new TodoApi()
