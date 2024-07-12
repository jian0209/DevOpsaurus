<template>
  <div class="login-main-cont">
    <div class="login-header">
      <q-img src="src/assets/logo.png" height="200px" width="200px" />
      <p class="logo-text">DevOpsaurus</p>
    </div>
    <div class="login-form" v-for="(item, index) in formList" :key="index">
      <div class="form-input-name">{{ item.label }}</div>
      <q-input
        @keypress="onKeyPress"
        v-model="formDetails[item.model]"
        :type="item.type"
        class="usual-form-input"
        color="secondary"
        dense
        outlined
      />
    </div>
    <q-btn
      color="primary"
      :loading="isLoading"
      :label="$t('loginPage.loginBtn')"
      class="login-btn"
      @click="login"
    />
  </div>
</template>

<script>
import { defineComponent } from "vue";
import "src/css/loginScreen.scss";
import { useUserStore } from "src/stores/user";
import { login } from "src/api/auth";
import {
  LOGIN_WITH_PASSWORD_ONLY,
  LOGIN_WITH_MFA_WITHOUT_SECRET_KEY,
  LOGIN_WITH_MFA_WITH_SECRET_KEY,
  LOGIN_WITH_FORCE_RESET_PASSWORD,
} from "src/utils/constants.js";

export default defineComponent({
  name: "LoginPage",
  data() {
    return {
      formList: [
        {
          label: `${this.$t("loginPage.username")}`,
          model: "username",
          type: "text",
        },
        {
          label: `${this.$t("loginPage.password")}`,
          model: "password",
          type: "password",
        },
      ],
      formDetails: {
        username: null,
        password: null,
      },
      userStore: useUserStore(),
      isLoading: false,
    };
  },
  methods: {
    async login() {
      if (!this.formDetails.username || !this.formDetails.password) {
        this.$q.notify({
          message: "Username and password are required",
          type: "negative",
        });
        return;
      }
      this.isLoading = true;
      await login(this.formDetails)
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
          console.log(res.data);

          if (res.data.step === LOGIN_WITH_PASSWORD_ONLY) {
            this.userStore.login(
              res.data.token,
              res.data.username,
              res.data.role
            );
            this.$q.notify({
              message: this.$t("dialog.welcome", {
                name: res.data.username,
              }),
              type: "positive",
            });
            if (res.data.role === 0) {
              this.$router.push({ path: "/ups-monitor" });
            } else {
              this.$router.push({ path: "/dashboard" });
            }
          } else if (res.data.step === LOGIN_WITH_MFA_WITHOUT_SECRET_KEY) {
            this.userStore.setUsername(res.data.username);
            setTimeout(() => {
              this.$router.push({ path: "/login/mfa-register" });
            }, 200);
          } else if (res.data.step === LOGIN_WITH_MFA_WITH_SECRET_KEY) {
            this.userStore.setUsername(res.data.username);
            this.$router.push({ path: "/login/mfa" });
          } else if (res.data.step === LOGIN_WITH_FORCE_RESET_PASSWORD) {
            this.userStore.setUsername(res.data.username);
            this.$router.push({ path: "/login/reset-password" });
          } else {
            this.$q.notify({
              message: this.$t("api.unknown"),
              type: "negative",
            });
          }
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    onKeyPress(e) {
      if (e.key === "Enter") {
        this.login();
      }
    },
  },
});
</script>
