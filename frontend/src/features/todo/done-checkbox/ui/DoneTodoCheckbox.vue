<template>
  <v-checkbox hide-details color="primary" :model-value="todo.done" @update:modelValue="updateTodo($event)" />
</template>

<script setup>
  import { Todo, TodoApi } from '@/entities/todo'

  const props = defineProps({
    todo: {
      type: Todo,
      required: true,
    },
  })

  const updateTodo = (done) => {
    TodoApi.updateTodo({ todoId: props.todo.id, noteId: props.todo.noteId, done })
  }
</script>
