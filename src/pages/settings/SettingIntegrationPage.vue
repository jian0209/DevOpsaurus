<template>
  <TelegramCont
    title="Integration Configuration"
    subtitle="Support SMTP Mail and Telegram Message"
    addBtnTxt="Save"
    :formList="formList"
    :formListDetails="integrationDetails"
    @submit:add="saveIntegration"
  />
</template>

<script>
import { defineComponent } from "vue";
import TelegramCont from "src/components/SettingsAddCont.vue";

export default defineComponent({
  name: "SettingIntegrationPage",
  components: {
    TelegramCont,
  },
  data() {
    return {
      formList: [
        {
          label: "Email",
          model: "email",
          type: "checkbox",
          value: ["true", "false"],
        },
        {
          label: "Telegram",
          model: "telegram",
          type: "checkbox",
          value: ["true", "false"],
        },
      ],
      integrationDetails: {
        email: false,
        telegram: false,
      },
    };
  },
  methods: {
    saveTelegram() {
      console.log(this.integrationDetails);
    },
  },
});
</script>
