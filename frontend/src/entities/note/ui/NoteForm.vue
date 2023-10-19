<template>
  <Field name="name" v-slot="{ field, errors }" v-model="newNote.name" rules="required">
    <BaseTextField v-bind="field" :error-messages="errors" @keyup.enter="onEnter" :label="$t('notes.model.name')" />
  </Field>
</template>

<script setup>
  import { cloneDeep } from 'lodash'
  import { Field, useForm, useIsFormValid } from 'vee-validate'
  import { watch, ref, watchEffect } from 'vue'

  import BaseTextField from '@/shared/ui/BaseTextField'

  import { Note } from '../model/note'

  const emits = defineEmits(['update:isValid', 'update:note', 'submit'])

  const props = defineProps({
    note: Note,
    isValid: {
      type: Boolean,
      default: false,
    },
  })

  const { setErrors } = useForm()
  const newNote = ref(cloneDeep(props.note))
  const isValid = useIsFormValid()

  const onEnter = () => {
    if (isValid.value) emits('submit')
  }

  watchEffect(() => emits('update:isValid', isValid))

  watch(
    newNote,
    (val) => {
      emits('update:note', val)
    },
    { deep: true }
  )

  defineExpose({
    setErrors,
  })
</script>
