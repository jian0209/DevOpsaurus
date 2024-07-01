<template>
  <div class="login-main-cont">
    <div class="login-header">
      <q-img src="src/assets/logo.png" height="200px" width="200px" />
      <p class="logo-text">DevOpsaurus</p>
    </div>
    <div class="login-form" v-for="(item, index) in formList" :key="index">
      <div class="form-input-name">{{ item.label }}</div>
      <q-input
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

export default defineComponent({
  name: "LoginPage",
  components: {
    // InputCont,
  },
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
    };
  },
  methods: {
    login() {
      if (!this.formDetails.username || !this.formDetails.password) {
        this.$q.notify({
          message: "Username and password are required",
          type: "negative",
        });
        return;
      }
      this.userStore.login("token!!!", {
        username: this.formList.username,
        password: this.formList.password,
      });
      this.$q.notify({
        // message: `Welcome ${this.formDetails.username}!`,
        message: this.$t("dialog.welcome", {
          name: this.formDetails.username,
        }),
        type: "positive",
      });
      this.$router.push({ path: "/dashboard" });
    },
  },
});
</script>
