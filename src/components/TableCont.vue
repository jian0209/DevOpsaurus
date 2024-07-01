<template>
  <div class="table-cont">
    <q-table
      :rows="rows"
      :columns="columns"
      :row-key="rowKey"
      :loading="loading"
      :no-data-label="loading ? 'Loading...' : noDataLabel"
      :no-results-label="loading ? 'Loading...' : 'No data found'"
      loading-label="Loading..."
      card-class="table-data-cont"
      separator="cell"
      @row-click="rowClick"
    >
      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
            class="table-header"
          >
            {{ col.label }}
          </q-th>
        </q-tr>
      </template>
      <template v-slot:body-cell-operate="props">
        <q-td :props="props">
          <div class="q-gutter-sm">
            <UsualButton
              color="positive"
              label="Info"
              @action:click="infoRow(props.row)"
              style="width: 90px"
              outline
            />
            <UsualButton
              color="info"
              label="Edit"
              @action:click="editRow(props.row)"
              style="width: 90px"
            />
            <UsualButton
              v-if="props.row.status === 1"
              color="warning"
              label="Disable"
              @action:click="disableRow(props.row)"
              style="width: 90px"
            />
            <UsualButton
              v-if="props.row.status === 0"
              color="positive"
              label="Enable"
              @action:click="enableRow(props.row)"
              style="width: 90px"
            />
            <UsualButton
              color="negative"
              label="Remove"
              :outline="true"
              @action:click="deleteRow(props.row)"
              style="width: 90px"
            />
          </div>
        </q-td>
      </template>
      <template v-slot:body-cell-refresh="props">
        <q-td :props="props">
          <div class="q-gutter-sm">
            <UsualButton
              color="positive"
              label="Info"
              @action:click="infoRow(props.row)"
              style="width: 90px"
              outline
            />
            <UsualButton
              color="info"
              label="Refresh"
              @action:click="refreshRow(props.row)"
              style="width: 90px"
            />
          </div>
        </q-td>
      </template>
    </q-table>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import UsualButton from "./Button.vue";

export default defineComponent({
  name: "TableContainer",
  components: {
    UsualButton,
  },
  props: {
    rows: Array,
    columns: Array,
    loading: Boolean,
    rowKey: String,
    noDataLabel: String,
  },
  methods: {
    infoRow(row) {
      this.$emit("info:row", row);
    },
    editRow(row) {
      this.$emit("edit:row", row);
    },
    disableRow(row) {
      this.$emit("disable:row", row);
    },
    enableRow(row) {
      this.$emit("enable:row", row);
    },
    deleteRow(row) {
      this.$emit("delete:row", row);
    },
    refreshRow(row) {
      this.$emit("refresh:row", row);
    },
    rowClick(event, row, index) {
      this.$emit("click:row", row);
    },
  },
});
</script>
