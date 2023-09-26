<template>
  <v-toolbar tag="footer">
    <div class="px-2">{{ $t('main.itemsPerPage') }}</div>
    <div class="px-4">
      <v-select
        color="primary"
        density="compact"
        variant="solo"
        hide-details
        @update:modelValue="noteStore.setItemsPerPage($event)"
        v-model="itemsPerPage"
        :items="perPageChoices"
      />
    </div>

    <v-btn color="primary" icon="mdi-chevron-left" :disabled="page === 1" @click="noteStore.setPage(page - 1)" />
    <div class="px-4">{{ page }}</div>
    <v-btn color="primary" icon="mdi-chevron-right" :disabled="!hasMoreNotes" @click="noteStore.setPage(page + 1)" />
  </v-toolbar>
</template>

<script setup>
  import { storeToRefs } from 'pinia'
  import { computed } from 'vue'

  import { useNotesStore } from '@/entities/note'

  import { perPageChoices } from '../const/constants'

  const noteStore = useNotesStore()
  const { totalItems, page, itemsPerPage } = storeToRefs(noteStore)

  const hasMoreNotes = computed(() => {
    return totalItems.value / itemsPerPage.value > page.value
  })
</script>

<style scoped lang="scss">
  :deep(.v-toolbar__content) {
    padding: 0 16px;
    display: flex;
    justify-content: flex-end;
  }
</style>
