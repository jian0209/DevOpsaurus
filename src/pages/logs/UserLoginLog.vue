<template>
  <div>
    <TitleContainer
      :title="$t('logsPage.userLogin.title')"
      :subtitle="$t('logsPage.userLogin.subtitle')"
    />
    <TableContainer
      :rows="rowData"
      :columns="columns"
      @click:row="infoRow"
      title="user-login-log"
    />
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
import { generateColumn, generateDialogDetails } from "src/utils/util.js";
import { getLogList } from "src/api/log.js";
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
      rowData: [
        {
          id: null,
          user_id: null,
          username: null,
          last_login_time: null,
          last_login_ip: null,
          user_agent: null,
          status: null,
          reason: null,
        },
      ],
      infoDialogStatus: ref(false),
      selectedRow: ref({}),
    };
  },
  methods: {
    initData() {
      this.columns = generateColumn(this.rowData, true);
      this.getList();
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
      this.selectedRow["Last Login Time"] = moment(row.lastLoginTime).format(
        "YYYY-MM-DD HH:mm:ss"
      );
      this.selectedRow["Status"] = LOG_STATUS[row.status];
      this.infoDialogStatus = true;
    },
    async getList() {
      this.$q.loading.show();
      await getLogList("user")
        .then((res) => {
          if (res.code !== 0) {
            if (res.code === 9001) {
              this.$q.notify({
                message: `${res.data.msg || "Unknown Error"}`,
                type: "negative",
              });
              return;
            }
            this.$q.notify({
              message: this.$t(`api.${res.code || "unknown"}`),
              type: "negative",
            });
            return;
          }

          if (!res.data || !Array.isArray(res.data.user_log)) {
            this.rowData = [];
            return;
          }

          if (res.data.user_log.length === 0) {
            this.rowData = [];
          } else {
            this.rowData = res.data.user_log;
          }
        })
        .finally(() => {
          this.$q.loading.hide();
        });
    },
  },
  created() {
    this.initData();
  },
});
</script>
