<template>
  <div>
    <TitleContainer title="Redis Page" :subtitle="'Set Redis Value'" />
    <TableContainer :rows="rowData" :columns="columns" @click:row="infoRow" title="redis-set" />
    <DialogComponent
      isExecuteDialog
      :title="'Redis Information Details'"
      executeBtnTxt="Set"
      :subtitle="`Name: ${selectedRow.name} | Get: ${selectedRow.get} | Result: ${selectedRow.result}`"
      :dialogStatus="infoDialogStatus"
      :formListDetails="selectedRow"
      @update:dialogStatus="updateDialogStatus"
      :executeInput="executeInput"
      @execute:data="executeData"
      :executeFormList="executeFormList"
    />
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import TitleContainer from "src/components/TitleCont.vue";
import TableContainer from "src/components/TableCont.vue";
import DialogComponent from "src/components/Dialog.vue";
import { generateColumn, generateModifyForm } from "src/utils/util.js";
import { getRedisList, setRedisValue } from "src/api/redis";

export default defineComponent({
  name: "SetRedisPage",
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
      executeInput: ref([]),
      executeFormList: ref({ value: null }),
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
      this.executeFormList = { value: null };
    },
    infoRow(row) {
      this.selectedRow = { ...row };
      this.executeInput = [generateModifyForm()];
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
    async executeData(data) {
      const submitData = {
        id: this.selectedRow.id,
        value: data.value,
      };

      this.$q.loading.show();
      await setRedisValue(submitData)
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
          this.$q.notify({
            message: "Set Redis Value Success",
            type: "positive",
          });
          this.getList();
        })
        .finally(() => {
          this.$q.loading.hide();
          this.executeFormList = { value: null };
          this.infoDialogStatus = false;
        });
    },
  },
  created() {
    this.initData();
  },
});
</script>
