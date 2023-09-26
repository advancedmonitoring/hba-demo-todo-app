import i18n from '@/shared/translation'

export const getTodoHeaders = () => [
  {
    title: i18n.global.t('todos.model.id'),
    key: 'id',
  },
  { title: i18n.global.t('notes.model.name'), key: 'noteName' },
  { title: i18n.global.t('todos.model.text'), key: 'text' },
  { title: i18n.global.t('todos.model.done'), key: 'done' },
  { title: i18n.global.t('todos.model.actions'), key: 'actions', sortable: false },
]
