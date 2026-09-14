<script setup>
import { money } from '../api'

const props = defineProps({
  operations: {
    type: Array,
    default: () => [],
  },

  cards: {
    type: Array,
    default: () => [],
  },
})

function label(type) {
  if (type === 'income') {
    return 'Дохід'
  }

  if (type === 'expense') {
    return 'Витрата'
  }

  return 'Переказ'
}

function getCard(operation) {
  return props.cards.find(
    (card) => Number(card.id) === Number(operation.card_id),
  )
}

function cardLabel(operation) {
  const card = getCard(operation)

  if (!card) {
    return `#${operation.card_id}`
  }

  return `${card.payment_system.toUpperCase()} •••• ${card.card_number.slice(-4)}`
}
</script>

<template>
  <section class="card mt-6 overflow-hidden p-0">
    <div class="p-5">
      <h2 class="text-lg font-bold">
        {{ $t("operationTable.lastOperations") }}
      </h2>
    </div>

    <div class="overflow-x-auto">
      <table class="w-full min-w-160 text-left text-sm">
        <thead class="bg-slate-50 text-slate-500">
          <tr>
            <th class="px-5 py-3 font-semibold">
              {{ $t("operationTable.date") }}
            </th>

            <th class="px-5 py-3 font-semibold">
              {{ $t("operationTable.type") }}
            </th>

            <th class="px-5 py-3 font-semibold">
              {{ $t("operationTable.card") }}
            </th>

            <th class="px-5 py-3 font-semibold">
              {{ $t("operationTable.category") }}
            </th>

            <th class="px-5 py-3 text-right font-semibold">
              {{ $t("operationTable.sum") }}
            </th>
          </tr>
        </thead>

        <tbody>
          <tr v-if="!operations.length">
            <td
              colspan="5"
              class="px-5 py-7 text-center text-slate-500"
            >
              {{ $t("operationTable.operationsDontExists") }}
            </td>
          </tr>

          <tr
            v-for="operation in operations"
            :key="operation.id"
            class="border-t border-slate-100"
          >
            <td class="px-5 py-3">
              {{ new Date(operation.created_at).toLocaleString('uk-UA') }}
            </td>

            <td
              class="px-5 py-3"
              :class="
                operation.type === 'income'
                  ? 'text-brand-700'
                  : operation.type === 'expense'
                    ? 'text-red-600'
                    : 'text-slate-600'
              "
            >
              {{ label(operation.type) }}
            </td>

            <td class="px-5 py-3">
              {{ cardLabel(operation) }}
            </td>

            <td class="px-5 py-3">
              <span v-if="operation.category">
                {{ operation.category }}

                <span v-if="operation.subcategory">
                  / {{ operation.subcategory }}
                </span>
              </span>

              <span v-else>
                —
              </span>
            </td>

            <td
              class="px-5 py-3 text-right font-semibold"
              :class="
                operation.type === 'expense'
                  ? 'text-red-600'
                  : operation.type === 'income'
                    ? 'text-brand-700'
                    : 'text-slate-600'
              "
            >
              <template v-if="operation.type === 'expense'">
                −
              </template>

              <template v-else-if="operation.type === 'income'">
                +
              </template>

              <template v-else>
                ↔
              </template>

              {{ money(operation.amount, operation.currency) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>