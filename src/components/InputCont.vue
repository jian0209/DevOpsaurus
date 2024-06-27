<template>
  <q-input
    :label="$props.label"
    :hint="$props.hint"
    :mask="$props.mask"
    :type="$props.type"
    :rules="$props.rules"
    :clearable="$props.clearable"
    :autofocus="$props.autofocus"
    :error-message="$props.errorMessage"
    :prefix="$props.prefix"
    :suffix="$props.suffix"
    :autogrow="$props.autogrow"
    label-color="indigo-1"
    bg-color="indigo-5"
    filled
    dense
    v-model="intervalValue"
    style="width: 100%"
  />
</template>

<script>
import { computed, defineComponent } from "vue";
import "src/css/component.scss";

export default defineComponent({
  name: "InputCont",
  props: {
    label: {
      type: String,
      default: "",
    },
    hint: {
      type: String,
      default: "",
    },
    mask: {
      type: String,
      default: "",
    },
    type: {
      type: String,
      default: "text",
    },
    rules: {
      type: Array,
      default: () => [],
    },
    clearable: {
      type: Boolean,
      default: false,
    },
    autofocus: {
      type: Boolean,
      default: false,
    },
    errorMessage: {
      type: String,
      default: "",
    },
    prefix: {
      type: String,
      default: "",
    },
    suffix: {
      type: String,
      default: "",
    },
    autogrow: {
      type: Boolean,
      default: false,
    },
    modelValue: {
      type: String,
      default: "",
      readonly: false,
    },
  },
  setup(props, { emit }) {
    const intervalValue = computed({
      get: () => props.modelValue,
      set: (val) => emit("update:modelValue", val),
    });
    return {
      intervalValue,
    };
  },
});
</script>
