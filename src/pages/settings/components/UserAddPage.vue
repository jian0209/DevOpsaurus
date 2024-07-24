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
import { addUser } from "src/api/settings";

export default defineComponent({
  name: "UserAddPage",
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
      this.userDetails.group = passedData.group;
      this.userDetails.role = ROLES_GROUP.find(
        (role) => role.value === parseInt(passedData.role)
      );
      this.userDetails.mfa_status = parseInt(passedData.mfa_status);
    }
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
          model: "mfa_status",
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
        mfa_status: 0,
      },
    };
  },
  methods: {
    async add() {
      const data = this.userDetails;
      data.role = data.role.value;
      this.$q.loading.show();
      await addUser(data)
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
            message: `Added ${data.username} successfully!`,
            type: "positive",
          });
          this.$router.push("/settings/user");
        })
        .finally(() => this.$q.loading.hide());
    },
  },
});
</script>
