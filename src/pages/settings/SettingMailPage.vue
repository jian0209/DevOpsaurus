<template>
  <MailCont
    title="Mail Server Configuration"
    subtitle="Support SMTP server with STARTTLS, and SSL/TLS"
    addBtnTxt="Save"
    testBtnTxt="Test Send Email"
    :formList="formList"
    :formListDetails="upsDetails"
    @submit:add="saveEmail"
    @test:connection="testEmail"
  />
</template>

<script>
import { defineComponent } from "vue";
import MailCont from "src/components/SettingsAddCont.vue";

export default defineComponent({
  name: "SettingMailPage",
  components: {
    MailCont,
  },
  props: {},
  methods: {},
  data() {
    return {
      formList: [
        {
          label: "SMTP Server",
          model: "smtpServer",
          type: "text",
        },
        {
          label: "SMTP Port",
          model: "smtpPort",
          type: "text",
        },
        {
          label: "SMTP HELO Domain",
          model: "smtpHeloDomain",
          type: "text",
        },
        {
          label: "SMTP Username",
          model: "smtpUsername",
          type: "text",
        },
        {
          label: "SMTP Password",
          model: "smtpPassword",
          type: "password",
        },
        {
          label: "Emission Email Address",
          model: "emitEmailAddr",
          type: "text",
        },
        {
          label: "Allow SSL/TLS",
          model: "allowSslTls",
          type: "checkbox",
          value: ["true", "false"],
        },
        {
          label: "Allow STARTTLS",
          model: "allowStartTls",
          type: "checkbox",
          value: ["true", "false"],
        },
      ],
      upsDetails: {
        smtpServer: null,
        smtpPort: null,
        smtpUsername: null,
        smtpPassword: null,
        emitEmailAddr: null,
        allowSslTls: false,
        allowStartTls: false,
      },
    };
  },
  methods: {
    saveEmail() {
      console.log(this.upsDetails);
      this.$q.notify({
        message: `Configuration Saved!`,
        type: "positive",
      });
    },
    testEmail() {
      console.log(this.upsDetails);
      this.$q.notify({
        message: `Email Sent!`,
        type: "positive",
      });
    },
  },
});
</script>
