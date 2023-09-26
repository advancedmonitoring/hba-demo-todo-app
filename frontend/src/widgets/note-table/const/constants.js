import i18n from '@/shared/translation'

export const getNoteHeaders = () => [
  {
    title: i18n.global.t('notes.model.id'),
    key: 'id',
  },
  { title: i18n.global.t('notes.model.author'), key: 'authorName' },
  { title: i18n.global.t('notes.model.name'), key: 'name' },
  { title: i18n.global.t('notes.model.actions'), key: 'actions', sortable: false },
]
