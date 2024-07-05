<template>
  <TelegramCont
    title="Slack Integration Configuration"
    subtitle="Support Send Slack Message through Slack API"
    addBtnTxt="Save"
    testBtnTxt="Test Send Slack"
    :formList="formList"
    :formListDetails="slackDetails"
    @submit:add="saveSlack"
    @test:connection="testSlack"
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
          hint: "Hint: T03M53Y0AG1",
        },
        {
          label: "Channel",
          model: "channel",
          type: "text",
          hint: "Hint: B05V1AL593X",
        },
        {
          label: "Token",
          model: "token",
          type: "text",
          hint: "Hint: KZnxxO755gLJ0tWQUysxvdH5",
        },
      ],
      slackDetails: {
        bot_token: null,
        channel: null,
        markdown: true,
      },
    };
  },
  methods: {
    async testSlack() {
      this.$q.loading.show();
      await testSettings("slack", this.slackDetails)
        .then((res) => {
          if (res.code !== 0) {
            this.$q.notify({
              message: this.$t(`api.${res.code}`),
              type: "negative",
            });
            return;
          }
          this.$q.notify({
            message: this.$t("notify.testSent", { platform: "Slack" }),
            type: "positive",
          });
        })
        .finally(() => {
          this.$q.loading.hide();
        });
    },
    async saveSlack() {
      this.$q.loading.show();
      await saveSettings("slack", this.slackDetails)
        .then((res) => {
          if (res.code !== 0) {
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
    async getSlack() {
      this.$q.loading.show();
      await getSettings("slack")
        .then((res) => {
          if (res.code !== 0) {
            this.$q.notify({
              message: this.$t(`api.${res.code}`),
              type: "negative",
            });
            return;
          }
          this.slackDetails = res.data;
        })
        .finally(() => {
          this.$q.loading.hide();
        });
    },
  },
  created() {
    this.getSlack();
  },
});
</script>
