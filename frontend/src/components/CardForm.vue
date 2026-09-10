<script setup>
import { reactive } from 'vue'

const emit = defineEmits(['submit'])

const form = reactive({
  payment_system: 'visa',
  card_type: 'debit',
  currency: 'uah',
  initial_balance: 0,
})

function submit() {
  emit('submit', { ...form })

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
      Нова картка
    </h2>

    <label>
      Платіжна система

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
      Тип картки

      <select v-model="form.card_type">
        <option value="debit">
          Дебетова
        </option>

        <option value="credit">
          Кредитна
        </option>

        <option value="overdraft">
          Овердрафт
        </option>
      </select>
    </label>

    <label>
      Початковий баланс

      <input
        v-model.number="form.initial_balance"
        min="0"
        step="0.01"
        type="number"
        required
      />
    </label>

    <label>
      Валюта

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
      Створити картку
    </button>
  </form>
</template>