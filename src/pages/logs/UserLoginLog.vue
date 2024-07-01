<template>
  <div>
    <TitleContainer
      :title="$t('logsPage.userLogin.title')"
      :subtitle="$t('logsPage.userLogin.subtitle')"
    />
    <TableContainer :rows="dummyData" :columns="columns" @click:row="infoRow" />
    <DialogComponent
      isInfoDialog
      :title="$t('logsPage.userLogin.infoDialog.title')"
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
import { formatObjectToTitleCase } from "src/utils/helper.js";
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
      const tempSelectedRow = formatObjectToTitleCase(row);
      for (const key in tempSelectedRow) {
        this.selectedRow[tempSelectedRow[key].formattedKey] =
          tempSelectedRow[key].value;
      }
      this.selectedRow["Last Login Time"] = moment(row.lastLoginTime).format(
        "YYYY-MM-DD HH:mm:ss"
      );
      this.selectedRow["Status"] = LOG_STATUS[row.status];
      this.infoDialogStatus = true;
    },
  },
  created() {
    this.initData();
  },
});
</script>
