<template>
  <div class="login-main-cont">
    <div class="login-header">
      <q-img src="src/assets/logo.png" height="200px" width="200px" />
      <p class="logo-text">DevOpsaurus</p>
    </div>
    <div class="login-form">
      <InputCont
        label="Username"
        :modelValue="username"
        @update:modelValue="username = $event"
        autofocus
        clearable
        errorMessage="Username is required"
      />
      <InputCont
        label="Password"
        :modelValue="password"
        @update:modelValue="password = $event"
        type="password"
        clearable
        errorMessage="Username is required"
      />
      <q-btn color="primary" label="Login" class="login-btn" @click="login" />
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import "src/css/loginScreen.scss";
import InputCont from "../components/InputCont.vue";
import { useQuasar } from "quasar";
import { useUserStore } from "src/stores/user";

export default defineComponent({
  name: "LoginPage",
  components: {
    InputCont,
  },
  data() {
    return {
      username: "",
      password: "",
      $q: useQuasar(),
      userStore: useUserStore(),
    };
  },
  methods: {
    login() {
      if (this.username === "" || this.password === "") {
        this.$q.notify({
          message: "Username and password are required",
          type: "negative",
        });
        return;
      }
      this.userStore.login("token!!!");
      this.$router.push("/dashboard");
    },
  },
});
</script>
