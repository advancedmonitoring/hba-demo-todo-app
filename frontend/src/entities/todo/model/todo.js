import { get } from '@/shared/utils/dispatch'

export class Todo {
  constructor(data) {
    this.id = data.id
    this.noteId = data.noteId
    this.text = data.text
    this.done = data.done
  }

  get note() {
    return get('note', 'noteData')
  }
}
