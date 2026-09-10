<script setup>
defineProps({ authenticated: Boolean, login: { type: String, default: '' } })
defineEmits(['logout'])
</script>
<template>
    <header class="border-b border-slate-200 bg-white">
        <div class="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6"><a href="/"
                class="text-xl font-black tracking-tight text-brand-700">Walletly</a>
            <div v-if="authenticated" class="flex items-center gap-3 text-sm text-slate-600"><span>{{ login
                    }}</span><button class="btn btn-secondary" @click="$emit('logout')">Вийти</button></div>
        </div>
    </header>
</template>
