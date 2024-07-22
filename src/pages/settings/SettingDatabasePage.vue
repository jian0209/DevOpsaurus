<template>
  <div>
    <TitleContainer
      :title="$t('settingsPage.database.title')"
      :subtitle="$t('settingsPage.database.subtitle')"
    />
    <div class="button-cont">
      <UsualButton
        :label="$t('settingsPage.button.add', { name: 'Database Connection' })"
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
      title="setting-database"
    />
    <DialogComponent
      :title="$t('settingsPage.dialog.edit.title', { name: 'Database' })"
      :dialogStatus="editDialogStatus"
      :formList="formList"
      :formListDetails="formListDetails"
      :testBtnTxt="$t('settingsPage.database.test')"
      isFormDialog
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEdit"
      @test:connection="getTablesForOption"
    />
    <DialogComponent
      :title="$t('settingsPage.dialog.enable.title', { name: 'Database' })"
      :dialogStatus="enableDialogStatus"
      :subtitle="
        $t('settingsPage.dialog.enable.subtitle', {
          name: 'Database',
          target: selectedRow,
        })
      "
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEditStatus(1)"
    />
    <DialogComponent
      :title="$t('settingsPage.dialog.disable.title', { name: 'Database' })"
      :dialogStatus="disableDialogStatus"
      :subtitle="
        $t('settingsPage.dialog.disable.subtitle', {
          name: 'Database',
          target: selectedRow,
        })
      "
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEditStatus(0)"
    />
    <DialogComponent
      :title="$t('settingsPage.dialog.remove.title', { name: 'Database' })"
      :dialogStatus="deleteDialogStatus"
      :subtitle="
        $t('settingsPage.dialog.remove.subtitle', {
          name: 'Database',
          target: selectedRow,
        })
      "
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitDelete"
    />
    <DialogComponent
      isInfoDialog
      :title="$t('settingsPage.dialog.info.title', { name: 'Database' })"
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
  name: "SettingDatabasePage",
  components: {
    TitleContainer,
    TableContainer,
    UsualButton,
    DialogComponent,
  },
  setup() {
    const $q = useQuasar();
    const { t } = useI18n();
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
      {
        label: "Username",
        model: "username",
        type: "text",
      },
      {
        label: "Password",
        model: "password",
        type: "text",
      },
      {
        label: "Database",
        model: "database",
        type: "select",
        option: [],
      },
      {
        label: "Table",
        model: "table",
        type: "select",
        option: [],
      },
      {
        label: "SELECT",
        model: "select",
        type: "textarea",
        placeholder: "username, email, phone",
        hint: "* Use comma to separate columns, '*' for all columns",
      },
      {
        label: "Parameter (WHERE)",
        model: "parameter",
        type: "textarea",
        placeholder: "id IN {ids} AND / OR name = {name}",
        hint: "* Eg: id IN {variable1} AND name IN {variable2}",
      },
    ]);
    const databaseDetails = ref({
      name: null,
      host: null,
      port: null,
      username: null,
      password: null,
      database: null,
      table: null,
      select: null,
      parameter: null,
    });

    const getTablesForOption = async (row) => {
      $q.loading.show();
      const data = { ...row };
      data.database = row.database.value || data.database;
      await getTables(data)
        .then((res) => {
          formList.value[6].option = [];
          if (res.code !== 0) {
            if (res.code === 9001) {
              this.$q.notify({
                message: `${res.data.msg || "Unknown Error"}`,
                type: "negative",
              });
              return;
            }
            $q.notify({
              message: t(`api.${res.code}`),
              type: "negative",
            });
            return;
          }

          for (const table of res.data.tables) {
            formList.value[6].option.push({
              label: table,
              value: table,
            });
          }
        })
        .finally(() => {
          $q.loading.hide();
        });
    };

    const getDatabasesForOption = async (data) => {
      // get databases
      $q.loading.show();
      await getDatabases(data)
        .then((res) => {
          formList.value[5].option = [];
          if (res.code !== 0) {
            if (res.code === 9001) {
              this.$q.notify({
                message: `${res.data.msg || "Unknown Error"}`,
                type: "negative",
              });
              return;
            }
            $q.notify({
              message: t(`api.${res.code}`),
              type: "negative",
            });
            return;
          }

          for (const db of res.data.databases) {
            formList.value[5].option.push({
              label: db,
              value: db,
            });
          }
        })
        .finally(() => {
          $q.loading.hide();
        });
    };
    return {
      formList,
      databaseDetails,
      getTablesForOption,
      getDatabasesForOption,
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
          username: null,
          database: null,
          table: null,
          select: null,
          parameter: null,
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
      this.$router.push("/settings/database/add");
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
      this.getDatabasesForOption(this.formListDetails);
      this.getTablesForOption(this.formListDetails);
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
        Username: row.username,
        Database: row.database,
        Table: row.table,
        Select: row.select,
        Parameter: row.parameter,
        Status: STATUS[row.status],
        "Created At": moment(row.created_at).format("YYYY-MM-DD HH:mm:ss"),
      };
      this.infoDialogStatus = true;
    },
    async submitEdit(data) {
      this.$q.loading.show();
      data.database = data.database.value || data.database;
      data.table = data.table.value || data.table;
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
