<template>
  <div>
    <TitleContainer
      title="Nodes Management"
      subtitle="Manage Nodes Connection"
    />
    <div class="button-cont">
      <UsualButton
        :label="$t('settingsPage.button.add', { name: 'Node Connection' })"
        color="info"
        icon="add_circle_outline"
        @action:click="goToAddPage"
      />
    </div>
    <TableContainer
      :rows="rowData"
      :columns="columns"
      @edit:row="editRow($event)"
      @disable:row="disableRow($event)"
      @enable:row="enableRow($event)"
      @delete:row="deleteRow($event)"
      @info:row="infoRow($event)"
    />
    <DialogComponent
      title="Edit Nodes"
      :dialogStatus="editDialogStatus"
      :formList="formList"
      :formListDetails="formListDetails"
      isFormDialog
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEdit"
    />
    <DialogComponent
      title="Enable Nodes"
      :dialogStatus="enableDialogStatus"
      :subtitle="`This Will Enable Nodes {${selectedRow}} Be Monitored`"
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEditStatus(1)"
    />
    <DialogComponent
      title="Disable Nodes"
      :dialogStatus="disableDialogStatus"
      :subtitle="`This Will Disable Nodes {${selectedRow}} Be Monitored`"
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEditStatus(0)"
    />
    <DialogComponent
      title="Delete Nodes"
      :dialogStatus="deleteDialogStatus"
      :subtitle="`This Will Delete Nodes Record {${selectedRow}}`"
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitDelete"
    />
    <DialogComponent
      isInfoDialog
      title="Nodes Information Details"
      :dialogStatus="infoDialogStatus"
      :formListDetails="selectedInfoRow"
      @update:dialogStatus="updateDialogStatus"
    />
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import TitleContainer from "src/components/TitleCont.vue";
import TableContainer from "src/components/TableCont.vue";
import UsualButton from "src/components/Button.vue";
import DialogComponent from "src/components/Dialog.vue";
import { CRYPTO_CURRENCY_GROUP, STATUS } from "src/utils/constants.js";
import { generateColumn } from "src/utils/util.js";
import moment from "moment";
import {
  getNodesList,
  editNode,
  editStatusNode,
  deleteNode,
} from "src/api/settings";
import "src/css/settingsScreen.scss";

export default defineComponent({
  name: "SettingNodesPage",
  components: {
    TitleContainer,
    TableContainer,
    UsualButton,
    DialogComponent,
  },
  data() {
    return {
      columns: ref([]),
      rowData: [
        {
          id: null,
          name: null,
          group_name: null,
          group_url: null,
          target_url: null,
          fetch_parameter: null,
          status: null,
          created_at: null,
        },
      ],
      formList: [
        {
          label: "Name",
          model: "name",
          type: "text",
          readonly: true,
        },
        {
          label: "Group Name",
          model: "group_name",
          type: "select",
          option: CRYPTO_CURRENCY_GROUP,
        },
        {
          label: "Group URL",
          model: "group_url",
          type: "text",
        },
        {
          label: "Target URL",
          model: "target_url",
          type: "text",
        },
        {
          label: "Fetch Parameter",
          model: "fetch_parameter",
          type: "text",
        },
      ],
      formListDetails: ref({}),
      editDialogStatus: ref(false),
      enableDialogStatus: ref(false),
      disableDialogStatus: ref(false),
      deleteDialogStatus: ref(false),
      infoDialogStatus: ref(false),
      selectedInfoRow: ref({}),
      selectedRow: ref(""),
    };
  },
  methods: {
    initData() {
      this.columns = generateColumn(this.rowData, false, true, true);
      this.getList();
    },
    goToAddPage() {
      this.$router.push("/settings/nodes/add");
    },
    updateDialogStatus(status) {
      this.editDialogStatus = status;
      this.enableDialogStatus = status;
      this.disableDialogStatus = status;
      this.deleteDialogStatus = status;
      this.infoDialogStatus = status;
    },
    editRow(row) {
      for (const key in row) {
        this.formListDetails[key] = row[key];
      }
      this.editDialogStatus = true;
    },
    disableRow(row) {
      this.selectedRow = row.name;
      this.disableDialogStatus = true;
    },
    enableRow(row) {
      this.selectedRow = row.name;
      this.enableDialogStatus = true;
    },
    deleteRow(row) {
      this.selectedRow = row.name;
      this.deleteDialogStatus = true;
    },
    infoRow(row) {
      this.selectedInfoRow = {
        Name: row.name,
        "Group Name": row.group_name,
        "Group URL": row.group_url,
        "Target URL": row.target_url,
        "Fetch Parameter": row.fetch_parameter,
        Status: STATUS[row.status],
        "Created At": moment(row.created_at).format("YYYY-MM-DD HH:mm:ss"),
      };
      this.infoDialogStatus = true;
    },
    async submitEdit(data) {
      this.$q.loading.show();
      data.group_name = data.group_name.value;
      await editNode(data)
        .then((res) => {
          if (res.code !== 0) {
            this.$q.notify({
              message: this.$t(`api.${res.code || "unknown"}`),
              type: "negative",
            });
            return;
          }
          this.$q.notify({
            message: `Edit "${data.name}" successfully!`,
            type: "positive",
          });
        })
        .finally(() => {
          this.getList();
          this.$q.loading.hide();
        });
    },
    async submitEditStatus(status) {
      this.$q.loading.show();
      const data = {
        name: this.selectedRow,
        status: status || 0,
      };
      await editStatusNode(data)
        .then((res) => {
          if (res.code !== 0) {
            this.$q.notify({
              message: this.$t(`api.${res.code || "unknown"}`),
              type: "negative",
            });
            return;
          }
          this.$q.notify({
            message: `${status ? "Enable" : "Disable"} "${
              this.selectedRow
            }" successfully!`,
            type: "positive",
          });
        })
        .finally(() => {
          this.getList();
          this.$q.loading.hide();
        });
    },
    async submitDelete() {
      this.$q.loading.show();
      const data = {
        name: this.selectedRow,
      };
      await deleteNode(data)
        .then((res) => {
          if (res.code !== 0) {
            this.$q.notify({
              message: this.$t(`api.${res.code || "unknown"}`),
              type: "negative",
            });
            return;
          }
          this.$q.notify({
            message: `Delete "${this.selectedRow}" successfully!`,
            type: "positive",
          });
        })
        .finally(() => {
          this.getList();
          this.$q.loading.hide();
        });
    },
    async getList() {
      this.$q.loading.show();
      await getNodesList()
        .then((res) => {
          console.log(res);
          if (res.code !== 0) {
            this.$q.notify({
              message: this.$t(`api.${res.code || "unknown"}`),
              type: "negative",
            });
            return;
          }

          if (!res.data || !Array.isArray(res.data.nodes)) {
            this.rowData = [];
            return;
          }

          if (res.data.nodes.length === 0) {
            this.rowData = [];
          } else {
            this.rowData = res.data.nodes;
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
