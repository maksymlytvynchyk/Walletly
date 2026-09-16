<script setup>
import { onMounted } from 'vue'
import { ref } from 'vue'

import AppHeader from './components/AppHeader.vue'
import AuthPanel from './components/AuthPanel.vue'
import DashboardTop from './components/DashboardTop.vue'
import OperationsTable from './components/OperationsTable.vue'
import OperationForm from './components/OperationForm.vue'
import TransferForm from './components/TransferForm.vue'
import CardForm from './components/CardForm.vue'
import CardList from './components/CardList.vue'

import { useFinance } from './composables/useFinance'

const finance = useFinance()

const cardFieldErrors = ref({})


onMounted(() => {
  finance.restoreSession()
})
</script>

<template>
  <AppHeader
    :authenticated="finance.authenticated.value"
    :login="finance.user.value?.phone"
    @logout="finance.logout"
  />

  <main class="mx-auto max-w-6xl px-4 py-10 sm:px-6">
    <LanguageSwitcher
      v-if="!finance.authenticated.value"
      class="mb-4 ml-auto block w-fit"
    />
    <!-- Повідомлення -->
    <p
      v-if="finance.notice.value || finance.error.value"
      :class="
        finance.error.value
          ? 'bg-red-50 text-red-700'
          : 'bg-brand-50 text-brand-700'
      "
      class="mb-6 rounded-lg px-4 py-3 text-sm font-medium"
    >
      {{ finance.error.value || finance.notice.value }}
    </p>

    <!-- Початкове завантаження -->
    <div
      v-if="finance.initializing.value"
      class="py-20 text-center"
    >
      Завантаження...
    </div>

    <!-- Авторизація -->
    <AuthPanel
      v-else-if="!finance.authenticated.value"
      :loading="finance.loading.value"
      :register="finance.register"
      :sign-in="finance.signIn"
    />

    <!-- Dashboard -->
    <template v-else>

      <!-- Верхня частина dashboard -->
      <DashboardTop
        :loading="finance.loading.value"
        :balances="finance.balances.value"
        @refresh="finance.loadDashboard"
      />

      <!-- Список карток -->
      <CardList
        :cards="finance.cards.value"
      />

      <!-- Форми -->
      <div class="grid gap-6 lg:grid-cols-3">

        <!-- Створення картки -->
        <CardForm
          :submit-action="finance.createCard"
        />

        <!-- Створення операції -->
        <OperationForm
          :field-errors="cardFieldErrors"
          :cards="finance.cards.value"
          :submit-action="finance.createOperation"
        />

        <!-- Переказ -->
        <TransferForm
          :field-errors="cardFieldErrors"
          :cards="finance.cards.value"
          :submit-action="finance.transfer"
        />

      </div>

      <!-- Історія операцій -->
      <OperationsTable
        :operations="finance.operations.value"
        :cards="finance.cards.value"
      />

    </template>

  </main>
</template>