<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  cards: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['submit'])

const form = reactive({
  type: 'income',
  card_id: '',
  amount: '',
  currency: 'uah',
  category: '',
  subcategory: '',
})

watch(
  () => props.cards,
  (cards) => {
    const selectedCard = cards.find(
      (card) => Number(card.id) === Number(form.card_id),
    )

    if (!selectedCard) {
      form.card_id = cards[0]?.id || ''
    }

    const currentCard = cards.find(
      (card) => Number(card.id) === Number(form.card_id),
    )

    if (currentCard) {
      form.currency = currentCard.currency
    }
  },
  { immediate: true },
)

watch(
  () => form.card_id,
  (cardId) => {
    const card = props.cards.find(
      (card) => Number(card.id) === Number(cardId),
    )

    if (card) {
      form.currency = card.currency
    }
  },
)

function submit() {
  emit('submit', {
    ...form,
    card_id: Number(form.card_id),
    amount: Number(form.amount),
    category: form.category || null,
    subcategory: form.subcategory || null,
  })

  Object.assign(form, {
    type: 'income',
    card_id: props.cards[0]?.id || '',
    amount: '',
    currency: props.cards[0]?.currency || 'uah',
    category: '',
    subcategory: '',
  })
}
</script>

<template>
  <form
    class="card space-y-3"
    @submit.prevent="submit"
  >
    <h2 class="text-lg font-bold">
      {{ $t("operationForm.newOperation") }}
    </h2>

    <!-- Тип операції -->
    <label>
      {{ $t("operationForm.type") }}

      <select v-model="form.type">
        <option value="income">
          {{ $t("operationForm.income") }}
        </option>

        <option value="expense">
          {{ $t("operationForm.expense") }}
        </option>
      </select>
    </label>

    <!-- Картка -->
    <label>
      {{ $t("operationForm.card") }}

      <select
        v-model="form.card_id"
        required
        :disabled="!cards.length"
      >
        <option
          v-for="card in cards"
          :key="card.id"
          :value="card.id"
        >
          {{ card.payment_system.toUpperCase() }}
          •••• {{ card.card_number.slice(-4) }}
          — {{ card.balance }} {{ card.currency.toUpperCase() }}
        </option>
      </select>
    </label>

    <!-- Сума -->
    <label>
      {{ $t("operationForm.sum") }}

      <input
        v-model="form.amount"
        min="0.01"
        step="0.01"
        type="number"
        required
      />
    </label>

    <!-- Валюта -->
    <label>
      {{ $t("operationForm.currency") }}

      <select
        v-model="form.currency"
        disabled
      >
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

    <!-- Категорія -->
    <label>
      {{ $t("operationForm.category") }}

      <input
        v-model="form.category"
        maxlength="127"
        :placeholder="$t('operationForm.categoryPlaceholder')"
      />
    </label>

    <!-- Підкатегорія -->
    <label>
      {{ $t("operationForm.subcategory") }}

      <input
        v-model="form.subcategory"
        maxlength="127"
        :placeholder="$t('operationForm.subcategoryPlaceholder')"
      />
    </label>

    <button
      class="btn btn-primary w-full"
      :disabled="!cards.length"
    >
      {{ $t("operationForm.add") }}
    </button>
  </form>
</template>