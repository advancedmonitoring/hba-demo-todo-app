<template>
  <div class="flex-column h-100 overflow-hidden">
    <NoteTable />
  </div>
</template>

<script setup>
  import { storeToRefs } from 'pinia'
  import { onMounted } from 'vue'

  import { NoteTable } from '@/widgets/note-table'

  import { useNotesStore } from '@/entities/note'

  const noteStore = useNotesStore()
  const { isLoading } = storeToRefs(noteStore)

  isLoading.value = true

  onMounted(() => {
    noteStore.loadNotes()
  })
</script>

<style scoped lang="scss">
  :deep(.v-table) {
    display: flex;
    height: 100%;
    flex-direction: column;

    & header & footer {
      flex-grow: 0;
    }

    & .v-table__wrapper {
      flex: 1 1 0;
    }
  }
</style>
