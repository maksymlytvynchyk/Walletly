<script setup>
import { computed, reactive, watch } from 'vue'

const props = defineProps({
  cards: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['submit'])

const form = reactive({
  from_card_id: '',
  to_card_id: '',
  amount: '',
  currency: 'uah',
})

// Card from which the transfer will be made
const fromCard = computed(() => {
  return props.cards.find(
    (card) => Number(card.id) === Number(form.from_card_id),
  )
})

// For the transfer, we show only cards with the same currency,
// but not the card from which the transfer will be made
const availableToCards = computed(() => {
  if (!fromCard.value) {
    return []
  }

  return props.cards.filter((card) => Number(card.id) !== Number(form.from_card_id))
})

// When the list of cards changes
// or the selection of the debit card changes
watch(
  [() => props.cards, () => form.from_card_id],
  () => {
    // If the debit card is not selected — we take the first one
    if (
      !props.cards.some(
        (card) => Number(card.id) === Number(form.from_card_id),
      )
    ) {
      form.from_card_id = props.cards[0]?.id || ''
    }

    // Automatically set the currency of the debit card
    const card = props.cards.find(
      (card) => Number(card.id) === Number(form.from_card_id),
    )

    if (card) {
      form.currency = card.currency
    }

    // If the current destination card is no longer valid,
    // select the first available one
    const destinationExists = availableToCards.value.some(
      (card) => Number(card.id) === Number(form.to_card_id),
    )

    if (!destinationExists) {
      form.to_card_id = availableToCards.value[0]?.id || ''
    }
  },
  { immediate: true },
)

function submit() {
  if (!form.from_card_id || !form.to_card_id) {
    return
  }

  if (Number(form.from_card_id) === Number(form.to_card_id)) {
    return
  }

  if (!form.amount || Number(form.amount) <= 0) {
    return
  }

  emit('submit', {
    from_card_id: Number(form.from_card_id),
    to_card_id: Number(form.to_card_id),
    amount: Number(form.amount),
    currency: form.currency,
  })

  form.amount = ''
}
</script>

<template>
  <form
    class="card space-y-3"
    @submit.prevent="submit"
  >
    <h2 class="text-lg font-bold">
      {{ $t("transferForm.transferBetweenCards") }}
    </h2>

    <!-- Card from which the transfer will be made -->
    <label>
      {{ $t("transferForm.fromCard") }}

      <select
        v-model="form.from_card_id"
        required
        :disabled="!cards.length"
      >
        <option value="" disabled>
          {{ $t("transferForm.selectCard") }}
        </option>

        <option
          v-for="card in cards"
          :key="card.id"
          :value="card.id"
        >
          {{ card.payment_system.toUpperCase() }}
          •••• {{ card.card_number.slice(-4) }}
          —
          {{ card.balance }}
          {{ card.currency.toUpperCase() }}
        </option>
      </select>
    </label>

    <!-- Card to which the transfer will be made -->
    <label>
      {{ $t("transferForm.toCard") }}

      <select
        v-model="form.to_card_id"
        required
        :disabled="!cards.length"
      >
        <option value="" disabled>
          {{ $t("transferForm.selectCard") }}
        </option>

        <option
          v-for="card in availableToCards"
          :key="card.id"
          :value="card.id"
        >
          {{ card.payment_system.toUpperCase() }}
          •••• {{ card.card_number.slice(-4) }}
          —
          {{ card.balance }}
          {{ card.currency.toUpperCase() }}
        </option>
      </select>
    </label>

    <!-- Amount -->
    <label>
      {{ $t("transferForm.sum") }}

      <input
        v-model="form.amount"
        type="number"
        min="0.01"
        step="0.01"
        required
      />
    </label>

    <!-- Currency is determined automatically -->
    <label>
      {{ $t("transferForm.currency") }}

      <select
        v-model="form.currency"
        disabled
      >
        <option value="uah">UAH</option>
        <option value="usd">USD</option>
        <option value="eur">EUR</option>
      </select>
    </label>

    <button
      class="btn btn-primary w-full"
      type="submit"
      :disabled="
        !cards.length ||
        !fromCard ||
        !availableToCards.length
      "
    >
      {{ $t("transferForm.transfer") }}
    </button>
  </form>
</template>
