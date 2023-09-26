<template>
  <v-select
    color="primary"
    clearable
    variant="solo"
    hide-details
    density="compact"
    :label="$t('todos.doneTypes.title')"
    :items="Object.values(getDoneTypes())"
    item-title="name"
    item-value="value"
  />
</template>

<script setup>
  import { getDoneTypes } from '../const/constants'
</script>
