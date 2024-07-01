<template>
  <q-dialog v-model="$props.dialogStatus" backdrop-filter="brightness(60%)">
    <q-card class="form-dialog-card">
      <q-toolbar class="form-dialog-card-title">
        <q-toolbar-title>
          <span class="text-weight-bold">{{ $props.title }}</span>
        </q-toolbar-title>
      </q-toolbar>
      <q-card-section>
        <q-form
          @submit="submitEdit"
          class="form-main-cont"
          v-if="$props.isFormDialog"
        >
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
            <UsualButton label="Save" type="submit" color="info" />
            <div style="width: 20px" />
            <UsualButton
              label="Cancel"
              @action:click="closeDialog"
              color="info"
            />
          </div>
        </q-form>
        <div v-else class="form-dialog-card">
          <q-toolbar class="usual-dialog-card">
            {{ $props.subtitle }}
          </q-toolbar>
          <div class="add-btn-cont">
            <UsualButton
              v-if="$props.testBtnTxt"
              :label="$props.testBtnTxt"
              color="positive"
              @action:click="testConnection"
            />
            <div v-if="$props.testBtnTxt" style="width: 20px" />
            <UsualButton label="Save" @action:click="submitEdit" color="info" />
            <div style="width: 20px" />
            <UsualButton
              label="Cancel"
              @action:click="closeDialog"
              color="info"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script>
import { defineComponent, ref, watch } from "vue";
import UsualButton from "src/components/Button.vue";
import "src/css/component.scss";

export default defineComponent({
  name: "DialogComponent",
  components: {
    UsualButton,
  },
  props: {
    dialogStatus: Boolean,
    formList: Array,
    formListDetails: Object,
    testBtnTxt: String,
    title: String,
    subtitle: String,
    isFormDialog: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    submitEdit() {
      this.closeDialog();
      this.$emit("submit:edit");
    },
    testConnection() {
      this.$emit("test:connection");
    },
  },
  setup(props, { emit }) {
    const localDialogStatus = ref(props.dialogStatus);

    watch(
      () => props.dialogStatus,
      (newValue) => {
        localDialogStatus.value = newValue;
      }
    );

    const closeDialog = () => {
      localDialogStatus.value = false;
      emit("update:dialogStatus", false);
    };

    return {
      localDialogStatus,
      closeDialog,
    };
  },
});
</script>
