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
      :rows="rowData"
      :columns="columns"
      @edit:row="editRow($event)"
      @disable:row="disableRow($event)"
      @enable:row="enableRow($event)"
      @delete:row="deleteRow($event)"
      @info:row="infoRow($event)"
      :searchValue="searchValue"
      @search:data="searchData"
      title="setting-user"
    />
    <DialogComponent
      title="Edit User"
      :dialogStatus="editDialogStatus"
      :formList="formList"
      :formListDetails="formListDetails"
      isFormDialog
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEdit"
    />
    <DialogComponent
      title="Enable User"
      :dialogStatus="enableDialogStatus"
      :subtitle="`This Will Enable User {${selectedRow}} Log In`"
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEditStatus(1)"
    />
    <DialogComponent
      title="Disable User"
      :dialogStatus="disableDialogStatus"
      :subtitle="`This Will Disable User {${selectedRow}} Log In`"
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEditStatus(0)"
    />
    <DialogComponent
      title="Delete User"
      :dialogStatus="deleteDialogStatus"
      :subtitle="`This Will Delete User {${selectedRow}}`"
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitDelete"
    />
    <DialogComponent
      isInfoDialog
      title="User Information Details"
      :dialogStatus="infoDialogStatus"
      :formListDetails="selectedInfoRow"
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
import { generateColumn } from "src/utils/util.js";
import "src/css/settingsScreen.scss";
import moment from "moment";
import {
  getUserList,
  editUser,
  editStatusUser,
  deleteUser,
} from "src/api/settings";

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
      columns: ref([]),
      rowData: ref([
        {
          id: null,
          username: null,
          email: null,
          role: null,
          group: null,
          mfa_status: null,
          status: null,
          created_at: null,
        },
      ]),
      formList: [
        {
          label: "Username",
          model: "username",
          type: "text",
          readonly: true,
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
        {
          label: "Force User To Change Password",
          model: "is_password_force_reset",
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
      infoDialogStatus: ref(false),
      selectedInfoRow: ref({}),
      selectedRow: ref(""),
      searchValue: ref({ name: null }),
    };
  },
  methods: {
    initData() {
      this.columns = generateColumn(
        this.rowData,
        false,
        true,
        true,
        false,
        false,
        true
      );
      this.getList();
    },
    goToAddPage() {
      this.$router.push("/settings/user/add");
    },
    updateDialogStatus(status) {
      this.editDialogStatus = status;
      this.enableDialogStatus = status;
      this.disableDialogStatus = status;
      this.deleteDialogStatus = status;
      this.infoDialogStatus = status;
    },
    editRow(row) {
      for (const key in row) {
        this.formListDetails[key] = row[key];
      }
      this.formListDetails.role = {
        label: ROLES[row.role] || row.role.label,
        value: row.role || row.role.value,
      };
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
    infoRow(row) {
      this.selectedInfoRow = {
        Id: row.id,
        Username: row.username,
        Email: row.email || "-",
        Role: ROLES[row.role] || "-",
        Group: row.group,
        "Mfa Status": STATUS[row.mfa_status],
        "Force Change Password": STATUS[row.is_password_force_reset] || "-",
        Status: STATUS[row.status],
        "Created At": moment(row.created_at).format("YYYY-MM-DD HH:mm:ss"),
      };
      this.infoDialogStatus = true;
    },
    async submitEdit(data) {
      this.$q.loading.show();
      data.role = data.role.value;

      await editUser(data)
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
              message: this.$t(`api.${res.code || "unknown"}`),
              type: "negative",
            });
            return;
          }
          this.$q.notify({
            message: `Edit "${data.username}" successfully!`,
            type: "positive",
          });
        })
        .finally(() => {
          this.getList();
          this.$q.loading.hide();
        });
    },
    async submitEditStatus(status) {
      this.$q.loading.show();
      const data = {
        username: this.selectedRow,
        status: status || 0,
      };
      await editStatusUser(data)
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
              message: this.$t(`api.${res.code || "unknown"}`),
              type: "negative",
            });
            return;
          }
          this.$q.notify({
            message: `${status ? "Enable" : "Disable"} "${
              this.selectedRow
            }" successfully!`,
            type: "positive",
          });
        })
        .finally(() => {
          this.getList();
          this.$q.loading.hide();
        });
    },
    async submitDelete() {
      this.$q.loading.show();
      const data = {
        username: this.selectedRow,
      };
      await deleteUser(data)
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
              message: this.$t(`api.${res.code || "unknown"}`),
              type: "negative",
            });
            return;
          }
          this.$q.notify({
            message: `Delete "${this.selectedRow}" successfully!`,
            type: "positive",
          });
        })
        .finally(() => {
          this.getList();
          this.$q.loading.hide();
        });
    },
    async getList(searchData) {
      const submitData = { name: null };
      if (searchData && searchData.name) {
        submitData.name = searchData.name;
      }
      this.$q.loading.show();
      await getUserList(submitData)
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
              message: this.$t(`api.${res.code || "unknown"}`),
              type: "negative",
            });
            return;
          }

          if (!res.data || !Array.isArray(res.data.users)) {
            this.rowData = [];
            return;
          }

          if (res.data.users.length === 0) {
            this.rowData = [];
          } else {
            this.rowData = res.data.users;
          }
        })
        .finally(() => {
          this.$q.loading.hide();
        });
    },
    searchData(data) {
      this.getList(data);
    },
  },
  created() {
    this.initData();
  },
});
</script>
