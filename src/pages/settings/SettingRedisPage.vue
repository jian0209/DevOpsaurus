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
      @info:row="infoRow($event)"
    />
    <DialogComponent
      title="Edit Redis"
      :dialogStatus="editDialogStatus"
      :formList="formList"
      :formListDetails="formListDetails"
      testBtnTxt="Test Redis Connection"
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
    <DialogComponent
      isInfoDialog
      title="Redis Information Details"
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
import { STATUS } from "src/utils/constants.js";
import { generateColumn } from "src/utils/util.js";
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
      columns: ref([]),
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
      infoDialogStatus: ref(false),
      selectedInfoRow: ref({}),
      selectedRow: ref(""),
    };
  },
  methods: {
    initData() {
      this.columns = generateColumn(this.dummyData, false, true, true);
    },
    goToAddPage() {
      this.$router.push("/settings/redis/add");
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
    infoRow(row) {
      for (const key in row) {
        this.selectedInfoRow[key] = row[key];
      }
      this.selectedInfoRow.status = STATUS[this.selectedInfoRow.status];
      this.selectedInfoRow.createdAt = moment(
        this.selectedInfoRow.createdAt
      ).format("YYYY-MM-DD HH:mm:ss");
      this.infoDialogStatus = true;
    },
  },
  created() {
    this.initData();
  },
});
</script>
