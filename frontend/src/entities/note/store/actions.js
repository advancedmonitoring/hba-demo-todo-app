import { debounce } from 'lodash'

import Api from '../api/note'

export const actions = {
  setPage(page) {
    this.page = page
    this.loadNotes()
  },
  setItemsPerPage(itemsPerPage) {
    this.itemsPerPage = itemsPerPage
    this.page = 1
    this.loadNotes()
  },
  setSearchText(searchText) {
    this.searchText = searchText
    this.page = 1
    this.loadNotes()
  },
  setSorting(sortBy) {
    this.sortBy = sortBy
    this.page = 1
    this.loadNotes()
  },
  loadNotes() {
    this.isLoading = true
    this._loadNotes()
  },
  _loadNotes: debounce(async function () {
    const response = await Api.getNotes(this.getNoteFilters)
    this.isLoading = false

    const noteData = response.data
    this.notes = noteData.results
    this.totalItems = noteData.count
  }, 300),
  updateNote(note) {
    this.note = { ...this.note, ...note }
  },
}
