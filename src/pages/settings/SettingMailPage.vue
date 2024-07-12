<template>
  <MailCont
    title="Mail Server Configuration"
    subtitle="Support SMTP server with STARTTLS, and SSL/TLS"
    addBtnTxt="Save"
    testBtnTxt="Test Send Email"
    :formList="formList"
    :formListDetails="mailDetails"
    @submit:add="saveEmail"
    @test:connection="testEmail"
  />
</template>

<script>
import { defineComponent } from "vue";
import MailCont from "src/components/SettingsAddCont.vue";
import { getSettings, saveSettings, testSettings } from "src/api/settings";

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
          model: "smtp_server",
          type: "text",
        },
        {
          label: "SMTP Port",
          model: "smtp_port",
          type: "text",
        },
        {
          label: "SMTP HELO Domain",
          model: "email_helo",
          type: "text",
        },
        {
          label: "SMTP Username",
          model: "smtp_username",
          type: "text",
        },
        {
          label: "SMTP Password",
          model: "smtp_password",
          type: "password",
        },
        {
          label: "Emission Email Address",
          model: "email_from",
          type: "text",
        },
        {
          label: "Allow SSL/TLS",
          model: "email_allow_ssl_tls",
          type: "checkbox",
          value: [true, false],
        },
        {
          label: "Allow STARTTLS",
          model: "email_allow_start_tls",
          type: "checkbox",
          value: [true, false],
        },
        {
          label: "Test Send Email",
          model: "email_to",
          type: "text",
        },
      ],
      mailDetails: {
        smtp_server: null,
        smtp_port: null,
        smtp_username: null,
        smtp_password: null,
        email_helo: null,
        email_from: null,
        email_to: null,
        email_allow_ssl_tls: false,
        email_allow_start_tls: false,
      },
    };
  },
  methods: {
    async testEmail() {
      this.$q.loading.show();
      await testSettings("email", this.mailDetails)
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
            message: this.$t("notify.testSent", { platform: "Email" }),
            type: "positive",
          });
        })
        .finally(() => {
          this.$q.loading.hide();
        });
    },
    async saveEmail() {
      this.$q.loading.show();
      await saveSettings("email", this.mailDetails)
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
    async getEmail() {
      this.$q.loading.show();
      await getSettings("email")
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
          this.mailDetails = res.data;
          this.mailDetails.email_allow_ssl_tls = res.data.email_allow_ssl_tls
            ? true
            : false;
          this.mailDetails.email_allow_start_tls = res.data
            .email_allow_start_tls
            ? true
            : false;
        })
        .finally(() => {
          this.$q.loading.hide();
        });
    },
  },
  created() {
    this.getEmail();
  },
});
</script>
