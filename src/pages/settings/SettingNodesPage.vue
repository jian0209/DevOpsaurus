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
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import TitleContainer from "src/components/TitleCont.vue";
import TableContainer from "src/components/TableCont.vue";
import UsualButton from "src/components/Button.vue";
import DialogComponent from "src/components/Dialog.vue";
import { STATUS, CRYPTO_CURRENCY_GROUP } from "src/utils/constants.js";
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
          label: "Name",
          align: "left",
          field: (row) => row.name,
          format: (val) => `${val}`,
          sortable: true,
        },
        {
          name: "groupName",
          required: true,
          label: "Group Name",
          align: "left",
          field: (row) => row.groupName,
          format: (val) => `${val.label || val}`,
          sortable: true,
        },
        {
          name: "getUrl",
          required: true,
          label: "Get URL",
          align: "left",
          field: (row) => row.getUrl,
          format: (val) => `${val}`,
          sortable: true,
        },
        {
          name: "targetUrl",
          required: true,
          label: "Target URL",
          align: "left",
          field: (row) => row.targetUrl,
          format: (val) => `${val}`,
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
      selectedRow: ref(""),
    };
  },
  methods: {
    goToAddPage() {
      this.$router.push("/settings/nodes/add");
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
  },
});
</script>
