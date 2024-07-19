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
      isExecuteDialog
      :title="'Redis Information Details'"
      :subtitle="`${selectedRow.get}`"
      :dialogStatus="infoDialogStatus"
      :formListDetails="selectedRow"
      @update:dialogStatus="updateDialogStatus"
      :executeInput="executeInput"
      @execute:data="executeData"
      :executeFormList="executeFormList"
    />
    <DialogComponent
      isResultDialog
      title="Get Redis Result Details"
      :subtitle="`${resultTitle}`"
      :result="resultArr"
      :dialogStatus="resultDialogStatus"
      @update:dialogStatus="updateDialogStatus"
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
  replaceCommandString,
} from "src/utils/util.js";
import { getRedisList, getRedisResult } from "src/api/redis";

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
          // result: null,
        },
      ],
      infoDialogStatus: ref(false),
      resultDialogStatus: ref(false),
      selectedRow: ref({}),
      executeInput: ref([]),
      executeFormList: ref({}),
      resultTitle: ref(""),
      resultArr: ref([]),
    };
  },
  methods: {
    initData() {
      this.columns = generateColumn(this.rowData);
      this.getList();
    },
    updateDialogStatus(status) {
      this.infoDialogStatus = status;
      this.resultDialogStatus = status;
    },
    infoRow(row) {
      this.selectedRow = {
        ...row,
      };
      this.executeInput = generateSearchForm(this.selectedRow.get);
      this.executeInput.forEach((input) => {
        this.executeFormList[input.model] = null;
      });
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
        ...this.selectedRow,
      };

      submitData.get_key = replaceCommandString(submitData.get, data);
      console.log(submitData);

      this.$q.loading.show();
      await getRedisResult(submitData)
        .then((res) => {
          if (res.code !== 0) {
            this.$q.notify({
              message: this.$t(`api.${res.code || "unknown"}`),
              type: "negative",
            });
            return;
          }
          this.resultArr = [res.data.redis.result];
          if (this.resultArr[0] === "") {
            this.resultArr = ["No result returned."];
          }
          this.resultTitle = submitData.get_key;
          this.resultDialogStatus = true;
        })
        .finally(() => {
          this.$q.loading.hide();
          this.infoDialogStatus = false;
        });
    },
  },
  created() {
    this.initData();
  },
});
</script>
