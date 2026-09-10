<script setup>
import { money } from '../api'

defineProps({
  loading: Boolean,

  balances: {
    type: Object,
    default: () => ({
      UAH: 0,
      USD: 0,
      EUR: 0,
    }),
  },
})

defineEmits(['refresh'])
</script>

<template>
  <div class="mb-7 flex items-end justify-between">
    <div>
      <p class="text-xs font-bold tracking-[0.18em] text-brand-700">
        ОГЛЯД
      </p>

      <h1 class="mt-1 text-3xl font-bold tracking-tight">
        Мої фінанси
      </h1>
    </div>

    <button
      class="btn btn-secondary"
      :disabled="loading"
      @click="$emit('refresh')"
    >
      Оновити
    </button>
  </div>

  <section
    class="mb-6 rounded-2xl bg-linear-to-br from-brand-700 to-brand-500 p-7 text-white shadow-lg shadow-brand-700/15"
  >
    <p class="text-sm text-brand-50">
      Баланс
    </p>

    <div class="mt-4 grid gap-4 sm:grid-cols-3">
      <!-- UAH -->
      <div>
        <p class="text-sm text-brand-100">
          UAH
        </p>

        <p class="mt-1 text-2xl font-bold">
          {{ money(balances.UAH, 'uah') }}
        </p>
      </div>

      <!-- USD -->
      <div>
        <p class="text-sm text-brand-100">
          USD
        </p>

        <p class="mt-1 text-2xl font-bold">
          {{ money(balances.USD, 'usd') }}
        </p>
      </div>

      <!-- EUR -->
      <div>
        <p class="text-sm text-brand-100">
          EUR
        </p>

        <p class="mt-1 text-2xl font-bold">
          {{ money(balances.EUR, 'eur') }}
        </p>
      </div>
    </div>
  </section>
</template>