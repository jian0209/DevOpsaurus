<template>
  <div>
    <TitleContainer title="Add User" />
    <q-form @submit="submitAddUser" class="form-main-cont">
      <div
        class="form-input-cont"
        v-for="(item, index) in formList"
        :key="index"
      >
        <div class="form-input-name">{{ item.label }}</div>
        <q-input
          v-if="
            item.type === 'text' ||
            item.type === 'email' ||
            item.type === 'password'
          "
          v-model="userDetails[item.model]"
          :type="item.type"
          class="usual-form-input"
          color="secondary"
          dense
          outlined
        />
        <q-select
          v-if="item.type === 'select'"
          class="usual-form-input"
          v-model="userDetails[item.model]"
          :options="roles"
          color="secondary"
          outlined
          dense
        />
        <div v-if="item.type === 'radio'" class="usual-form-input">
          <q-radio
            v-model="userDetails.mfaStatus"
            :val="1"
            label="Enabled"
            color="secondary"
          />
          <q-radio
            v-model="userDetails.mfaStatus"
            :val="0"
            label="Disabled"
            color="secondary"
          />
        </div>
      </div>
      <div class="add-btn-cont">
        <UsualButton label="Add User" type="submit" color="info" />
      </div>
    </q-form>
  </div>
</template>

<script>
import { computed, defineComponent } from "vue";
import TitleContainer from "src/components/TitleCont.vue";
import UsualButton from "src/components/Button.vue";
import "src/css/settingsScreen.scss";

export default defineComponent({
  name: "UserAddPage",
  components: {
    TitleContainer,
    UsualButton,
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
          option: "roleOptions",
        },
        {
          label: "MFA Status",
          model: "mfaStatus",
          type: "radio",
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
      roleOptions: [
        {
          label: "Admin",
          value: 3,
        },
        {
          label: "Editor",
          value: 2,
        },
        {
          label: "Reader",
          value: 1,
        },
        {
          label: "Visitor",
          value: 0,
        },
      ],
    };
  },
  methods: {
    submitAddUser() {
      console.log("Add user", this.userDetails);
      this.$router.push("/settings/user");
    },
  },
  created() {
    this.title = computed(() => this.commonStore.pageTitle);
  },
});
</script>
