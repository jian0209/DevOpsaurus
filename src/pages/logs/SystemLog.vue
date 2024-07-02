<template>
  <div>
    <TitleContainer
      :title="$t('logsPage.system.title')"
      :subtitle="$t('logsPage.system.subtitle')"
    />
    <TableContainer :rows="dummyData" :columns="columns" @click:row="infoRow" />
    <DialogComponent
      isInfoDialog
      :title="$t('logsPage.system.infoDialog.title')"
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
import { generateColumn, generateDialogDetails } from "src/utils/util.js";
import { ROLES } from "src/utils/constants.js";
import moment from "moment";

export default defineComponent({
  name: "SystemLog",
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
          username: "John Doe",
          role: 3,
          action: "Edit",
          source: "Redis",
          description: "Edit Redis Configuration ${name}",
          createdAt: 1719553933000,
        },
      ],
      infoDialogStatus: ref(false),
      selectedRow: ref({}),
    };
  },
  methods: {
    initData() {
      this.columns = generateColumn(this.dummyData, true, true);
    },
    updateDialogStatus(status) {
      this.infoDialogStatus = status;
    },
    infoRow(row) {
      const tempSelectedRow = generateDialogDetails(row);
      for (const key in tempSelectedRow) {
        this.selectedRow[tempSelectedRow[key].formattedKey] =
          tempSelectedRow[key].value;
      }
      this.selectedRow["Created At"] = moment(row.createdAt).format(
        "YYYY-MM-DD HH:mm:ss"
      );
      this.selectedRow["Role"] = ROLES[row.role];
      this.infoDialogStatus = true;
    },
  },
  created() {
    this.initData();
  },
});
</script>
