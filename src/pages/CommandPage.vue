<template>
  <div>
    <TitleContainer
      :title="$t('commandPage.title')"
      :subtitle="$t('commandPage.subtitle')"
    />
    <TableContainer :rows="rowData" :columns="columns" @click:row="infoRow" />
    <DialogComponent
      isExecuteDialog
      :title="$t('commandPage.executeDialog.title')"
      :subtitle="`${selectedRow.command}`"
      :dialogStatus="infoDialogStatus"
      :formListDetails="selectedRow"
      @update:dialogStatus="updateDialogStatus"
      :executeInput="executeInput"
      @execute:data="executeData"
      :executeFormList="executeFormList"
    />
    <DialogComponent
      isResultDialog
      title="Command Result Details"
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
import { getCommandList, executeCommand } from "src/api/command.js";
import moment from "moment";

export default defineComponent({
  name: "CommandPage",
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
          host: null,
          command: null,
        },
      ],
      executeFormList: ref({}),
      executeInput: ref([]),
      infoDialogStatus: ref(false),
      resultDialogStatus: ref(false),
      selectedRow: ref({}),
      resultArr: ref([]),
      resultTitle: ref(""),
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
      for (const key in row) {
        this.selectedRow[key] = row[key];
      }
      this.selectedRow.timeFetch = moment(row.timeFetch).format(
        "YYYY-MM-DD HH:mm:ss"
      );
      this.executeInput = generateSearchForm(this.selectedRow.command);
      this.executeInput.forEach((input) => {
        this.executeFormList[input.model] = null;
      });
      this.infoDialogStatus = true;
    },
    async executeData(data) {
      const submitData = {
        ...this.selectedRow,
      };

      submitData.command = replaceCommandString(submitData.command, data);

      this.$q.loading.show();
      await executeCommand(submitData)
        .then((res) => {
          if (res.code !== 0) {
            this.$q.notify({
              message: this.$t(`api.${res.code || "unknown"}`),
              type: "negative",
            });
            return;
          }
          this.$q.notify({
            message: this.$t("dialog.executeSuccess", {
              command: this.selectedRow.name,
            }),
            type: "positive",
          });
          if (res.data.output.length > 1 || res.data.output[0] !== "") {
            this.resultArr = res.data.output;
          } else {
            this.resultArr = res.data.error;
          }
          if (this.resultArr[0] === "") {
            this.resultArr = ["No result returned."];
          }
          this.resultTitle = res.data.command;
          this.resultDialogStatus = true;
        })
        .finally(() => {
          this.$q.loading.hide();
          this.infoDialogStatus = false;
        });
    },
    async getList() {
      this.$q.loading.show();
      await getCommandList()
        .then((res) => {
          if (res.code !== 0) {
            this.$q.notify({
              message: this.$t(`api.${res.code || "unknown"}`),
              type: "negative",
            });
            return;
          }

          if (!res.data || !Array.isArray(res.data.commands)) {
            this.rowData = [];
            return;
          }

          if (res.data.commands.length === 0) {
            this.rowData = [];
          } else {
            this.rowData = res.data.commands;
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
