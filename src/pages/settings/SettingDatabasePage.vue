<template>
  <div>
    <TitleContainer
      title="Database Management"
      subtitle="Manage Database Connection (Currently only support MySQL)"
    />
    <div class="button-cont">
      <UsualButton
        label="Add Database Connection"
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
      title="Edit database"
      :dialogStatus="editDialogStatus"
      :formList="formList"
      :formListDetails="formListDetails"
      testBtnTxt="Get Databases and Tables"
      isFormDialog
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      title="Enable Database"
      :dialogStatus="enableDialogStatus"
      :subtitle="`This Will Enable Database {${selectedRow}} Be View or Edit By User`"
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      title="Disable Database"
      :dialogStatus="disableDialogStatus"
      :subtitle="`This Will Disable Database {${selectedRow}} Be View or Edit By User`"
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      title="Delete Database"
      :dialogStatus="deleteDialogStatus"
      :subtitle="`This Will Delete Database Record {${selectedRow}}`"
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      isInfoDialog
      title="Database Information Details"
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
  name: "SettingDatabasePage",
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
          name: "production",
          host: "localhost",
          port: "3306",
          username: "root",
          database: "coinsdo_deposit",
          table: "t_deposit_record",
          status: 1,
          createdAt: 1719553933000,
        },
      ],
      formList: [
        {
          label: "Name",
          model: "name",
          type: "text",
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
          label: "Password",
          model: "password",
          type: "text",
        },
        {
          label: "Database",
          model: "database",
          type: "select",
          option: [
            {
              label: "Database 1",
              value: "database1",
            },
            {
              label: "Database 2",
              value: "database2",
            },
          ],
        },
        {
          label: "Table",
          model: "table",
          type: "select",
          option: [
            {
              label: "Table 1",
              value: "table1",
            },
            {
              label: "Table 2",
              value: "table2",
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
    };
  },
  methods: {
    initData() {
      this.columns = generateColumn(this.dummyData, false, true, true);
    },
    goToAddPage() {
      this.$router.push("/settings/database/add");
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
