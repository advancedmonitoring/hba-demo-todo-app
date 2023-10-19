<template>
  <v-dialog @click:outside="close" v-model="isOpenAddModal" @close="close" max-width="500px">
    <template #activator>
      <BaseButton :label="$t('main.add')" @click="addNote" />
    </template>

    <v-card>
      <v-card-title>
        <span class="text-h5">{{ $t('notes.addingNoteTitle') }}</span>
      </v-card-title>

      <v-card-text>
        <NoteForm ref="noteForm" v-model:note="note" v-model:isValid="isValid" @submit="save" />
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <BaseButton :label="$t('main.cancel')" @click="close" />
        <BaseButton :label="$t('main.save')" :disabled="!isValid" primary @click="save" />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
  import { ref } from 'vue'

  import { Note, NoteApi, NoteForm } from '@/entities/note'

  import BaseButton from '@/shared/ui/BaseButton'
  const noteForm = ref(null)
  const note = ref(new Note({}))

  const isOpenAddModal = ref(false)
  const isValid = ref(false)

  const addNote = () => (isOpenAddModal.value = true)

  const close = () => {
    note.value = new Note({})
    isOpenAddModal.value = false
  }

  const save = () =>
    NoteApi.createNote(note.value)
      .then(close)
      .catch((e) => {
        noteForm.value.setErrors(e?.validationErrors || {})
      })
</script>
