<template>
  <div>
    <TitleContainer
      title="Redis Management"
      subtitle="Manage Redis Connection"
    />
    <div class="button-cont">
      <UsualButton
        label="Add Redis Connection"
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
      title="setting-redis"
    />
    <DialogComponent
      title="Edit Redis"
      :dialogStatus="editDialogStatus"
      :formList="formList"
      :formListDetails="formListDetails"
      testBtnTxt="Test Redis Connection"
      isFormDialog
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEdit"
      @test:connection="testRedisConnection"
    />
    <DialogComponent
      title="Enable Redis"
      :dialogStatus="enableDialogStatus"
      :subtitle="`This Will Enable Redis {${selectedRow}} Be View By User`"
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEditStatus(1)"
    />
    <DialogComponent
      title="Disable Redis"
      :dialogStatus="disableDialogStatus"
      :subtitle="`This Will Disable Redis {${selectedRow}} Be View By User`"
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitEditStatus(0)"
    />
    <DialogComponent
      title="Delete Redis"
      :dialogStatus="deleteDialogStatus"
      :subtitle="`This Will Delete Redis Record {${selectedRow}}`"
      @update:dialogStatus="updateDialogStatus"
      @submit:edit="submitDelete"
    />
    <DialogComponent
      isInfoDialog
      title="Redis Information Details"
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
  getRedisList,
  editRedis,
  editStatusRedis,
  deleteRedis,
  testRedis,
} from "src/api/settings.js";
import "src/css/settingsScreen.scss";

export default defineComponent({
  name: "SettingRedisPage",
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
          host: null,
          port: null,
          database: null,
          auth: null,
          get: null,
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
          label: "Host",
          model: "host",
          type: "text",
        },
        {
          label: "Port",
          model: "port",
          type: "text",
        },
        {
          label: "Database",
          model: "database",
          type: "text",
        },
        {
          label: "Auth",
          model: "auth",
          type: "text",
        },
        {
          label: "Get",
          model: "get",
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
      this.$router.push("/settings/redis/add");
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
          database: row.database,
          auth: row.auth,
        })
      );
      const encryptedString = this.$CryptoJS.AES.encrypt(
        rowString,
        process.env.ENCRYPT_KEY
      );
      this.$router.push({
        path: "/settings/redis/add",
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
        Database: row.database,
        Auth: row.auth,
        Get: row.get,
        Status: STATUS[row.status],
        "Created At": moment(row.created_at).format("YYYY-MM-DD HH:mm:ss"),
      };
      this.infoDialogStatus = true;
    },
    async submitEdit(data) {
      this.$q.loading.show();
      await editRedis(data)
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
      await editStatusRedis(data)
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
      await deleteRedis(data)
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
    async testRedisConnection(data) {
      this.$q.loading.show();
      await testRedis(data)
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
            message: "Test Redis Connection Successfully!",
            type: "positive",
          });
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
