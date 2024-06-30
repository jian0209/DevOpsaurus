<template>
  <SettingsAddCont
    title="Add Redis Connection"
    addBtnTxt="Add Redis Connection"
    testBtnTxt="Test Redis Connection"
    :formList="formList"
    :formListDetails="redisDetails"
    @submit:add="add"
  />
</template>

<script>
import { defineComponent } from "vue";
import SettingsAddCont from "src/components/SettingsAddCont.vue";
import "src/css/settingsScreen.scss";

export default defineComponent({
  name: "RedisAddPage",
  components: {
    SettingsAddCont,
  },
  data() {
    return {
      formList: [
        {
          label: "Host",
          model: "host",
          type: "text",
        },
        {
          label: "Port",
          model: "port",
          type: "text",
        },
        {
          label: "Database",
          model: "database",
          type: "text",
        },
        {
          label: "Auth",
          model: "auth",
          type: "text",
        },
        {
          label: "Get",
          model: "get",
          type: "text",
        },
      ],
      redisDetails: {
        host: null,
        port: null,
        database: null,
        auth: null,
        get: null,
      },
    };
  },
  methods: {
    add() {
      this.$router.push("/settings/redis");
    },
  },
});
</script>
