<template>
  <div>
    <TitleContainer
      :title="$t('logsPage.system.title')"
      :subtitle="$t('logsPage.system.subtitle')"
    />
    <TableContainer
      :rows="rowData"
      :columns="columns"
      @click:row="infoRow"
      title="system-log"
    />
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
import { getLogList } from "src/api/log.js";
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
      rowData: [
        {
          id: null,
          username: null,
          role: null,
          action: null,
          source: null,
          description: null,
          created_at: null,
        },
      ],
      infoDialogStatus: ref(false),
      selectedRow: ref({}),
    };
  },
  methods: {
    initData() {
      this.columns = generateColumn(this.rowData, true, true);
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
      this.selectedRow["Created At"] = moment(row.createdAt).format(
        "YYYY-MM-DD HH:mm:ss"
      );
      this.selectedRow["Role"] = ROLES[row.role];
      this.infoDialogStatus = true;
    },
    async getList() {
      this.$q.loading.show();
      await getLogList("system")
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

          if (!res.data || !Array.isArray(res.data.system_log)) {
            this.rowData = [];
            return;
          }

          if (res.data.system_log.length === 0) {
            this.rowData = [];
          } else {
            this.rowData = res.data.system_log;
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
