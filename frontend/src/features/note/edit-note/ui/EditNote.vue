<template>
  <v-dialog @click:outside="close" :model-value="isOpen" @close="close" max-width="500px">
    <template #activator="{ props }">
      <slot name="button" v-bind="props" />
    </template>
    <v-card>
      <v-card-title>
        <span class="text-h5">{{ $t('notes.editingNoteTitle') }}</span>
      </v-card-title>

      <v-card-text>
        <NoteForm v-model:note="note" v-model:isValid="isValid" @submit="save" />
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
  import { storeToRefs } from 'pinia'
  import { ref } from 'vue'

  import { useNotesStore, NoteApi, Note, NoteForm } from '@/entities/note'

  import BaseButton from '@/shared/ui/BaseButton'

  const props = defineProps({
    isOpen: Boolean,
    noteId: String || Number,
  })

  const emits = defineEmits(['update:isOpen'])

  const noteStore = useNotesStore()
  const { getNoteById } = storeToRefs(noteStore)
  const note = ref(new Note(getNoteById.value(props.noteId)))
  const isValid = ref(false)

  const close = () => emits('update:isOpen', false)

  const save = () => {
    NoteApi.updateNote({ noteId: note.value.id, name: note.value.name }).finally(close)
  }
</script>
