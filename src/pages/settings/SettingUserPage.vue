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
    <TableContainer
      :rows="dummyData"
      :columns="columns"
      @edit:row="editRow($event)"
      @disable:row="disableRow($event)"
      @enable:row="enableRow($event)"
      @delete:row="deleteRow($event)"
    />
    <DialogComponent
      title="Edit User"
      :dialogStatus="editDialogStatus"
      :formList="formList"
      :formListDetails="formListDetails"
      isFormDialog
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      title="Enable User"
      :dialogStatus="enableDialogStatus"
      :subtitle="`This Will Enable User {${selectedRow}} Log In`"
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      title="Disable User"
      :dialogStatus="disableDialogStatus"
      :subtitle="`This Will Disable User {${selectedRow}} Log In`"
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      title="Delete User"
      :dialogStatus="deleteDialogStatus"
      :subtitle="`This Will Delete User {${selectedRow}}`"
      @update:dialogStatus="updateDialogStatus"
    />
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import TitleContainer from "src/components/TitleCont.vue";
import TableContainer from "src/components/TableCont.vue";
import UsualButton from "src/components/Button.vue";
import DialogComponent from "src/components/Dialog.vue";
import { ROLES, ROLES_GROUP, STATUS } from "src/utils/constants.js";
import moment from "moment";
import "src/css/settingsScreen.scss";

export default defineComponent({
  name: "SettingUserPage",
  components: {
    TitleContainer,
    TableContainer,
    UsualButton,
    DialogComponent,
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
          name: "username",
          required: true,
          label: "Username",
          align: "left",
          field: (row) => row.username,
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
          format: (val) => `${ROLES[val] || val.label}` || "Unknown",
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
          name: "mfaStatus",
          required: true,
          label: "MFA",
          align: "left",
          field: (row) => row.mfaStatus,
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
          username: "John Doe",
          email: "john123@gmail.com",
          group: "IT",
          mfaStatus: 1,
          role: 2,
          status: 1,
          createdAt: 1719553933000,
        },
        {
          id: 2,
          username: "Jane Doe",
          email: "jane123@gmail.com",
          group: "IT",
          mfaStatus: 1,
          role: 3,
          status: 1,
          createdAt: 1719553933000,
        },
        {
          id: 3,
          username: "John Smith",
          email: "smith@gmsil.com",
          group: "IT",
          mfaStatus: 0,
          role: 1,
          status: 0,
          createdAt: 1719553933000,
        },
      ],
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
      formListDetails: ref({}),
      editDialogStatus: ref(false),
      enableDialogStatus: ref(false),
      disableDialogStatus: ref(false),
      deleteDialogStatus: ref(false),
      selectedRow: ref(""),
    };
  },
  methods: {
    goToAddPage() {
      this.$router.push("/settings/user/add");
    },
    updateDialogStatus(status) {
      this.editDialogStatus = status;
      this.enableDialogStatus = status;
      this.disableDialogStatus = status;
      this.deleteDialogStatus = status;
    },
    editRow(row) {
      row.role = {
        label: ROLES[row.role] || row.role.label,
        value: row.role || row.role.value,
      };
      this.formListDetails = row;
      this.editDialogStatus = true;
    },
    disableRow(row) {
      this.selectedRow = row.username;
      this.disableDialogStatus = true;
    },
    enableRow(row) {
      this.selectedRow = row.username;
      this.enableDialogStatus = true;
    },
    deleteRow(row) {
      this.selectedRow = row.username;
      this.deleteDialogStatus = true;
    },
  },
});
</script>
