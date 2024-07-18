<template>
  <div>
    <TitleContainer title="Redis Page" :subtitle="'Get Redis Result'" />
    <TableContainer
      :rows="rowData"
      :columns="columns"
      @click:row="infoRow"
      title="get-redis"
    />
    <DialogComponent
      isInfoDialog
      :title="'Redis Information Details'"
      :subtitle="`${selectedRow.command}`"
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
import { getRedisList } from "src/api/redis";

export default defineComponent({
  name: "GetRedisPage",
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
          get: null,
          result: null,
        },
      ],
      infoDialogStatus: ref(false),
      selectedRow: ref({}),
    };
  },
  methods: {
    initData() {
      this.columns = generateColumn(this.rowData);
      this.getList();
    },
    updateDialogStatus(status) {
      this.infoDialogStatus = status;
    },
    infoRow(row) {
      this.selectedRow = {
        Id: row.id,
        Name: row.name,
        Get: row.get,
        Result: row.result,
      };
      this.infoDialogStatus = true;
    },
    async getList() {
      this.$q.loading.show();
      await getRedisList()
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

          if (!res.data || !Array.isArray(res.data.redis)) {
            this.rowData = [];
            return;
          }

          if (res.data.redis.length === 0) {
            this.rowData = [];
          } else {
            this.rowData = res.data.redis;
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
