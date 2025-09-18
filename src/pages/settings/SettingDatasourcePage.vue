<template>
  <div>
    <TitleContainer
      :title="$t('settingsPage.datasource.title')"
      :subtitle="$t('settingsPage.datasource.subtitle')"
    />
    <div class="button-cont">
      <UsualButton
        :label="$t('settingsPage.button.add', { name: 'Datasource' })"
        color="info"
        icon="add_circle_outline"
        @action:click="goToAddPage"
      />
    </div>
    <TableContainer
      :rows="rowData"
      :columns="columns"
      @edit:row="editRow($event)"
      @clone:row="cloneRow($event)"
      @disable:row="disableRow($event)"
      @enable:row="enableRow($event)"
      @delete:row="deleteRow($event)"
      @info:row="infoRow($event)"
      :searchValue="searchValue"
      @search:data="searchData"
      title="setting-datasource"
    />
    <DialogComponent
      :title="$t('settingsPage.dialog.edit.title', { name: 'Datasource' })"
      :dialogStatus="editDialogStatus"
      :formList="formList"
      :formListDetails="formListDetails"
      :testBtnTxt="$t('settingsPage.datasource.test')"
      isFormDialog
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEdit"
      @test:connection="getTablesForOption"
    />
    <DialogComponent
      :title="$t('settingsPage.dialog.enable.title', { name: 'Datasource' })"
      :dialogStatus="enableDialogStatus"
      :subtitle="
        $t('settingsPage.dialog.enable.subtitle', {
          name: 'Datasource',
          target: selectedRow,
        })
      "
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEditStatus(1)"
    />
    <DialogComponent
      :title="$t('settingsPage.dialog.disable.title', { name: 'Datasource' })"
      :dialogStatus="disableDialogStatus"
      :subtitle="
        $t('settingsPage.dialog.disable.subtitle', {
          name: 'Datasource',
          target: selectedRow,
        })
      "
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEditStatus(0)"
    />
    <DialogComponent
      :title="$t('settingsPage.dialog.remove.title', { name: 'Datasource' })"
      :dialogStatus="deleteDialogStatus"
      :subtitle="
        $t('settingsPage.dialog.remove.subtitle', {
          name: 'Datasource',
          target: selectedRow,
        })
      "
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitDelete"
    />
    <DialogComponent
      isInfoDialog
      :title="$t('settingsPage.dialog.info.title', { name: 'Datasource' })"
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
import { STATUS } from "src/utils/constants.js";
import { generateColumn } from "src/utils/util.js";
import AESCipher from "src/utils/crypto";
import moment from "moment";
import {
  getDatabaseList,
  editDatabase,
  editStatusDatabase,
  deleteDatabase,
  getDatabases,
  getTables,
} from "src/api/settings";
import { useQuasar } from "quasar";
import "src/css/settingsScreen.scss";
import { useI18n } from "vue-i18n";

export default defineComponent({
  name: "SettingDatasourcePage",
  components: {
    TitleContainer,
    TableContainer,
    UsualButton,
    DialogComponent,
  },
  setup() {
    const $q = useQuasar();
    const { t } = useI18n();
    const crypto = new AESCipher();
    const formList = ref([
      {
        label: "Name",
        model: "name",
        type: "text",
        readonly: true,
      },
      {
        label: "Host",
        model: "host",
        type: "text",
      },
      {
        label: "Port",
        model: "port",
        type: "text",
        placeholder: "Default: 3306",
      },
    ]);
    const datasourceDetails = ref({
      name: null,
      host: null,
      port: null,
    });
    return {
      formList,
      datasourceDetails,
      crypto,
    };
  },
  data() {
    return {
      columns: ref([]),
      rowData: ref([
        {
          id: null,
          name: null,
          host: null,
          port: null,
          status: null,
          created_at: null,
        },
      ]),
      formListDetails: ref({}),
      editDialogStatus: ref(false),
      enableDialogStatus: ref(false),
      disableDialogStatus: ref(false),
      deleteDialogStatus: ref(false),
      infoDialogStatus: ref(false),
      selectedInfoRow: ref({}),
      selectedRow: ref(""),
      searchValue: ref({ name: null }),
    };
  },
  methods: {
    initData() {
      this.columns = generateColumn(
        this.rowData,
        false,
        true,
        true,
        false,
        false,
        true
      );
      this.getList();
    },
    goToAddPage() {
      this.$router.push("/settings/datasource/add");
    },
    updateDialogStatus(status) {
      this.editDialogStatus = status;
      this.enableDialogStatus = status;
      this.disableDialogStatus = status;
      this.deleteDialogStatus = status;
      this.infoDialogStatus = status;
    },
    editRow(row) {
      this.formListDetails = { ...row };
      this.editDialogStatus = true;
    },
    cloneRow(row) {
      const rowString = btoa(
        JSON.stringify({
          host: row.host,
          port: row.port,
          username: row.username,
          password: row.password,
        })
      );
      const encryptedString = this.$CryptoJS.AES.encrypt(
        rowString,
        process.env.ENCRYPT_KEY
      );
      this.$router.push({
        path: "/settings/database/add",
        query: {
          isClone: true,
          passedData: encryptedString.toString(),
        },
      });
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
        Host: row.host,
        Port: row.port,
        Status: STATUS[row.status],
        "Created At": moment(row.created_at).format("YYYY-MM-DD HH:mm:ss"),
      };
      this.infoDialogStatus = true;
    },
    async submitEdit(data) {
      this.$q.loading.show();
      data.database = data.database.value || data.database;
      data.table = data.table.value || data.table;
      data.password = this.crypto.encrypt(data.password);
      await editDatabase(data)
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
      await editStatusDatabase(data)
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
      await deleteDatabase(data)
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
            message: `Delete "${this.selectedRow}" successfully!`,
            type: "positive",
          });
        })
        .finally(() => {
          this.getList();
          this.$q.loading.hide();
        });
    },
    async getList(searchData) {
      const submitData = { name: null };
      if (searchData && searchData.name) {
        submitData.name = searchData.name;
      }
      this.$q.loading.show();
      await getDatabaseList(submitData)
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

          if (!res.data || !Array.isArray(res.data.databases)) {
            this.rowData = [];
            return;
          }

          if (res.data.databases.length === 0) {
            this.rowData = [];
          } else {
            this.rowData = res.data.databases;
          }

          for (const row of this.rowData) {
            row.password = this.crypto.decrypt(row.password);
          }
        })
        .finally(() => {
          this.$q.loading.hide();
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
