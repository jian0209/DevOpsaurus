<template>
  <div>
    <TitleContainer :title="$props.title" />
    <q-form @submit="submitAdd" class="form-main-cont">
      <div
        class="form-input-cont"
        v-for="(item, index) in $props.formList"
        :key="index"
      >
        <div class="form-input-name">{{ item.label }}</div>
        <q-input
          v-if="
            item.type === 'text' ||
            item.type === 'password' ||
            item.type === 'email' ||
            item.type === 'textarea'
          "
          v-model="$props.formListDetails[item.model]"
          :type="item.type"
          class="usual-form-input"
          color="secondary"
          :placeholder="item.placeholder"
          dense
          outlined
        />
        <q-select
          v-if="item.type === 'select'"
          class="usual-form-input"
          v-model="$props.formListDetails[item.model]"
          :options="item.option"
          color="secondary"
          outlined
          dense
        />
        <div v-if="item.type === 'radio'" class="usual-form-input">
          <q-radio
            v-for="(radioItem, index) in item.radioOption"
            :key="index"
            v-model="$props.formListDetails[item.model]"
            :val="radioItem.value"
            :label="radioItem.label"
            color="secondary"
          />
        </div>
      </div>
      <div class="add-btn-cont">
        <UsualButton
          v-if="$props.testBtnTxt"
          :label="$props.testBtnTxt"
          color="positive"
          @action:click="testConnection"
        />
        <div v-if="$props.testBtnTxt" style="width: 20px" />
        <UsualButton :label="$props.addBtnTxt" type="submit" color="info" />
      </div>
    </q-form>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import TitleContainer from "src/components/TitleCont.vue";
import UsualButton from "src/components/Button.vue";
import "src/css/component.scss";

export default defineComponent({
  name: "SettingsAddCont",
  props: {
    title: {
      type: String,
      required: true,
    },
    addBtnTxt: {
      type: String,
      required: true,
    },
    testBtnTxt: {
      type: String,
      default: null,
    },
    formList: {
      type: Array,
      required: true,
    },
    formListDetails: {
      type: Object,
      required: true,
    },
  },
  components: {
    TitleContainer,
    UsualButton,
  },
  methods: {
    submitAdd() {
      this.$emit("submit:add", this.formListDetails);
    },
    testConnection() {
      this.$emit("test:connection", this.formListDetails);
    },
  },
});
</script>
