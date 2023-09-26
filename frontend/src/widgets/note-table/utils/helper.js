import { storeToRefs } from 'pinia'

import { useUserStore } from '@/entities/user'

export const getAuthorNameById = (authorId) => {
  const userStore = useUserStore()
  const { user } = storeToRefs(userStore)
  return user.value.id === authorId ? user.value.username : '-'
}
