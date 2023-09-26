<template>
  <Field name="text" v-slot="{ field, errors }" v-model="newTodo.text" rules="required">
    <BaseTextField v-bind="field" :error-messages="errors" @keyup.enter="onEnter" :label="$t('todos.model.text')" />
  </Field>
  <Field name="done" v-model="newTodo.done" v-slot="{ value, handleChange, errors }" v-if="newTodo.id">
    <v-checkbox
      :model-value="value"
      hide-details
      :false-value="false"
      density="compact"
      @keyup.enter="onEnter"
      @update:modelValue="handleChange"
      :label="$t('todos.model.done')"
      color="primary"
      :error-messages="errors"
    />
  </Field>
</template>

<script setup>
  import { cloneDeep } from 'lodash'
  import { Field, useForm, useIsFormValid } from 'vee-validate'
  import { watch, ref, watchEffect } from 'vue'

  import BaseTextField from '@/shared/ui/BaseTextField'
  //import BaseCheckbox from '@/shared/ui/BaseCheckbox'

  const emits = defineEmits(['update:isValid', 'update:todo', 'submit'])

  const props = defineProps({
    todo: {
      type: Object,
      required: true,
    },
    isValid: {
      type: Boolean,
      default: false,
    },
  })

  useForm()
  const isValid = useIsFormValid()
  const newTodo = ref(cloneDeep(props.todo))

  const onEnter = () => {
    if (isValid.value) emits('submit')
  }

  watchEffect(() => emits('update:isValid', isValid))

  watch(
    newTodo,
    (val) => {
      emits('update:todo', val)
    },
    { deep: true }
  )
</script>
