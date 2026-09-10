<script setup>
import { ref } from 'vue'

defineProps({
  loading: Boolean,
})

const emit = defineEmits(['submit'])

const phone = ref('')
const password = ref('')

const submit = () => {
  emit('submit', phone.value, password.value)
}
</script>

<template>
  <form class="mt-6 space-y-4" @submit.prevent="submit">
    <label>
      Номер телефону

      <input
        v-model="phone"
        type="tel"
        required
        maxlength="20"
        placeholder="+380 50 123 45 67"
        autocomplete="tel"
      />
    </label>

    <label>
      Пароль

      <input
        v-model="password"
        type="password"
        required
        maxlength="128"
        placeholder="Введіть пароль"
        autocomplete="current-password"
      />
    </label>

    <button
      type="submit"
      class="btn btn-primary w-full"
      :disabled="loading"
    >
      {{ loading ? 'Вхід...' : 'Увійти' }}
    </button>
  </form>
</template>