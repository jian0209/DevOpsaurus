<template>
  <SettingsAddCont
    title="Add Nodes Information"
    addBtnTxt="Add Nodes Information"
    :formList="formList"
    :formListDetails="nodesDetails"
    @submit:add="add"
  />
</template>

<script>
import { defineComponent } from "vue";
import SettingsAddCont from "src/components/SettingsAddCont.vue";
import { CRYPTO_CURRENCY_GROUP } from "src/utils/constants.js";
import "src/css/settingsScreen.scss";

export default defineComponent({
  name: "NodesAddPage",
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
          label: "Group Name",
          model: "groupName",
          type: "select",
          option: CRYPTO_CURRENCY_GROUP,
        },
        {
          label: "Get URL",
          model: "getUrl",
          type: "text",
        },
        {
          label: "Target URL",
          model: "targetUrl",
          type: "text",
        },
        // {
        //   label: "SSH Key",
        //   model: "sshKey",
        //   type: "textarea",
        // },
      ],
      nodesDetails: {
        name: null,
        groupName: null,
        url: null,
        // sshKey: null,
      },
    };
  },
  methods: {
    add() {
      this.$q.notify({
        message: `Added ${this.nodesDetails.name} successfully!`,
        type: "positive",
      });
      this.$router.push("/settings/nodes");
    },
  },
});
</script>
