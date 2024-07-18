<template>
  <div>
    <TitleContainer
      :title="$t('upsPage.title')"
      :subtitle="$t('upsPage.subtitle')"
    />
    <TableContainer
      :rows="dummyData"
      :columns="columns"
      @click:row="infoRow"
      title="ups"
    />
    <DialogComponent
      isInfoDialog
      :title="$t('upsPage.viewDialog.title')"
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
  name: "UpsMonitorPage",
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
          name: "Tung Ann UPS",
          ups_bat: "value",
          ups_log: 123,
          ups_asd: true,
          key_key: "value",
          timeFetch: 1719553933000,
        },
      ],
      infoDialogStatus: ref(false),
      selectedRow: ref({}),
    };
  },
  methods: {
    initData() {
      this.columns = generateColumn(this.dummyData);
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
  },
  created() {
    this.initData();
  },
});
</script>
