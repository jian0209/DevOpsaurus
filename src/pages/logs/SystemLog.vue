<template>
  <div>
    <TitleContainer
      title="System Log"
      subtitle="View System Logs (Save Only 1 week logs)"
    />
    <TableContainer :rows="dummyData" :columns="columns" @click:row="infoRow" />
    <DialogComponent
      isInfoDialog
      title="User Login Information Details"
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
import { ROLES } from "src/utils/constants.js";
import { generateColumn } from "src/utils/util.js";
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
      for (const key in row) {
        this.selectedRow[key] = row[key];
      }
      this.selectedRow.createdAt = moment(row.createdAt).format(
        "YYYY-MM-DD HH:mm:ss"
      );
      this.selectedRow.role = ROLES[row.role];
      this.infoDialogStatus = true;
    },
  },
  created() {
    this.initData();
  },
});
</script>
