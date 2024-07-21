<template>
  <div>
    <TitleContainer title="UPS Management" subtitle="Manage UPS Connection" />
    <div class="button-cont">
      <UsualButton
        label="Add UPS Connection"
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
      title="setting-ups"
    />
    <DialogComponent
      title="Edit UPS"
      :dialogStatus="editDialogStatus"
      :formList="formList"
      :formListDetails="formListDetails"
      isFormDialog
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      title="Enable UPS"
      :dialogStatus="enableDialogStatus"
      :subtitle="`This Will Enable UPS {${selectedRow}} Be Monitored`"
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      title="Disable User"
      :dialogStatus="disableDialogStatus"
      :subtitle="`This Will Disable UPS {${selectedRow}} Be Monitored`"
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      title="Delete User"
      :dialogStatus="deleteDialogStatus"
      :subtitle="`This Will Delete UPS Record {${selectedRow}}`"
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      isInfoDialog
      title="UPS Information Details"
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
          name: "Tung Ann UPS",
          ipAddr: "122.11.149.168",
          port: "8888",
          location: "Tung Ann",
          parameter: JSON.stringify({
            ups_bat: "value",
            ups_log: 123,
            ups_asd: true,
            key: {
              key: "value",
            },
          }),
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
          label: "IP Address",
          model: "ipAddr",
          type: "text",
        },
        {
          label: "Port",
          model: "port",
          type: "text",
        },
        {
          label: "Location",
          model: "location",
          type: "text",
        },
        {
          label: "Parameter (JSON)",
          model: "parameter",
          type: "textarea",
          placeholder:
            'e.g. {"key": string, "key": int, "key": bool, "key": {"key": string}}',
          hint: "* Will use JSON.stringify() to format your input.",
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
      this.columns = generateColumn(
        this.dummyData,
        false,
        true,
        true,
        false,
        false,
        true
      );
    },
    goToAddPage() {
      this.$router.push("/settings/ups/add");
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
