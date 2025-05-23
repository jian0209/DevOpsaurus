<template>
  <div class="table-cont">
    <div
      class="table-top-function-cont"
      :style="
        !$props.noSearch
          ? 'justify-content: space-between'
          : 'justify-content: flex-end'
      "
    >
      <div class="table-search-cont" v-if="!$props.noSearch">
        <q-input
          v-model="$props.searchValue['name']"
          type="text"
          class="table-search-input"
          color="secondary"
          placeholder="Name"
          dense
          outlined
          clearable
        />
        <q-btn
          color="secondary"
          icon-right="search"
          label="Search"
          no-caps
          :class="!$props.noSearch ? 'search-btn' : null"
          @click="searchData"
        />
      </div>
      <q-btn
        color="secondary"
        icon-right="archive"
        label="Export table"
        no-caps
        :class="!$props.noClass ? 'export-btn' : null"
        @click="exportTable"
      />
    </div>
    <q-table
      :rows="rows"
      :columns="columns"
      :row-key="rowKey"
      :loading="loading"
      :no-data-label="loading ? 'Loading...' : noDataLabel"
      :no-results-label="loading ? 'Loading...' : 'No data found'"
      loading-label="Loading..."
      :card-class="!$props.noClass ? 'table-data-cont' : null"
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
      <template v-slot:body-cell-info="props">
        <q-td :props="props">
          <div class="q-gutter-sm">
            <UsualButton
              color="positive"
              label="Info"
              @action:click="infoRow(props.row)"
              style="width: 90px"
              outline
            />
          </div>
        </q-td>
      </template>
      <template v-slot:body-cell-operate="props">
        <q-td :props="props">
          <div class="q-gutter-sm">
            <UsualButton
              v-if="props.row.is_favourite === 0"
              color="positive"
              label="Star"
              @action:click="favouriteRow(props.row)"
              style="width: 90px"
              outline
            />
            <UsualButton
              v-if="props.row.is_favourite === 1"
              color="accent"
              label="Star"
              @action:click="unFavouriteRow(props.row)"
              style="width: 90px"
              outline
            />
            <UsualButton
              color="info"
              label="Clone"
              @action:click="cloneRow(props.row)"
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
import { wrapCsvValue } from "src/utils/util";
import { exportFile } from "quasar";
import moment from "moment";

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
    noClass: Boolean,
    noSearch: Boolean,
    searchValue: Object,
    title: String,
  },
  methods: {
    infoRow(row) {
      this.$emit("info:row", row);
    },
    cloneRow(row) {
      this.$emit("clone:row", row);
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
    favouriteRow(row) {
      this.$emit("favourite:row", row);
    },
    unFavouriteRow(row) {
      this.$emit("unFavourite:row", row);
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
    searchData() {
      this.$emit("search:data", this.searchValue);
    },
    exportTable() {
      const content = [this.columns.map((col) => wrapCsvValue(col.label))]
        .concat(
          this.rows.map((row) =>
            this.columns
              .map((col) =>
                wrapCsvValue(
                  typeof col.field === "function"
                    ? col.field(row)
                    : row[col.field === void 0 ? col.name : col.field],
                  col.format,
                  row
                )
              )
              .join(",")
          )
        )
        .join("\r\n");

      const status = exportFile(
        `${this.title || "table"}-export-${moment(moment.now()).format(
          "YYYY-MM-DD_HH-mm-ss"
        )}.csv`,
        content,
        "text/csv"
      );

      if (status !== true) {
        $q.notify({
          message: "Browser denied file download...",
          color: "negative",
          icon: "warning",
        });
      }
    },
  },
});
</script>
