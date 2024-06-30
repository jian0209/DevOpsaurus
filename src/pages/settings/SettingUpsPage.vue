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
    />
    <DialogComponent
      title="Edit UPS"
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
          name: "name",
          required: true,
          label: "Name",
          align: "left",
          field: (row) => row.name,
          format: (val) => `${val}`,
          sortable: true,
        },
        {
          name: "ipAddr",
          required: true,
          label: "IP Address",
          align: "left",
          field: (row) => row.ipAddr,
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
          name: "location",
          required: true,
          label: "Location",
          align: "left",
          field: (row) => row.location,
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
        },
      ],
      formListDetails: ref({}),
      editDialogStatus: ref(false),
    };
  },
  methods: {
    goToAddPage() {
      this.$router.push("/settings/ups/add");
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
