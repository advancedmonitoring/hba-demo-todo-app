<template>
  <v-dialog @click:outside="close" :model-value="isOpen" @close="close" max-width="500px">
    <template v-for="(slot, index) of Object.keys($slots)" :key="index" v-slot:[slot]>
      <slot :name="slot"></slot>
    </template>

    <v-card>
      <v-card-title>
        <span class="text-h5">{{ $t('todos.addingTodoTitle') }}</span>
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
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'

  import { Todo, TodoApi, TodoForm } from '@/entities/todo'

  import BaseButton from '@/shared/ui/BaseButton'

  defineProps({
    isOpen: Boolean,
  })

  const emit = defineEmits(['update:isOpen'])
  const router = useRouter()
  const currentNoteId = ref(router.currentRoute.value.params.noteId)
  const todo = ref(
    new Todo({
      noteId: currentNoteId.value,
    })
  )

  const close = () => {
    todo.value = new Todo({
      noteId: currentNoteId.value,
    })
    emit('update:isOpen', false)
  }
  const isValid = ref(false)

  const save = () => TodoApi.createTodo(todo.value).finally(close)
</script>
