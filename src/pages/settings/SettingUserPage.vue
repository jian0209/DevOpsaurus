<template>
  <div>
    <TitleContainer title="User Management" subtitle="Manage users and roles" />
    <div class="button-cont">
      <UsualButton
        label="Add User"
        color="info"
        icon="add_circle_outline"
        @action:click="goToAddPage"
      />
    </div>
    <TableContainer :rows="dummyData" :columns="columns" />
  </div>
</template>

<script>
import { defineComponent } from "vue";
import TitleContainer from "src/components/TitleCont.vue";
import TableContainer from "src/components/TableCont.vue";
import UsualButton from "src/components/Button.vue";
import { ROLES, STATUS } from "src/utils/constants.js";
import { useCommonStore } from "src/stores/common.js";
import moment from "moment";
import "src/css/settingsScreen.scss";

export default defineComponent({
  name: "SettingUserPage",
  components: {
    TitleContainer,
    TableContainer,
    UsualButton,
  },
  data() {
    return {
      columns: [
        {
          name: "id",
          required: true,
          label: "ID",
          align: "left",
          field: (row) => row.id,
          format: (val) => `${val}`,
          sortable: true,
        },
        {
          name: "name",
          required: true,
          label: "Username",
          align: "left",
          field: (row) => row.name,
          format: (val) => `${val}`,
          sortable: true,
        },
        {
          name: "email",
          required: true,
          label: "Email",
          align: "left",
          field: (row) => row.email,
          format: (val) => `${val}`,
          sortable: true,
        },
        {
          name: "group",
          required: true,
          label: "Group",
          align: "left",
          field: (row) => row.group,
          format: (val) => `${val}`,
          sortable: true,
        },
        {
          name: "role",
          required: true,
          label: "Role",
          align: "left",
          field: (row) => row.role,
          format: (val) => ROLES[val] || "Unknown",
          sortable: true,
        },
        {
          name: "createdAt",
          required: true,
          label: "Created At",
          align: "left",
          field: (row) => row.createdAt,
          format: (val) => moment(val).format("YYYY-MM-DD HH:mm:ss"),
          sortable: true,
        },
        {
          name: "isMfaEnabled",
          required: true,
          label: "MFA",
          align: "left",
          field: (row) => row.isMfaEnabled,
          format: (val) => STATUS[val] || "Unknown",
          sortable: true,
        },
        {
          name: "status",
          required: true,
          label: "Status",
          align: "left",
          field: (row) => row.status,
          format: (val) => STATUS[val] || "Unknown",
          sortable: true,
        },
        {
          name: "operate",
          field: "operate",
          label: "Operate",
          align: "right",
          sortable: false,
        },
      ],
      dummyData: [
        {
          id: 1,
          name: "John Doe",
          email: "john123@gmail.com",
          group: "IT",
          isMfaEnabled: 1,
          role: 2,
          status: 1,
          createdAt: 1719553933000,
        },
        {
          id: 2,
          name: "Jane Doe",
          email: "jane123@gmail.com",
          group: "IT",
          isMfaEnabled: 1,
          role: 3,
          status: 1,
          createdAt: 1719553933000,
        },
        {
          id: 3,
          name: "John Smith",
          email: "smith@gmsil.com",
          group: "IT",
          isMfaEnabled: 0,
          role: 1,
          status: 0,
          createdAt: 1719553933000,
        },
      ],
      commonStore: useCommonStore(),
    };
  },
  methods: {
    goToAddPage() {
      this.$router.push("/settings/user/add");
    },
  },
});
</script>
