<script setup>
import { ref } from 'vue'
import { vMaska } from 'maska/vue'

defineProps({
    loading: Boolean,
})

const emit = defineEmits(['submit'])

const fullName = ref('')
const phone = ref('')
const password = ref('')
const passwordConfirm = ref('')
const passwordError = ref('')
const birthDate = ref('')
const email = ref('')
const gender = ref('')


const getMaxBirthDate = () => {
    const today = new Date()

    return new Date(
        today.getFullYear() - 14,
        today.getMonth(),
        today.getDate()
    )
        .toISOString()
        .split('T')[0]
}

const maxBirthDate = getMaxBirthDate()

const submit = () => {
    passwordError.value = ''

    if (password.value !== passwordConfirm.value) {
        passwordError.value = $t("register.passwordsNotSame")
        return
    }

    emit('submit', {
        full_name: fullName.value,
        phone: phone.value,
        password: password.value,
        birth_date: birthDate.value,
        email: email.value,
        gender: gender.value,
    })
}
</script>

<template>
    <form class="mt-6 space-y-4" @submit.prevent="submit">
        <label>
            {{ $t("register.fullName") }}

            <input v-model="fullName" type="text" required minlength="3" maxlength="127"
                :placeholder="$t('register.fullNameExample')" autocomplete="name" />
        </label>

        <label>
            {{ $t("register.phone") }}

            <input v-model="phone" v-maska="'+380 (##) ###-##-##'" type="tel" required minlength="10" maxlength="20" placeholder="+380 (__) ___-__-__"
                autocomplete="tel" />
        </label>

        <label>
            {{ $t("register.email") }}

            <input v-model="email" type="email" required maxlength="255" placeholder="ivan@example.com"
                autocomplete="email" />
        </label>

        <label>
            {{ $t("register.birthDate") }}

            <input v-model="birthDate" type="date" required :max="maxBirthDate" autocomplete="bday" />
        </label>

        <label>
            {{ $t("register.gender") }}

            <select v-model="gender" required>
                <option value="" disabled>{{ $t("register.genderSelect") }}</option>
                <option value="male">{{ $t("register.genderMale") }}</option>
                <option value="female">{{ $t("register.genderFemale") }}</option>
            </select>
        </label>

        <label>
            {{ $t("register.password") }}

            <input v-model="password" type="password" required minlength="8" maxlength="128"
                :placeholder="$t('register.passwordPlaceholder')" autocomplete="new-password" />
        </label>

        <label>
            {{ $t("register.passwordConfirm") }}

            <input v-model="passwordConfirm" type="password" required minlength="8" maxlength="128"
                :placeholder="$t('register.passwordConfirmPlaceholder')" autocomplete="new-password" />
        </label>

        <p v-if="passwordError" class="text-sm text-red-600">
            {{ passwordError }}
        </p>

        <button type="submit" class="btn btn-primary w-full" :disabled="loading">
            {{ loading ? $t("auth.registerProcess") : $t("auth.register") }}
        </button>
    </form>
</template>