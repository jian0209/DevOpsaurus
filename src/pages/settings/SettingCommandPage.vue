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
      :rows="dummyData"
      :columns="columns"
      @edit:row="editRow($event)"
    />
    <DialogComponent
      title="Edit Command"
      :dialogStatus="editDialogStatus"
      :formList="formList"
      :formListDetails="formListDetails"
      isFormDialog
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
  name: "SettingCommandPage",
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
          name: "host",
          required: true,
          label: "Host",
          align: "left",
          field: (row) => row.host,
          format: (val) => `${val}`,
          sortable: true,
        },
        {
          name: "sshPort",
          required: true,
          label: "SSH Port",
          align: "left",
          field: (row) => row.sshPort,
          format: (val) => `${val}`,
          sortable: true,
        },
        {
          name: "command",
          required: true,
          label: "Command",
          align: "left",
          field: (row) => row.command,
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
          name: "production",
          host: "localhost",
          username: "root",
          sshPort: "3306",
          command: "curl http://localhost:8080/api/v1/health",
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
          label: "SSH Key",
          model: "sshKey",
          type: "textarea",
        },
        {
          label: "SSH Port",
          model: "sshPort",
          type: "text",
        },
        {
          label: "Command",
          model: "command",
          type: "text",
        },
      ],
      formListDetails: ref({}),
      editDialogStatus: ref(false),
    };
  },
  methods: {
    goToAddPage() {
      this.$router.push("/settings/command/add");
    },
    updateDialogStatus(status) {
      this.editDialogStatus = status;
    },
    editRow(row) {
      this.formListDetails = row;
      this.editDialogStatus = true;
    },
  },
});
</script>
