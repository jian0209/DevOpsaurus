<template>
  <q-btn
    :label="label"
    :color="color"
    :icon="icon"
    :loading="loading"
    :disable="disable"
    @click="handleClick"
    :outline="outline"
    :style="style"
    :type="type"
  >
    <!-- <slot></slot> -->
  </q-btn>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "UsualButton",
  props: {
    label: {
      type: String,
      default: "",
    },
    color: {
      type: String,
      default: "primary",
    },
    icon: String,
    style: Object,
    loading: {
      type: Boolean,
      default: false,
    },
    disable: {
      type: Boolean,
      default: false,
    },
    outline: {
      type: Boolean,
      default: false,
    },
    type: {
      type: String,
      default: "button",
    },
  },
  methods: {
    handleClick() {
      this.$emit("action:click");
    },
  },
});
</script>
