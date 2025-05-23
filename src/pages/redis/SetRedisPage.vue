<template>
  <div>
    <TitleContainer title="Redis Page" :subtitle="'Set Redis Value'" />
    <TableContainer
      :rows="rowData"
      :columns="columns"
      @click:row="infoRow"
      :searchValue="searchValue"
      @search:data="searchData"
      title="redis-set"
    />
    <DialogComponent
      isExecuteDialog
      :title="'Redis Information Details'"
      executeBtnTxt="Set"
      :subtitle="`Name: ${selectedRow.name} | Get: ${selectedRow.get}`"
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
import {
  generateColumn,
  generateModifyForm,
  generateSearchForm,
  replaceCommandString,
} from "src/utils/util.js";
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
          // result: null,
        },
      ],
      executeInput: ref([]),
      executeFormList: ref({ value: null }),
      infoDialogStatus: ref(false),
      selectedRow: ref({}),
      searchValue: ref({ name: null }),
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
      this.executeInput = [
        ...generateSearchForm(this.selectedRow.get),
        generateModifyForm(),
      ];
      this.infoDialogStatus = true;
    },
    async getList(searchData) {
      const submitData = { name: null };
      if (searchData && searchData.name) {
        submitData.name = searchData.name;
      }
      this.$q.loading.show();
      await getRedisList(submitData)
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
        get_key: replaceCommandString(this.selectedRow.get, data),
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
    searchData(data) {
      this.getList(data);
    },
  },
  created() {
    this.initData();
  },
});
</script>
