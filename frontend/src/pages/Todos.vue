<template>
  <div class="flex-column">
    <Transition>
      <v-skeleton-loader
        v-if="!noteLoaded"
        class="mx-auto border h-100"
        type="table-heading, table-tbody, table-tbody, table-tbody"
      />
      <TodoTable v-else />
    </Transition>
  </div>
</template>

<script setup>
  import { storeToRefs } from 'pinia'
  import { onMounted, onUnmounted } from 'vue'
  import { useRouter } from 'vue-router'

  import { TodoTable } from '@/widgets/todo-table'

  import { useTodoStore } from '@/entities/todo'

  const todoStore = useTodoStore()
  const router = useRouter()
  const { noteLoaded } = storeToRefs(todoStore)

  onMounted(() => {
    todoStore.openNote(router.currentRoute.value.params.noteId)
  })

  onUnmounted(() => {
    todoStore.closeNote()
  })
</script>
