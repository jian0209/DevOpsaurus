<template>
  <div>
    <TitleContainer
      title="Command Management"
      subtitle="Manage Command with Using SSH Connection"
    />
    <div class="button-cont">
      <UsualButton
        label="Add Command"
        color="info"
        icon="add_circle_outline"
        @action:click="goToAddPage"
      />
    </div>
    <TableContainer
      :rows="rowData"
      :columns="columns"
      @edit:row="editRow($event)"
      @clone:row="cloneRow($event)"
      @disable:row="disableRow($event)"
      @enable:row="enableRow($event)"
      @delete:row="deleteRow($event)"
      @info:row="infoRow($event)"
      :searchValue="searchValue"
      @search:data="searchData"
      title="setting-command"
    />
    <DialogComponent
      title="Edit Command"
      :dialogStatus="editDialogStatus"
      :formList="formList"
      :formListDetails="formListDetails"
      testBtnTxt="Test SSH Connection"
      isFormDialog
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEdit"
      @test:connection="testConnect"
    />
    <DialogComponent
      title="Enable Command"
      :dialogStatus="enableDialogStatus"
      :subtitle="`This Will Enable Command {${selectedRow}} Be Execute By User`"
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEditStatus(1)"
    />
    <DialogComponent
      title="Disable Command"
      :dialogStatus="disableDialogStatus"
      :subtitle="`This Will Disable Command {${selectedRow}} Be Execute By User`"
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEditStatus(0)"
    />
    <DialogComponent
      title="Delete Command"
      :dialogStatus="deleteDialogStatus"
      :subtitle="`This Will Delete Command Record {${selectedRow}}`"
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitDelete"
    />
    <DialogComponent
      isInfoDialog
      title="Command Information Details"
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
import { generateColumn } from "src/utils/util.js";
import { STATUS } from "src/utils/constants.js";
import moment from "moment";
import "src/css/settingsScreen.scss";
import {
  getCommandList,
  editCommand,
  editStatusCommand,
  deleteCommand,
  testCommand,
} from "src/api/settings.js";

export default defineComponent({
  name: "SettingCommandPage",
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
          name: null,
          host: null,
          username: null,
          ssh_port: null,
          command: null,
          status: null,
          created_at: null,
        },
      ]),
      formList: [
        {
          label: "Name",
          model: "name",
          type: "text",
          readonly: true,
        },
        {
          label: "Host",
          model: "host",
          type: "text",
        },
        {
          label: "Username",
          model: "username",
          type: "text",
        },
        {
          label: "SSH Key",
          model: "ssh_key",
          type: "textarea",
          hint: "* SSH Key Should Be In PEM Format",
        },
        {
          label: "SSH Port",
          model: "ssh_port",
          type: "text",
        },
        {
          label: "Command",
          model: "command",
          type: "textarea",
          hint: "* Variable Eg: curl http://localhost:8080/{variable} {variable2}",
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
      this.$router.push("/settings/command/add");
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
      this.editDialogStatus = true;
    },
    cloneRow(row) {
      const rowString = btoa(
        JSON.stringify({
          host: row.host,
          username: row.username,
          ssh_port: row.ssh_port,
          ssh_key: row.ssh_key,
        })
      );
      const encryptedString = this.$CryptoJS.AES.encrypt(
        rowString,
        process.env.ENCRYPT_KEY
      );
      this.$router.push({
        path: "/settings/command/add",
        query: {
          isClone: true,
          passedData: encryptedString.toString(),
        },
      });
    },
    disableRow(row) {
      this.selectedRow = row.name;
      this.disableDialogStatus = true;
    },
    enableRow(row) {
      this.selectedRow = row.name;
      this.enableDialogStatus = true;
    },
    deleteRow(row) {
      this.selectedRow = row.name;
      this.deleteDialogStatus = true;
    },
    infoRow(row) {
      this.selectedInfoRow = {
        Name: row.name,
        Host: row.host,
        Username: row.username,
        "SSH Port": row.ssh_port,
        Command: row.command,
        Status: STATUS[row.status],
        "Created At": moment(row.created_at).format("YYYY-MM-DD HH:mm:ss"),
      };
      this.infoDialogStatus = true;
    },
    async submitEdit(data) {
      this.$q.loading.show();
      await editCommand(data)
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
            message: `Edit "${data.name}" successfully!`,
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
        name: this.selectedRow,
        status: status || 0,
      };
      await editStatusCommand(data)
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
        name: this.selectedRow,
      };
      await deleteCommand(data)
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
      await getCommandList(submitData)
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

          if (!res.data || !Array.isArray(res.data.commands)) {
            this.rowData = [];
            return;
          }

          if (res.data.commands.length === 0) {
            this.rowData = [];
          } else {
            this.rowData = res.data.commands;
          }
        })
        .finally(() => {
          this.$q.loading.hide();
        });
    },
    async testConnect() {
      this.$q.loading.show();
      await testCommand(this.formListDetails)
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
            message: this.$t("notify.testSuccess", { platform: "SSH" }),
            type: "positive",
          });
        })
        .finally(() => this.$q.loading.hide());
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
