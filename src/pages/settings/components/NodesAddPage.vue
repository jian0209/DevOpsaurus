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
import { addNode } from "src/api/settings.js";
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
          model: "group_name",
          type: "select",
          option: CRYPTO_CURRENCY_GROUP,
        },
        {
          label: "Group URL",
          model: "group_url",
          type: "text",
        },
        {
          label: "Target URL",
          model: "target_url",
          type: "text",
        },
        {
          label: "Fetch Parameter",
          model: "fetch_parameter",
          type: "text",
          placeholder: ".data.check_results.*",
          hint: '* Use . to select the key of the JSON data, eg: .data.check_results.* the example will fetch "{data:{check_result:*}}"',
        },
      ],
      nodesDetails: {
        name: null,
        group_name: null,
        group_url: null,
        target_url: null,
        fetch_parameter: null,
      },
    };
  },
  methods: {
    async add() {
      const data = this.nodesDetails;
      data.group_name = data.group_name.value;
      this.$q.loading.show();
      await addNode(data)
        .then((res) => {
          if (res.code !== 0) {
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
          this.$router.push("/settings/nodes");
        })
        .finally(() => {
          this.$q.loading.hide();
        });
    },
  },
});
</script>
