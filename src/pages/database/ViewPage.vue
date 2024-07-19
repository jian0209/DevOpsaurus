<template>
  <div>
    <TitleContainer
      :title="$t('databasePage.view.title')"
      :subtitle="$t('databasePage.view.subtitle')"
    />
    <TableContainer
      :rows="rowData"
      :columns="columns"
      @click:row="infoRow"
      title="database-view"
    />
    <DialogComponent
      isTableDialog
      :title="$t('databasePage.view.dialog.title')"
      :subtitle="`SELECT ${selectedRow.select} FROM ${selectedRow.table}`"
      :dialogStatus="infoDialogStatus"
      :formListDetails="selectedRow"
      @update:dialogStatus="updateDialogStatus"
      :dialogRows="dialogRows"
      :dialogColumns="dialogColumns"
      :searchInput="searchInput"
      :searchFormList="searchFormList"
      @search:data="searchData"
    />
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import TitleContainer from "src/components/TitleCont.vue";
import TableContainer from "src/components/TableCont.vue";
import DialogComponent from "src/components/Dialog.vue";
import {
  generateColumn,
  generateSearchForm,
  replaceQueryString,
} from "src/utils/util.js";
import { getDatabaseList, executeQueryToGetData } from "src/api/database";

export default defineComponent({
  name: "DatabaseViewPage",
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
          name: null,
          database: null,
          table: null,
          select: null,
          parameter: null,
        },
      ],
      searchFormList: ref({}),
      searchInput: ref([]),
      infoDialogStatus: ref(false),
      selectedRow: ref({}),
      dialogRows: ref([]),
      dialogColumns: ref([]),
    };
  },
  methods: {
    initData() {
      this.columns = generateColumn(this.rowData);
      this.getList();
    },
    updateDialogStatus(status) {
      this.infoDialogStatus = status;
      this.dialogColumns = [];
      this.dialogRows = [];
    },
    infoRow(row) {
      this.selectedRow = { ...row };
      this.searchInput = generateSearchForm(this.selectedRow.parameter);
      this.searchInput.forEach((input) => {
        this.searchFormList[input.model] = null;
      });
      this.infoDialogStatus = true;
    },
    async searchData(data) {
      this.$q.loading.show();
      let select = "";
      let parameter = "";
      let query = "";
      if (
        !this.selectedRow.select ||
        this.selectedRow.select === "" ||
        this.selectedRow.select === "None"
      ) {
        select = "*";
      } else {
        select = this.selectedRow.select;
      }

      if (
        !this.selectedRow.parameter ||
        this.selectedRow.parameter === "" ||
        this.selectedRow.parameter === "None"
      ) {
        parameter = "";
      } else {
        parameter = `WHERE ${replaceQueryString(
          this.selectedRow.parameter,
          data
        )}`;
      }
      query = `SELECT ${select} FROM ${this.selectedRow.database}.${this.selectedRow.table} ${parameter}`;

      const submitData = {
        database_id: this.selectedRow.id,
        query: query,
      };

      await executeQueryToGetData(submitData)
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

          const columns = [{}];
          res.data.columns.forEach((column) => {
            columns[0][column] = null;
          });

          this.dialogColumns = generateColumn(
            columns,
            false,
            false,
            false,
            false,
            true
          );

          if (!res.data || !Array.isArray(res.data.result)) {
            this.dialogRows = [];
            return;
          }

          if (res.data.result.length === 0) {
            this.dialogRows = [];
          } else {
            this.dialogRows = res.data.result;
          }

          this.$q.notify({
            message: "Data Searched Successfully!",
            type: "positive",
          });
        })
        .finally(() => {
          this.$q.loading.hide();
        });
      // this.dialogRows.push({
      //   id: this.dialogRows.length + 1,
      //   name: data.name,
      //   database: data.database,
      //   table: data.table,
      //   parameter: data.parameter,
      // });
    },
    async getList() {
      this.$q.loading.show();
      await getDatabaseList()
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

          if (!res.data || !Array.isArray(res.data.databases)) {
            this.rowData = [];
            return;
          }

          if (res.data.databases.length === 0) {
            this.rowData = [];
          } else {
            this.rowData = res.data.databases;
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
