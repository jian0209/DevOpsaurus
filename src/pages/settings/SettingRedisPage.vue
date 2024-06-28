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
          name: "get",
          required: true,
          label: "Get",
          align: "left",
          field: (row) => row.get,
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
          host: "localhost",
          port: "6379",
          database: 0,
          get: "debug:trx_status",
          status: 1,
          createdAt: 1719553933000,
        },
      ],
    };
  },
  methods: {
    goToAddPage() {
      this.$router.push("/settings/redis/add");
    },
  },
});
</script>
