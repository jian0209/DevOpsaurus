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
      @click="changePassword"
    />
  </div>
</template>

<script>
import { defineComponent } from "vue";
import "src/css/loginScreen.scss";
import { useUserStore } from "src/stores/user";
import { resetPassword, logout } from "src/api/auth";

export default defineComponent({
  name: "ResetPasswordPage",
  data() {
    return {
      formList: [
        {
          label: `${this.$t("loginPage.newPassword")}`,
          model: "password",
          type: "password",
        },
      ],
      formDetails: {
        password: null,
      },
      userStore: useUserStore(),
      isLoading: false,
    };
  },
  methods: {
    async changePassword() {
      if (this.formDetails.password === null) {
        this.$q.notify({
          message: `${this.$t("notify.passwordEmpty")}`,
          type: "negative",
        });
        return;
      }
      this.isLoading = true;
      this.formDetails.username = this.userStore.username;
      await resetPassword(this.formDetails)
        .then((res) => {
          if (res.code !== 0) {
            this.$q.notify({
              message: this.$t(`api.${res.code}`),
              type: "negative",
            });
            return;
          }
          this.userStore.logout();
          this.$router.push("/login");

          logout();

          this.$q.notify({
            message: this.$t("notify.changePasswordSuccess"),
            type: "positive",
          });
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    onKeyPress(e) {
      if (e.key === "Enter") {
        this.changePassword();
      }
    },
  },
});
</script>
