<template>
  <SettingsAddCont
    title="Add Command Information"
    addBtnTxt="Add Command Information"
    testBtnTxt="Test SSH Connection"
    :formList="formList"
    :formListDetails="commandDetails"
    @submit:add="add"
  />
</template>

<script>
import { defineComponent } from "vue";
import SettingsAddCont from "src/components/SettingsAddCont.vue";
import "src/css/settingsScreen.scss";

export default defineComponent({
  name: "CommandAddPage",
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
          model: "sshKey",
          type: "textarea",
        },
        {
          label: "SSH Port",
          model: "sshPort",
          type: "text",
        },
        {
          label: "Command",
          model: "command",
          type: "text",
        },
      ],
      commandDetails: {
        name: null,
        host: null,
        username: null,
        sshKey: null,
        sshPort: null,
        command: null,
      },
    };
  },
  methods: {
    add() {
      this.$router.push("/settings/command");
    },
  },
});
</script>
