<template>
  <SettingsAddCont
    title="Add User"
    addBtnTxt="Add User"
    :formList="formList"
    :formListDetails="userDetails"
    @submit:add="add"
  />
</template>

<script>
import { defineComponent } from "vue";
import SettingsAddCont from "src/components/SettingsAddCont.vue";
import { ROLES_GROUP } from "src/utils/constants";
import "src/css/settingsScreen.scss";

export default defineComponent({
  name: "UserAddPage",
  components: {
    SettingsAddCont,
  },
  data() {
    return {
      formList: [
        {
          label: "Username",
          model: "username",
          type: "text",
        },
        {
          label: "Password",
          model: "password",
          type: "password",
        },
        {
          label: "Email",
          model: "email",
          type: "email",
        },
        {
          label: "Group",
          model: "group",
          type: "text",
        },
        {
          label: "Role",
          model: "role",
          type: "select",
          option: ROLES_GROUP,
        },
        {
          label: "MFA Status",
          model: "mfaStatus",
          type: "radio",
          radioOption: [
            {
              label: "Enabled",
              value: 1,
            },
            {
              label: "Disabled",
              value: 0,
            },
          ],
        },
      ],
      userDetails: {
        username: null,
        password: null,
        email: null,
        group: null,
        role: null,
        mfaStatus: 0,
      },
    };
  },
  methods: {
    add() {
      this.$q.notify({
        message: `Added ${this.userDetails.username} successfully!`,
        type: "positive",
      });
      this.$router.push("/settings/user");
    },
  },
});
</script>
