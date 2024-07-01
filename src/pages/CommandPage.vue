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
      title="Command Information Details"
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
          database: "coinsdo_deposit",
          table: "t_deposit_record",
          parameter: "id IN {ids} AND name = {name}",
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
      this.searchInput = generateSearchForm(this.selectedRow.parameter);
      this.searchInput.forEach((input) => {
        this.searchFormList[input.model] = null;
      });
      this.dialogColumns = generateColumn(this.dummyData);
      this.dialogRows = this.dummyData;
      this.infoDialogStatus = true;
    },
    refresh(row) {
      console.log(row);
    },
    searchData(data) {
      console.log(data);
    },
  },
  created() {
    this.initData();
  },
});
</script>
