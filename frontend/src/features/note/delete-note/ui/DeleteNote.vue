<template>
  <v-dialog @click:outside="close" :model-value="isOpen" @close="close" max-width="500px">
    <v-card>
      <v-card-title class="text-h5">{{ $t('notes.deletingNoteTitle') }}</v-card-title>
      <v-card-text>
        {{ $t('notes.actions.confirmDelete', [note.name]) }}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <BaseButton :label="$t('main.no')" @click="close" />
        <BaseButton :label="$t('main.yes')" primary @click="deleteItem" />
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
  import { storeToRefs } from 'pinia'
  import { ref } from 'vue'

  import { useNotesStore, NoteApi, Note } from '@/entities/note'

  import BaseButton from '@/shared/ui/BaseButton'

  const props = defineProps({
    isOpen: Boolean,
    noteId: String || Number,
  })

  const emits = defineEmits(['update:isOpen'])

  const noteStore = useNotesStore()
  const { getNoteById } = storeToRefs(noteStore)
  const note = ref(new Note(getNoteById.value(props.noteId)))

  const close = () => emits('update:isOpen', false)

  const deleteItem = () => {
    NoteApi.deleteNote({ noteId: note.value.id }).finally(close)
  }
</script>
