<script setup>
import { money } from '../api'

defineProps({
  cards: {
    type: Array,
    default: () => [],
  },
})

function formatCardNumber(cardNumber) {
  if (!cardNumber) {
    return ''
  }

  return cardNumber.replace(/(.{4})/g, '$1 ').trim()
}
</script>

<template>
  <section class="card mb-6">
    <div class="mb-4 flex items-center justify-between">
      <h2 class="text-lg font-bold">
        Картки
      </h2>

      <span
        class="rounded-full bg-brand-50 px-2.5 py-1 text-xs font-bold text-brand-700"
      >
        {{ cards.length }}
      </span>
    </div>

    <div
      v-if="cards.length"
      class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3"
    >
      <article
        v-for="card in cards"
        :key="card.id"
        class="rounded-xl border border-slate-200 p-4"
      >
        <div class="flex items-center justify-between">
          <p class="text-sm font-bold">
            {{ card.payment_system.toUpperCase() }}
          </p>

          <p class="text-xs text-slate-500">
            {{ card.card_type }}
          </p>
        </div>

        <p class="mt-4 font-mono text-lg font-bold tracking-wider">
          {{ formatCardNumber(card.card_number) }}
        </p>

        <p class="mt-2 text-xs text-slate-500">
          IBAN: {{ card.iban }}
        </p>

        <p class="mt-3 text-sm text-slate-500">
          {{ card.currency.toUpperCase() }}
        </p>

        <p class="mt-1 text-lg font-bold">
          {{ money(card.balance, card.currency) }}
        </p>

        <p class="mt-2 text-xs text-slate-500">
          Дійсна до: {{ card.expires_at }}
        </p>
      </article>
    </div>

    <p
      v-else
      class="text-sm text-slate-500"
    >
      Карток ще немає.
    </p>
  </section>
</template>