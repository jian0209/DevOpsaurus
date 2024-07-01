<template>
  <div>
    <TitleContainer
      title="User Login Log"
      subtitle="View User Logged In (Save Only 1 week logs)"
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
import { LOG_STATUS } from "src/utils/constants.js";
import { generateColumn } from "src/utils/util.js";
import moment from "moment";

export default defineComponent({
  name: "UserLoginLog",
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
          userId: 1,
          username: "John Doe",
          lastLoginTime: 1719553933000,
          lastLoginIp: "47.241.105.101",
          userAgent:
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
          status: 1,
          reason: "Success",
        },
      ],
      infoDialogStatus: ref(false),
      selectedRow: ref({}),
    };
  },
  methods: {
    initData() {
      this.columns = generateColumn(this.dummyData, true);
    },
    updateDialogStatus(status) {
      this.infoDialogStatus = status;
    },
    infoRow(row) {
      for (const key in row) {
        this.selectedRow[key] = row[key];
      }
      this.selectedRow.lastLoginTime = moment(row.lastLoginTime).format(
        "YYYY-MM-DD HH:mm:ss"
      );
      this.selectedRow.status = LOG_STATUS[row.status];
      this.infoDialogStatus = true;
    },
  },
  created() {
    this.initData();
  },
});
</script>
