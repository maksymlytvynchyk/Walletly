<script setup>
import { ref } from 'vue'
import LoginForm from './LoginForm.vue'
import RegisterForm from './RegisterForm.vue'

const props = defineProps({
  loading: Boolean,

  register: {
    type: Function,
    required: true,
  },
})

const emit = defineEmits(['login'])

const mode = ref('login')

const showLogin = () => {
  mode.value = 'login'
}

const showRegister = () => {
  mode.value = 'register'
}

const handleLogin = (phone, password) => {
  emit('login', phone, password)
}

const handleRegister = async (payload) => {
  const success = await props.register(payload)

  if (success) {
    mode.value = 'login'
  }
}
</script>

<template>
  <section class="mx-auto mt-14 max-w-md card">
    <p class="mb-2 text-xs font-bold tracking-[0.18em] text-brand-700">
      {{ $t("auth.eyebrow") }}
    </p>

    <h1 class="text-3xl font-bold tracking-tight">
      {{ $t("auth.title") }}
    </h1>

    <p class="mt-2 text-slate-600">
      {{ mode === 'login'
        ? $t("auth.loginDescription")
        : $t("auth.createNewAcc")
      }}
    </p>

    <LoginForm
      v-if="mode === 'login'"
      :loading="loading"
      @submit="handleLogin"
    />

    <RegisterForm
      v-else
      :loading="loading"
      @submit="handleRegister"
    />

    <div class="mt-6 text-center text-sm text-slate-600">
      <template v-if="mode === 'login'">
        {{ $t("auth.registerDescription") }}

        <button
          type="button"
          class="font-semibold text-brand-700 hover:underline"
          @click="showRegister"
        >
          {{ $t("auth.register") }}
        </button>
      </template>

      <template v-else>
        {{ $t("register.haveAcc") }}

        <button
          type="button"
          class="font-semibold text-brand-700 hover:underline"
          @click="showLogin"
        >
          {{ $t("auth.login") }}
        </button>
      </template>
    </div>
  </section>
</template>