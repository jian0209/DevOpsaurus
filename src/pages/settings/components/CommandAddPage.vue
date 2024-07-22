<template>
  <SettingsAddCont
    title="Add Command Information"
    addBtnTxt="Add Command Information"
    testBtnTxt="Test SSH Connection"
    :formList="formList"
    :formListDetails="commandDetails"
    @submit:add="add"
    @test:connection="testCommand"
  />
</template>

<script>
import { defineComponent } from "vue";
import SettingsAddCont from "src/components/SettingsAddCont.vue";
import "src/css/settingsScreen.scss";
import { addCommand, testCommand } from "src/api/settings";

export default defineComponent({
  name: "CommandAddPage",
  components: {
    SettingsAddCont,
  },
  created() {
    if (this.$route.query.isClone) {
      const decryptedText = atob(
        this.$CryptoJS.AES.decrypt(
          this.$route.query.passedData,
          process.env.ENCRYPT_KEY
        ).toString(this.$CryptoJS.enc.Utf8)
      );
      const passedData = JSON.parse(decryptedText);
      this.commandDetails.host = passedData.host;
      this.commandDetails.username = passedData.username;
      this.commandDetails.ssh_key = passedData.ssh_key;
      this.commandDetails.ssh_port = passedData.ssh_port;
    }
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
          label: "Host",
          model: "host",
          type: "text",
        },
        {
          label: "Username",
          model: "username",
          type: "text",
        },
        {
          label: "SSH Key",
          model: "ssh_key",
          type: "textarea",
        },
        {
          label: "SSH Port",
          model: "ssh_port",
          type: "text",
        },
        {
          label: "Command",
          model: "command",
          type: "textarea",
        },
      ],
      commandDetails: {
        name: null,
        host: null,
        username: null,
        ssh_key: null,
        ssh_port: null,
        command: null,
      },
    };
  },
  methods: {
    async add() {
      const data = this.commandDetails;
      this.$q.loading.show();
      await addCommand(data)
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
            message: `Added ${data.name} successfully!`,
            type: "positive",
          });
          this.$router.push("/settings/command");
        })
        .finally(() => this.$q.loading.hide());
    },
    async testCommand() {
      this.$q.loading.show();
      await testCommand(this.commandDetails)
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
            message: this.$t("notify.testSuccess", { platform: "SSH" }),
            type: "positive",
          });
        })
        .finally(() => this.$q.loading.hide());
    },
  },
});
</script>
