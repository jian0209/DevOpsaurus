<template>
  <SettingsAddCont
    title="Add Redis Connection"
    addBtnTxt="Add Redis Connection"
    testBtnTxt="Test Redis Connection"
    :formList="formList"
    :formListDetails="redisDetails"
    @submit:add="add"
    @test:connection="testRedisConnection"
  />
</template>

<script>
import { defineComponent } from "vue";
import SettingsAddCont from "src/components/SettingsAddCont.vue";
import { addRedis, testRedis } from "src/api/settings.js";
import "src/css/settingsScreen.scss";
import AESCipher from "src/utils/crypto";

export default defineComponent({
  name: "RedisAddPage",
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
      this.redisDetails.host = passedData.host;
      this.redisDetails.port = passedData.port;
      this.redisDetails.database = passedData.database;
      this.redisDetails.auth = passedData.auth;
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
        name: null,
        host: null,
        port: null,
        database: null,
        auth: null,
        get: null,
      },
      crypto: new AESCipher(),
    };
  },
  methods: {
    async add() {
      this.$q.loading.show();
      const submitData = {
        ...this.redisDetails,
        auth: this.crypto.encrypt(this.redisDetails.auth),
      };
      await addRedis(submitData)
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
            message: `Added ${this.redisDetails.host} successfully!`,
            type: "positive",
          });
          this.$router.push("/settings/redis");
        })
        .finally(() => {
          this.$q.loading.hide();
        });
    },
    async testRedisConnection() {
      this.$q.loading.show();
      const submitData = {
        ...this.redisDetails,
        auth: this.crypto.encrypt(this.redisDetails.auth),
      };
      await testRedis(submitData)
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
            message: `Tested ${this.redisDetails.host} successfully!`,
            type: "positive",
          });
        })
        .finally(() => {
          this.$q.loading.hide();
        });
    },
  },
});
</script>
