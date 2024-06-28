<template>
  <div>
    <TitleContainer title="UPS Management" subtitle="Manage UPS Connection" />
    <div class="button-cont">
      <UsualButton
        label="Add UPS Connection"
        color="info"
        icon="add_circle_outline"
      />
    </div>
    <TableContainer :rows="dummyData" :columns="columns" />
  </div>
</template>

<script>
import { defineComponent } from "vue";
import TitleContainer from "src/components/TitleCont.vue";
import TableContainer from "src/components/TableCont.vue";
import UsualButton from "src/components/Button.vue";
import { STATUS } from "src/utils/constants.js";
import moment from "moment";
import "src/css/settingsScreen.scss";

export default defineComponent({
  name: "SettingRedisPage",
  components: {
    TitleContainer,
    TableContainer,
    UsualButton,
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
          status: 1,
          createdAt: 1719553933000,
        },
      ],
    };
  },
});
</script>
