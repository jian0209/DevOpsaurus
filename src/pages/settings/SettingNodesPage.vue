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
  name: "SettingNodesPage",
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
          name: "groupName",
          required: true,
          label: "Group Name",
          align: "left",
          field: (row) => row.groupName,
          format: (val) => `${val}`,
          sortable: true,
        },
        {
          name: "url",
          required: true,
          label: "URL",
          align: "left",
          field: (row) => row.url,
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
          url: "http://203.117.22.213:10001/eth-achavie",
          status: 1,
          createdAt: 1719553933000,
        },
        {
          id: 2,
          name: "ETH - International Plaza",
          groupName: "ETH",
          url: "http://122.11.149.168:10001/eth-achavie",
          status: 1,
          createdAt: 1719553933000,
        },
      ],
    };
  },
});
</script>
