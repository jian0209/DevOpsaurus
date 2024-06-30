<template>
  <SettingsAddCont
    title="Add UPS Information"
    addBtnTxt="Add UPS Information"
    testBtnTxt="Test Get Data"
    :formList="formList"
    :formListDetails="upsDetails"
    @submit:add="add"
  />
</template>

<script>
import { defineComponent } from "vue";
import SettingsAddCont from "src/components/SettingsAddCont.vue";
import "src/css/settingsScreen.scss";

export default defineComponent({
  name: "UpsAddPage",
  components: {
    SettingsAddCont,
  },
  data() {
    return {
      formList: [
        {
          label: "Name",
          model: "name",
          type: "text",
        },
        {
          label: "IP Address",
          model: "ipAddr",
          type: "text",
        },
        {
          label: "Port",
          model: "port",
          type: "text",
        },
        {
          label: "Location",
          model: "location",
          type: "text",
        },
        {
          label: "Parameter (JSON)",
          model: "parameter",
          type: "textarea",
          placeholder:
            'e.g. {"key": string, "key": int, "key": bool, "key": {"key": string}}',
        },
      ],
      upsDetails: {
        name: null,
        ipAddr: null,
        port: null,
        location: null,
        parameter: null,
      },
    };
  },
  methods: {
    add() {
      this.$router.push("/settings/ups");
    },
  },
});
</script>
