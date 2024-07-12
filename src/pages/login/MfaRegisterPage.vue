<template>
  <div class="login-main-cont">
    <div class="login-header">
      <q-img src="src/assets/logo.png" height="200px" width="200px" />
      <p class="logo-text">DevOpsaurus</p>
      <q-img
        :src="'data:image/png;base64,' + qrCodeImg"
        height="200px"
        width="200px"
      />
    </div>
    <div class="mfa-form" v-for="(item, index) in formList" :key="index">
      <div class="mfa-form-input-name">{{ item.label }}</div>
      <q-input
        @keypress="onKeyPress"
        v-model="formDetails[item.model]"
        :type="item.type"
        class="mfa-form-input"
        color="secondary"
        dense
        outlined
      />
    </div>
    <q-btn
      color="primary"
      :loading="isLoading"
      :label="$t('loginPage.submitBtn')"
      class="login-btn"
      @click="localMfaLogin"
    />
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import "src/css/loginScreen.scss";
import { useUserStore } from "src/stores/user";
import { getMfaImg, mfaLogin } from "src/api/auth";

export default defineComponent({
  name: "MfaRegisterPage",
  data() {
    return {
      formList: [
        {
          label: `${this.$t("loginPage.mfaCode")}`,
          model: "mfa_token",
          type: "text",
        },
      ],
      formDetails: {
        mfa_token: null,
      },
      userStore: useUserStore(),
      isLoading: false,
      qrCodeImg: ref(null),
    };
  },
  created() {
    this.getQrCodeImage();
  },
  methods: {
    async getQrCodeImage() {
      await getMfaImg({ username: this.userStore.username }).then((res) => {
        if (res.code !== 0) {
          if (res.code === 9001) {
            this.$q.notify({
              message: `${res.data.msg || "Unknown Error"}`,
              type: "negative",
            });
            return;
          }
          this.$q.notify({
            message: `${this.$t("notify.getQrCodeFailed")}`,
            type: "negative",
          });
          this.$router.push("/login");
          return;
        }
        this.qrCodeImg = res.data.img;
      });
    },
    async localMfaLogin() {
      if (this.formDetails.mfa_token === null) {
        this.$q.notify({
          message: `${this.$t("notify.mfaEmpty")}`,
          type: "negative",
        });
        return;
      }
      this.isLoading = true;
      this.formDetails.username = this.userStore.username;
      await mfaLogin(this.formDetails)
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
          this.userStore.login(
            res.data.token,
            this.userStore.username,
            res.data.role
          );
          this.$router.push("/dashboard");
          this.$q.notify({
            message: this.$t("dialog.welcome", {
              name: this.userStore.username,
            }),
            type: "positive",
          });
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    onKeyPress(e) {
      if (e.key === "Enter") {
        this.localMfaLogin();
      }
    },
  },
});
</script>
