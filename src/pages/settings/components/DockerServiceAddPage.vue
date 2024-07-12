<template>
  <SettingsAddCont
    title="Add Database Connection"
    addBtnTxt="Add Database Connection"
    testBtnTxt="Get Databases and Tables or Test Parameter"
    :formList="formList"
    :formListDetails="databaseDetails"
    @submit:add="add"
    @test:connection="getDatabaseAndTable"
  />
</template>

<script>
import { defineComponent, ref } from "vue";
import SettingsAddCont from "src/components/SettingsAddCont.vue";
import { addDatabase, getDatabases, getTables } from "src/api/settings";
import "src/css/settingsScreen.scss";
import { useQuasar } from "quasar";
import { useI18n } from "vue-i18n";

export default defineComponent({
  name: "DockerServiceAddPage",
  components: {
    SettingsAddCont,
  },
  setup() {
    const $q = useQuasar();
    const { t } = useI18n();
    const formList = ref([
      {
        label: "Name",
        model: "name",
        type: "text",
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
        hint: "* Eg: id IN {variable1} AND name IN {variable2}, leave it empty if no parameter is needed",
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

    const getDatabaseAndTable = async () => {
      $q.loading.show();
      if (!databaseDetails.value.database) {
        // get databases
        await getDatabases(databaseDetails.value)
          .then((res) => {
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
      } else {
        // get tables
        const data = {
          ...databaseDetails.value,
          database: databaseDetails.value.database.value,
        };
        await getTables(data)
          .then((res) => {
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
      }
    };
    return {
      formList,
      databaseDetails,
      getDatabaseAndTable,
    };
  },
  methods: {
    async add() {
      const data = {
        ...this.databaseDetails,
        database: this.databaseDetails.database.value,
        table: this.databaseDetails.table.value,
      };
      this.$q.loading.show();
      await addDatabase(data)
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
              message: this.$t(`api.${res.code}`),
              type: "negative",
            });
            return;
          }
          this.$q.notify({
            message: `Added ${this.databaseDetails.name} successfully!`,
            type: "positive",
          });
          this.$router.push("/settings/database");
        })
        .finally(() => {
          this.$q.loading.hide();
        });
    },
  },
});
</script>
