<template>
  <div class="page-title-cont">
    <div class="page-title">{{ $props.title }}</div>
    <div class="page-subtitle">{{ $props.subtitle }}</div>
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "TitleContainer",
  props: {
    title: String,
    subtitle: String,
  },
});
</script>
