<template>
  <v-dialog @click:outside="close" :model-value="isOpen" @close="close" max-width="500px">
    <v-card>
      <v-card-title class="text-h5">{{ $t('todos.deletingTodoTitle') }}</v-card-title>
      <v-card-text>
        {{ $t('todos.actions.confirmDelete', [todo.text]) }}
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

  import { useTodoStore, TodoApi, Todo } from '@/entities/todo'

  import BaseButton from '@/shared/ui/BaseButton'

  const props = defineProps({
    isOpen: Boolean,
    todoId: Number || String,
  })

  const emits = defineEmits(['update:isOpen'])

  const todoStore = useTodoStore()
  const { getTodoById } = storeToRefs(todoStore)
  const todo = ref(new Todo(getTodoById.value(props.todoId)))

  const close = () => {
    emits('update:isOpen', false)
  }

  const deleteItem = () => {
    TodoApi.deleteTodo({ ...todo.value, todoId: props.todoId }).finally(close)
  }
</script>
