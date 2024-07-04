<template>
  <div class="login-main-cont">
    <div class="login-header">
      <q-img src="src/assets/logo.png" height="200px" width="200px" />
      <p class="logo-text">DevOpsaurus</p>
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
import { defineComponent } from "vue";
import "src/css/loginScreen.scss";
import { useUserStore } from "src/stores/user";
import { mfaLogin } from "src/api/auth";
import { LOGIN_WITH_FORCE_RESET_PASSWORD } from "src/utils/constants.js";

export default defineComponent({
  name: "MfaSubmitPage",
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
    };
  },
  methods: {
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
            this.$q.notify({
              message: this.$t(`api.${res.code}`),
              type: "negative",
            });
            return;
          }
          this.userStore.login(res.data.token, this.userStore.username);
          if (res.data.step === LOGIN_WITH_FORCE_RESET_PASSWORD) {
            this.$router.push("/login/reset-password");
            return;
          }
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
