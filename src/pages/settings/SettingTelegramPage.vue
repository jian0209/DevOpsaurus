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
          hint: "Hint: 1234567:abcdefghijk1234567890abcdefghijk",
        },
        {
          label: "Chat ID",
          model: "chatId",
          type: "text",
          hint: "Hint: 1234567890",
        },
        {
          label: "Parse Mode (Markdown)",
          model: "markdown",
          type: "checkbox",
          value: ["true", "false"],
        },
      ],
      tgDetails: {
        botToken: null,
        chatId: null,
        markdown: true,
      },
    };
  },
  methods: {
    saveTelegram() {
      console.log(this.tgDetails);
      this.$q.notify({
        message: `Configuration Saved!`,
        type: "positive",
      });
    },
    testTelegram() {
      console.log(this.tgDetails);
      this.$q.notify({
        message: `Telegram Message Sent!`,
        type: "positive",
      });
    },
  },
});
</script>
