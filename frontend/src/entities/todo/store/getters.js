import { Todo } from '../model/todo'

export const getters = {
  todosData: (state) => {
    return state.todos.map((item) => new Todo(item))
  },
  getTodoById: (state) => {
    return (todoId) => state.todos.find((todo) => todo.id === todoId)
  },
}
