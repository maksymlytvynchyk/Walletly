<script setup>
import { ref } from 'vue'
import { vMaska } from 'maska/vue'
import { useI18n } from "vue-i18n";

const { t } = useI18n();
defineProps({
    loading: Boolean,
    fieldErrors: {
        type: Object,
        default: () => ({}),
    },
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

const errors = ref({})


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
    errors.value = {}
    passwordError.value = ''

    if (password.value !== passwordConfirm.value) {
        passwordError.value = t("register.passwordsNotSame")
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
            <p v-if="fieldErrors.full_name" class="mt-1 text-sm text-red-600">
                {{ $t(`errors.${fieldErrors.full_name}`) }}
            </p>
        </label>

        <label>
            {{ $t("register.phone") }}

            <input v-model="phone" v-maska="'+380 (##) ###-##-##'" type="tel" required minlength="10" maxlength="20"
                placeholder="+380 (__) ___-__-__" autocomplete="tel" />
            <p v-if="fieldErrors.phone" class="mt-1 text-sm text-red-600">
                {{ $t(`errors.${fieldErrors.phone}`) }}
            </p>
        </label>

        <label>
            {{ $t("register.email") }}

            <input v-model="email" type="email" required maxlength="255" placeholder="ivan@example.com"
                autocomplete="email" />
            <p v-if="fieldErrors.email" class="mt-1 text-sm text-red-600">
                {{ $t(`errors.${fieldErrors.email}`) }}
            </p>
        </label>

        <label>
            {{ $t("register.birthDate") }}

            <input v-model="birthDate" type="date" required :max="maxBirthDate" autocomplete="bday" />
            <p v-if="fieldErrors.birth_date" class="mt-1 text-sm text-red-600">
                {{ $t(`errors.${fieldErrors.birth_date}`) }}
            </p>
        </label>

        <label>
            {{ $t("register.gender") }}

            <select v-model="gender" required>
                <option value="" disabled>{{ $t("register.genderSelect") }}</option>
                <option value="male">{{ $t("register.genderMale") }}</option>
                <option value="female">{{ $t("register.genderFemale") }}</option>
            </select>
            <p v-if="fieldErrors.gender" class="mt-1 text-sm text-red-600">
                {{ $t(`errors.${fieldErrors.gender}`) }}
            </p>
        </label>

        <label>
            {{ $t("register.password") }}

            <input v-model="password" type="password" required minlength="8" maxlength="128"
                :placeholder="$t('register.passwordPlaceholder')" autocomplete="new-password" />
            <p v-if="fieldErrors.password" class="mt-1 text-sm text-red-600">
                {{ $t(`errors.${fieldErrors.password}`) }}
            </p>
        </label>

        <label>
            {{ $t("register.passwordConfirm") }}

            <input v-model="passwordConfirm" type="password" required minlength="8" maxlength="128"
                :placeholder="$t('register.passwordConfirmPlaceholder')" autocomplete="new-password" />
            <p v-if="fieldErrors.password" class="mt-1 text-sm text-red-600">
                {{ $t(`errors.${fieldErrors.password}`) }}
            </p>
        </label>

        <p v-if="passwordError" class="text-sm text-red-600">
            {{ passwordError }}
        </p>

        <button type="submit" class="btn btn-primary w-full" :disabled="loading">
            {{ loading ? $t("auth.registerProcess") : $t("auth.register") }}
        </button>
    </form>
</template>