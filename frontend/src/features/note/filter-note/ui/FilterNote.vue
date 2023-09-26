<template>
  <BaseTextField
    color="primary"
    hide-details
    density="compact"
    variant="solo"
    @update:modelValue="setSearchText"
    v-model="searchText"
    :label="$t('main.filter')"
  />
</template>

<script setup>
  import { debounce } from 'lodash'
  import { ref } from 'vue'

  import { useNotesStore } from '@/entities/note'

  import BaseTextField from '@/shared/ui/BaseTextField'

  const searchText = ref('')
  const noteStore = useNotesStore()

  const setSearchText = debounce(() => {
    noteStore.setSearchText(searchText.value)
  }, 200)
</script>
