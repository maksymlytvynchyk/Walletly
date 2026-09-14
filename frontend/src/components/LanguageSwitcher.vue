<script setup>
import { useI18n } from "vue-i18n";
import 'flag-icons/css/flag-icons.min.css'

const { locale } = useI18n();

function changeLanguage(event) {
  const selectedLocale = event.target.value;
  console.log(selectedLocale)

  locale.value = selectedLocale;
  localStorage.setItem("locale", selectedLocale);
}
console.log(locale.value)
</script>

<template>
  <label>
    <span class="sr-only">{{ $t("language") }}</span>
    <select :value="locale" aria-label="Language" id="Language" @change="changeLanguage">
      <option value="uk">
        Українська
      </option>
      <option value="en">
        English
      </option>
    </select>
  </label>
</template>

<style scoped>
.fi {
  font-size: 1.2rem;
  border-radius: 2px;
  margin-right: 8px;
}
</style>