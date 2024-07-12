<template>
  <TelegramCont
    title="Telegram Integration Configuration"
    subtitle="Support Send Telegram Message with Telegram Bot API"
    addBtnTxt="Save"
    testBtnTxt="Test Send Telegram"
    :formList="formList"
    :formListDetails="tgDetails"
    @submit:add="saveTelegram"
    @test:connection="testTelegram"
  />
</template>

<script>
import { defineComponent } from "vue";
import TelegramCont from "src/components/SettingsAddCont.vue";
import { getSettings, saveSettings, testSettings } from "src/api/settings";

export default defineComponent({
  name: "SettingTelegramPage",
  components: {
    TelegramCont,
  },
  data() {
    return {
      formList: [
        {
          label: "Bot Token",
          model: "bot_token",
          type: "text",
          hint: "Hint: 1234567:abcdefghijk1234567890abcdefghijk",
        },
        {
          label: "Chat ID",
          model: "chat_id",
          type: "text",
          hint: "Hint: 1234567890",
        },
        {
          label: "Parse Mode (Markdown)",
          model: "parse",
          type: "checkbox",
          value: [true, false],
        },
      ],
      tgDetails: {
        bot_token: null,
        chat_id: null,
        parse: true,
      },
    };
  },
  methods: {
    async testTelegram() {
      this.$q.loading.show();
      await testSettings("telegram", this.tgDetails)
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
            message: this.$t("notify.testSent", { platform: "Telegram" }),
            type: "positive",
          });
        })
        .finally(() => {
          this.$q.loading.hide();
        });
    },
    async saveTelegram() {
      this.$q.loading.show();
      await saveSettings("telegram", this.tgDetails)
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
    async getTelegram() {
      this.$q.loading.show();
      await getSettings("telegram")
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
          this.tgDetails = res.data;
          this.tgDetails.parse = res.data.parse ? true : false;
        })
        .finally(() => {
          this.$q.loading.hide();
        });
    },
  },
  created() {
    this.getTelegram();
  },
});
</script>
