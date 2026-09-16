<script setup>
import { reactive, ref } from 'vue'

const props = defineProps({
  submitAction: {
    type: Function,
    required: true,
  }
})

const fieldErrors = ref({})

const emit = defineEmits(['submit'])

const form = reactive({
  payment_system: 'visa',
  card_type: 'debit',
  currency: 'uah',
  initial_balance: 0,
})

async function submit() {
  fieldErrors.value = {}

  const result = await props.submitAction({ ...form })

  fieldErrors.value = result.fieldErrors

  if (!result.success) {
    return
  }

  Object.assign(form, {
    payment_system: 'visa',
    card_type: 'debit',
    currency: 'uah',
    initial_balance: 0,
  })
}
</script>

<template>
  <form class="card space-y-3" @submit.prevent="submit">
    <h2 class="text-lg font-bold">
      {{ $t("cardForm.newCard") }}
    </h2>

    <label>
      {{ $t("cardForm.paymentSystem") }}

      <select v-model="form.payment_system">
        <option value="visa">
          Visa
        </option>

        <option value="mastercard">
          Mastercard
        </option>
      </select>
    </label>

    <label>
      {{ $t("cardForm.cardType") }}

      <select v-model="form.card_type">
        <option value="debit">
          {{ $t("cardForm.debit") }}
        </option>

        <option value="credit">
          {{ $t("cardForm.credit") }}
        </option>

        <option value="overdraft">
          {{ $t("cardForm.overdraft") }}
        </option>
      </select>
    </label>

    <label>
      {{ $t("cardForm.initialBalance") }}

      <input v-model.number="form.initial_balance" min="0" step="0.01" type="number" required />
      <p v-if="fieldErrors.initial_balance" class="mt-1 text-sm text-red-600">
        {{ $t(`errors.${fieldErrors.initial_balance}`) }}
      </p>
    </label>

    <label>
      {{ $t("cardForm.currency") }}

      <select v-model="form.currency">
        <option value="uah">
          UAH
        </option>

        <option value="usd">
          USD
        </option>

        <option value="eur">
          EUR
        </option>
      </select>
    </label>

    <button class="btn btn-primary w-full">
      {{ $t("cardForm.createCard") }}
    </button>
  </form>
</template>