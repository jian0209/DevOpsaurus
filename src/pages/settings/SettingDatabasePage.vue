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
  name: "SettingDatabasePage",
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
          name: "table",
          required: true,
          label: "Table",
          align: "left",
          field: (row) => row.table,
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
          name: "production",
          host: "localhost",
          port: "3306",
          database: "coinsdo_deposit",
          table: "t_deposit_record",
          status: 1,
          createdAt: 1719553933000,
        },
      ],
    };
  },
});
</script>
