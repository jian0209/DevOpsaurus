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
          model: "botToken",
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
        botToken: null,
        chatId: null,
        markdown: true,
      },
    };
  },
  methods: {
    saveSlack() {
      console.log(this.slackDetails);
      this.$q.notify({
        message: `Configuration Saved!`,
        type: "positive",
      });
    },
    testSlack() {
      console.log(this.slackDetails);
      this.$q.notify({
        message: `Slack Message Sent!`,
        type: "positive",
      });
    },
  },
});
</script>
