<script setup>
import { ref } from 'vue'
import { IMaskDirective as vImask } from 'vue-imask'

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

const phoneMask = {
    mask: '+380 (00) 000-00-00',
    lazy: false,
}

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
        passwordError.value = 'Паролі не збігаються'
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
            ПІБ

            <input v-model="fullName" type="text" required minlength="3" maxlength="127"
                placeholder="Наприклад, Іван Петренко" autocomplete="name" />
        </label>

        <label>
            Номер телефону

            <input v-model="phone" v-imask="phoneMask" type="text" required minlength="10" maxlength="20" placeholder="+380 (__) ___-__-__"
                autocomplete="tel" />
        </label>

        <label>
            Електронна пошта

            <input v-model="email" type="email" required maxlength="255" placeholder="ivan@example.com"
                autocomplete="email" />
        </label>

        <label>
            Дата народження

            <input v-model="birthDate" type="date" required :max="maxBirthDate" autocomplete="bday" />
        </label>

        <label>
            Стать

            <select v-model="gender" required>
                <option value="" disabled>Оберіть стать</option>
                <option value="male">Чоловіча</option>
                <option value="female">Жіноча</option>
            </select>
        </label>

        <label>
            Пароль

            <input v-model="password" type="password" required minlength="8" maxlength="128"
                placeholder="Мінімум 8 символів" autocomplete="new-password" />
        </label>

        <label>
            Підтвердження пароля

            <input v-model="passwordConfirm" type="password" required minlength="8" maxlength="128"
                placeholder="Повторіть пароль" autocomplete="new-password" />
        </label>

        <p v-if="passwordError" class="text-sm text-red-600">
            {{ passwordError }}
        </p>

        <button type="submit" class="btn btn-primary w-full" :disabled="loading">
            {{ loading ? 'Створення...' : 'Зареєструватися' }}
        </button>
    </form>
</template>