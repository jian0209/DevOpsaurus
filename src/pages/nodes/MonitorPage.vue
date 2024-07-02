<template>
  <div>
    <TitleContainer
      :title="$t('nodesPage.monitor.title')"
      :subtitle="$t('nodesPage.monitor.subtitle')"
    />
    <TableContainer
      :rows="dummyData"
      :columns="columns"
      @info:row="infoRow"
      @refresh:row="refresh"
    />
    <DialogComponent
      isInfoDialog
      title="Node Information Details"
      :dialogStatus="infoDialogStatus"
      :formListDetails="selectedRow"
      @update:dialogStatus="updateDialogStatus"
    />
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import TitleContainer from "src/components/TitleCont.vue";
import TableContainer from "src/components/TableCont.vue";
import DialogComponent from "src/components/Dialog.vue";
import { generateColumn } from "src/utils/util.js";
import moment from "moment";

export default defineComponent({
  name: "NodesMonitorPage",
  components: {
    TitleContainer,
    TableContainer,
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
          target: 123456,
          timeFetch: 1719553933000,
        },
      ],
      infoDialogStatus: ref(false),
      selectedRow: ref({}),
    };
  },
  methods: {
    initData() {
      this.columns = generateColumn(this.dummyData, false, false, false, true);
    },
    updateDialogStatus(status) {
      this.infoDialogStatus = status;
    },
    infoRow(row) {
      for (const key in row) {
        const keyName = this.$t(`table.column.${key}`);
        this.selectedRow[keyName] = row[key];
      }
      this.selectedRow["Time Fetch"] = moment(row.timeFetch).format(
        "YYYY-MM-DD HH:mm:ss"
      );
      this.infoDialogStatus = true;
    },
    refresh(row) {
      console.log(row);
      this.$q.notify({
        message: `Refresh ${row.name} successfully!`,
        type: "positive",
      });
      this.dummyData = this.dummyData.map((item) => {
        if (item.id === row.id) {
          item.timeFetch = Date.now();
        }
        return item;
      });
    },
  },
  created() {
    this.initData();
  },
});
</script>
