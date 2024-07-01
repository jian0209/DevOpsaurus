<template>
  <div>
    <TitleContainer
      title="Redis Management"
      subtitle="Manage Redis Connection"
    />
    <div class="button-cont">
      <UsualButton
        label="Add Redis Connection"
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
      title="Edit Redis"
      :dialogStatus="editDialogStatus"
      :formList="formList"
      :formListDetails="formListDetails"
      isFormDialog
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      title="Enable Redis"
      :dialogStatus="enableDialogStatus"
      :subtitle="`This Will Enable Redis {${selectedRow}} Be View By User`"
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      title="Disable Redis"
      :dialogStatus="disableDialogStatus"
      :subtitle="`This Will Disable Redis {${selectedRow}} Be View By User`"
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      title="Delete Redis"
      :dialogStatus="deleteDialogStatus"
      :subtitle="`This Will Delete Redis Record {${selectedRow}}`"
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
import { STATUS } from "src/utils/constants.js";
import moment from "moment";
import "src/css/settingsScreen.scss";

export default defineComponent({
  name: "SettingRedisPage",
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
          name: "host",
          required: true,
          label: "Host",
          align: "left",
          field: (row) => row.host,
          format: (val) => `${val}`,
          sortable: true,
        },
        {
          name: "port",
          required: true,
          label: "Port",
          align: "left",
          field: (row) => row.port,
          format: (val) => `${val}`,
          sortable: true,
        },
        {
          name: "database",
          required: true,
          label: "Database",
          align: "left",
          field: (row) => row.database,
          format: (val) => `${val}`,
          sortable: true,
        },
        {
          name: "get",
          required: true,
          label: "Get",
          align: "left",
          field: (row) => row.get,
          format: (val) => `${val.substring(0, 20)}...`,
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
          host: "localhost",
          port: "6379",
          database: 0,
          auth: "password",
          get: "debug:trx_status",
          status: 1,
          createdAt: 1719553933000,
        },
      ],
      formList: [
        {
          label: "Host",
          model: "host",
          type: "text",
        },
        {
          label: "Port",
          model: "port",
          type: "text",
        },
        {
          label: "Database",
          model: "database",
          type: "text",
        },
        {
          label: "Auth",
          model: "auth",
          type: "text",
        },
        {
          label: "Get",
          model: "get",
          type: "text",
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
      this.$router.push("/settings/redis/add");
    },
    updateDialogStatus(status) {
      this.editDialogStatus = status;
      this.enableDialogStatus = status;
      this.disableDialogStatus = status;
      this.deleteDialogStatus = status;
    },
    editRow(row) {
      this.formListDetails = row;
      this.editDialogStatus = true;
    },
    disableRow(row) {
      this.selectedRow = `${row.host}:${row.port}`;
      this.disableDialogStatus = true;
    },
    enableRow(row) {
      this.selectedRow = `${row.host}:${row.port}`;
      this.enableDialogStatus = true;
    },
    deleteRow(row) {
      this.selectedRow = `${row.host}:${row.port}`;
      this.deleteDialogStatus = true;
    },
  },
});
</script>
