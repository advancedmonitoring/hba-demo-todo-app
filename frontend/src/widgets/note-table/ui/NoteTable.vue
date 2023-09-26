<template>
  <v-data-table
    hover
    :headers="getNoteHeaders()"
    v-model:sort-by="sortBy"
    :multi-sort="false"
    :items="notes"
    :items-per-page="itemsPerPage"
    class="elevation-4"
    :loading="isLoading"
    @click:row="goToTodos"
    @update:sortBy="onSortChange"
  >
    <template #top>
      <v-toolbar>
        <AddNote />
        <v-spacer />
        <div class="d-flex px-4 w-25 align-center justify-center">
          <FilterNote />
        </div>
      </v-toolbar>
    </template>
    <template #loader>
      <v-skeleton-loader class="mx-auto border h-100" type="table-tbody, table-tbody, table-tbody" />
    </template>

    <template #item.authorName="{ item }">
      <div>{{ getAuthorNameById(item.raw.authorId) }}</div>
    </template>

    <template #item.actions="{ item }">
      <v-icon size="small" color="primary" class="me-2" @click="editNote($event, item.raw)"> mdi-pencil </v-icon>
      <v-icon size="small" color="primary" @click="deleteNote($event, item.raw)"> mdi-delete </v-icon>
    </template>
    <template #bottom><ToolbarNote /></template>
  </v-data-table>

  <EditNote v-if="isOpenEditModal" :noteId="currentNoteId" v-model:isOpen="isOpenEditModal" />
  <DeleteNote v-if="isOpenDeleteModal" :noteId="currentNoteId" v-model:isOpen="isOpenDeleteModal" />
</template>

<script setup>
  import { storeToRefs } from 'pinia'
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'

  import { AddNote, EditNote, DeleteNote, ToolbarNote, FilterNote } from '@/features/note'

  import { useNotesStore } from '@/entities/note'

  import { getNoteHeaders } from '../const/constants'
  import { getAuthorNameById } from '../utils/helper'

  const router = useRouter()

  const isOpenEditModal = ref(false)
  const isOpenDeleteModal = ref(false)
  const noteStore = useNotesStore()
  const { notesData: notes, itemsPerPage, isLoading, sortBy } = storeToRefs(noteStore)
  const currentNoteId = ref({})

  const editNote = (e, note) => {
    e.stopPropagation()
    currentNoteId.value = note.id
    isOpenEditModal.value = true
  }

  const deleteNote = (e, note) => {
    e.stopPropagation()
    currentNoteId.value = note.id
    isOpenDeleteModal.value = true
  }

  const goToTodos = (e, { item }) => {
    router.push({ name: 'todos', params: { noteId: item.raw.id } })
  }

  const onSortChange = (val) => {
    noteStore.setSorting(val)
  }
</script>
