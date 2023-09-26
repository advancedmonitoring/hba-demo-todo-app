<template>
  <v-dialog @click:outside="close" :model-value="isOpen" @close="close" max-width="500px">
    <template #activator="{ props }">
      <slot name="button" v-bind="props" />
    </template>
    <v-card>
      <v-card-title>
        <span class="text-h5">{{ $t('todos.editingTodoTitle') }}</span>
      </v-card-title>

      <v-card-text>
        <TodoForm v-model:todo="todo" v-model:isValid="isValid" @submit="save" />
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

  import { useTodoStore, TodoApi, Todo, TodoForm } from '@/entities/todo'

  import BaseButton from '@/shared/ui/BaseButton'

  const props = defineProps({
    isOpen: Boolean,
    todoId: String || Number,
  })

  const emits = defineEmits(['update:isOpen'])

  const todoStore = useTodoStore()
  const { getTodoById } = storeToRefs(todoStore)
  const isValid = ref(false)
  const todo = ref(new Todo(getTodoById.value(props.todoId)))

  const close = () => {
    emits('update:isOpen', false)
  }

  const save = () => {
    TodoApi.updateTodo({ ...todo.value, todoId: props.todoId }).finally(close)
  }
</script>
