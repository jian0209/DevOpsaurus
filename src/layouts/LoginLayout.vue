<template>
  <q-layout view="lHh Lpr lFf" class="main-background global-css">
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "LoginLayout",
});
</script>
