<script setup>
import { ref } from 'vue'
import { vMaska } from 'maska/vue'

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
      {{ $t("auth.phone") }}

      <input
        v-model="phone"
        v-maska="'+380 (##) ###-##-##'"
        type="tel"
        required
        maxlength="20"
        placeholder="+380 (__) ___-__-__"
        autocomplete="tel"
      />
    </label>
    <label>
      {{ $t("auth.password") }}

      <input
        v-model="password"
        type="password"
        required
        maxlength="128"
        :placeholder="$t('auth.enterPassword')"
        autocomplete="current-password"
      />
    </label>

    <button
      type="submit"
      class="btn btn-primary w-full"
      :disabled="loading"
    >
      {{ loading ? $t("auth.loginProcess") : $t("auth.login") }}
    </button>
  </form>
</template>