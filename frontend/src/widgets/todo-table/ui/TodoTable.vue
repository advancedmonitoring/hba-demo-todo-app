<template>
  <v-data-table
    hover
    :headers="getTodoHeaders()"
    :items="filteredTodos"
    :items-per-page="-1"
    :sort-by="[{ key: 'id', order: 'desc' }]"
    class="elevation-4"
  >
    <template #top>
      <v-toolbar>
        <BaseButton class="mr-2" :label="$t('main.back')" variant="text" @click="back" />
        <AddTodo v-model:isOpen="isOpenAddModal">
          <template #activator="{ props }">
            <BaseButton :label="$t('main.add')" v-bind="props" @click="addTodo" />
          </template>
        </AddTodo>
        <v-spacer />
        <div class="d-flex px-4 w-25 align-center justify-center">
          <DoneFilter v-model="done" />
        </div>
      </v-toolbar>
    </template>

    <template #item.done="{ item }">
      <DoneTodoCheckbox :todo="item.raw" />
    </template>

    <template #item.id="{ item }">
      <div v-bind:class="{ 'text-decoration-line-through': item.raw.done }">{{ item.raw.id }}</div>
    </template>

    <template #item.noteName="{ item }">
      <div v-bind:class="{ 'text-decoration-line-through': item.raw.done }">{{ item.raw.note.name }}</div>
    </template>

    <template #item.text="{ item }">
      <div v-bind:class="{ 'text-decoration-line-through': item.raw.done }">{{ item.raw.text }}</div>
    </template>

    <template #item.actions="{ item }">
      <v-icon size="small" color="primary" class="me-2" @click="editTodo(item.raw.id)"> mdi-pencil</v-icon>
      <v-icon size="small" color="primary" @click="deleteTodo(item.raw.id)"> mdi-delete</v-icon>
    </template>
    <template #bottom />
  </v-data-table>

  <EditTodo v-if="isOpenEditModal" v-model:todo-id="currentTodoId" v-model:isOpen="isOpenEditModal" />
  <DeleteTodo v-if="isOpenDeleteModal" v-model:todo-id="currentTodoId" v-model:isOpen="isOpenDeleteModal" />
</template>

<script setup>
  import { isNil } from 'lodash'
  import { storeToRefs } from 'pinia'
  import { computed, ref } from 'vue'
  import { useRouter } from 'vue-router'

  import { AddTodo, EditTodo, DeleteTodo, DoneTodoCheckbox, DoneFilter } from '@/features/todo'

  import { useTodoStore } from '@/entities/todo'

  import BaseButton from '@/shared/ui/BaseButton'

  import { getTodoHeaders } from '../const/constants'

  const isOpenAddModal = ref(false)
  const isOpenEditModal = ref(false)
  const isOpenDeleteModal = ref(false)
  const done = ref(null)
  const router = useRouter()
  const todoStore = useTodoStore()
  const currentTodoId = ref(null)
  const { todosData: todos } = storeToRefs(todoStore)

  const filteredTodos = computed(() => {
    if (isNil(done.value)) return todos.value

    return todos.value.filter((item) => item.done === done.value)
  })

  const addTodo = () => (isOpenAddModal.value = true)
  const editTodo = (todoId) => {
    currentTodoId.value = todoId
    isOpenEditModal.value = true
  }
  const deleteTodo = (todoId) => {
    currentTodoId.value = todoId
    isOpenDeleteModal.value = true
  }

  const back = () => router.push({ name: 'notes' })
</script>
