import i18n from '@/shared/translation'

export const getDoneTypes = () => {
  return {
    1: {
      id: 1,
      value: true,
      name: i18n.global.t('todos.doneTypes.done'),
    },
    2: {
      id: 2,
      value: false,
      name: i18n.global.t('todos.doneTypes.inProgress'),
    },
  }
}
