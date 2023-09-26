import { isArray, isEmpty, isNil } from 'lodash'

import { Note } from '../model/note'

export const getters = {
  notesData: (state) => {
    return state.notes.map((item) => new Note(item))
  },
  getNoteById: (state) => {
    return (noteId) => state.notes.find((note) => note.id === noteId)
  },
  noteData: (state) => {
    return new Note(state.note)
  },
  getNoteFilters: (state) => {
    const params = { ...state.filters }

    params.page = state.page
    params.limit = state.itemsPerPage

    if (!isNil(state.searchText)) {
      params.search = state.searchText
    }

    const sortBy = state.sortBy
    if (!isEmpty(sortBy) && isArray(sortBy)) {
      params.ordering = sortBy[0].order === 'desc' ? `-${sortBy[0].key}` : sortBy[0].key
    }

    return params
  },
}
