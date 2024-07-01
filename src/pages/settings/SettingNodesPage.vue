<template>
  <div>
    <TitleContainer
      title="Nodes Management"
      subtitle="Manage Nodes Connection"
    />
    <div class="button-cont">
      <UsualButton
        label="Add Node Connection"
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
      title="Edit Nodes"
      :dialogStatus="editDialogStatus"
      :formList="formList"
      :formListDetails="formListDetails"
      isFormDialog
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      title="Enable Nodes"
      :dialogStatus="enableDialogStatus"
      :subtitle="`This Will Enable Nodes {${selectedRow}} Be Monitored`"
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      title="Disable Nodes"
      :dialogStatus="disableDialogStatus"
      :subtitle="`This Will Disable Nodes {${selectedRow}} Be Monitored`"
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      title="Delete Nodes"
      :dialogStatus="deleteDialogStatus"
      :subtitle="`This Will Delete Nodes Record {${selectedRow}}`"
      @update:dialogStatus="updateDialogStatus"
    />
    <DialogComponent
      isInfoDialog
      title="Nodes Information Details"
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
import { CRYPTO_CURRENCY_GROUP, STATUS } from "src/utils/constants.js";
import { generateColumn } from "src/utils/util.js";
import moment from "moment";
import "src/css/settingsScreen.scss";

export default defineComponent({
  name: "SettingNodesPage",
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
          name: "ETH - Tung Ann",
          groupName: "ETH",
          getUrl:
            "https://mainnet.coinsdo.com/monitor/nodes/check?network=mainnet&id=1",
          targetUrl: "http://203.117.22.213:10001/eth-achavie",
          status: 1,
          createdAt: 1719553933000,
        },
        {
          id: 2,
          name: "ETH - International Plaza",
          groupName: "ETH",
          getUrl:
            "https://mainnet.coinsdo.com/monitor/nodes/check?network=mainnet&id=1",
          targetUrl: "http://122.11.149.168:10001/eth-achavie",
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
          label: "Group Name",
          model: "groupName",
          type: "select",
          option: CRYPTO_CURRENCY_GROUP,
        },
        {
          label: "Get URL",
          model: "getUrl",
          type: "text",
        },
        {
          label: "Target URL",
          model: "targetUrl",
          type: "text",
        },
        // {
        //   label: "SSH Key",
        //   model: "sshKey",
        //   type: "textarea",
        // },
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
      this.$router.push("/settings/nodes/add");
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
      this.selectedRow = `${row.groupName} - ${row.name}`;
      this.disableDialogStatus = true;
    },
    enableRow(row) {
      this.selectedRow = `${row.groupName} - ${row.name}`;
      this.enableDialogStatus = true;
    },
    deleteRow(row) {
      this.selectedRow = `${row.groupName} - ${row.name}`;
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
