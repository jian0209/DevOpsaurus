<template>
  <TelegramCont
    title="Integration Configuration"
    subtitle="Support SMTP Mail, Telegram Message and Slack Message"
    addBtnTxt="Save"
    :formList="formList"
    :formListDetails="integrationDetails"
    @submit:add="saveIntegration"
  />
</template>

<script>
import { defineComponent } from "vue";
import TelegramCont from "src/components/SettingsAddCont.vue";
import { getSettings, saveSettings } from "src/api/settings";

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
          value: [true, false],
        },
        {
          label: "Telegram",
          model: "telegram",
          type: "checkbox",
          value: [true, false],
        },
        {
          label: "Slack",
          model: "slack",
          type: "checkbox",
          value: [true, false],
        },
      ],
      integrationDetails: {
        email: false,
        telegram: false,
        slack: false,
      },
    };
  },
  methods: {
    async saveIntegration() {
      this.$q.loading.show();
      await saveSettings("integration", this.integrationDetails)
        .then((res) => {
          if (res.code !== 0) {
            if (res.code === 9001) {
              this.$q.notify({
                message: `${res.data.msg || "Unknown Error"}`,
                type: "negative",
              });
              return;
            }
            this.$q.notify({
              message: this.$t(`api.${res.code}`),
              type: "negative",
            });
            return;
          }
          this.$q.notify({
            message: this.$t("notify.configurationSaved"),
            type: "positive",
          });
        })
        .finally(() => {
          this.$q.loading.hide();
        });
    },
    async getIntegration() {
      this.$q.loading.show();
      await getSettings("integration")
        .then((res) => {
          if (res.code !== 0) {
            if (res.code === 9001) {
              this.$q.notify({
                message: `${res.data.msg || "Unknown Error"}`,
                type: "negative",
              });
              return;
            }
            this.$q.notify({
              message: this.$t(`api.${res.code}`),
              type: "negative",
            });
            return;
          }
          this.integrationDetails.email = res.data.email ? true : false;
          this.integrationDetails.telegram = res.data.telegram ? true : false;
          this.integrationDetails.slack = res.data.slack ? true : false;
        })
        .finally(() => {
          this.$q.loading.hide();
        });
    },
  },
  created() {
    this.getIntegration();
  },
});
</script>
