<template>
  <div>
    <TitleContainer
      title="Command Page"
      subtitle="Execute Command (Click on Row to View Details)"
    />
    <TableContainer
      :rows="dummyData"
      :columns="columns"
      @click:row="infoRow"
      @refresh:row="refresh"
    />
    <DialogComponent
      isExecuteDialog
      title="Command Information Details"
      :subtitle="`${selectedRow.command}`"
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
import { generateColumn, generateSearchForm } from "src/utils/util.js";
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
      dummyData: [
        {
          id: 1,
          name: "Production",
          command:
            "curl -X POST -H 'Content-Type: application/json' -d '{data}' http://localhost:8080/api/{id}",
        },
        {
          id: 2,
          name: "Production Test",
          command: "curl http://localhost/api/v1/health",
        },
      ],
      executeFormList: ref({}),
      executeInput: ref([]),
      infoDialogStatus: ref(false),
      selectedRow: ref({}),
    };
  },
  methods: {
    initData() {
      this.columns = generateColumn(this.dummyData);
    },
    updateDialogStatus(status) {
      this.infoDialogStatus = status;
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
    refresh(row) {
      console.log(row);
    },
    executeData(data) {
      console.log(data);
    },
  },
  created() {
    this.initData();
  },
});
</script>
