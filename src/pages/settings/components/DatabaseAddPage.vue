<template>
  <SettingsAddCont
    title="Add Database Connection"
    addBtnTxt="Add Database Connection"
    testBtnTxt="Get Databases and Tables"
    :formList="formList"
    :formListDetails="databaseDetails"
    @submit:add="add"
  />
</template>

<script>
import { defineComponent } from "vue";
import SettingsAddCont from "src/components/SettingsAddCont.vue";
import "src/css/settingsScreen.scss";

export default defineComponent({
  name: "DatabaseAddPage",
  components: {
    SettingsAddCont,
  },
  data() {
    return {
      formList: [
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
          option: [
            {
              label: "Database 1",
              value: "database1",
            },
            {
              label: "Database 2",
              value: "database2",
            },
          ],
        },
        {
          label: "Table",
          model: "table",
          type: "select",
          option: [
            {
              label: "Table 1",
              value: "table1",
            },
            {
              label: "Table 2",
              value: "table2",
            },
          ],
        },
        {
          label: "Parameter (WHERE)",
          model: "parameter",
          type: "textarea",
          placeholder: "id IN {ids} AND / OR name = {name}",
          hint: "* Use comma to split (AND LOGIC), Eg: id IN {variable1} AND name IN {variable2}",
        },
      ],
      databaseDetails: {
        name: null,
        host: null,
        username: null,
        password: null,
        database: null,
        table: null,
      },
    };
  },
  methods: {
    add() {
      this.$q.notify({
        message: `Added ${this.databaseDetails.name} successfully!`,
        type: "positive",
      });
      this.$router.push("/settings/database");
    },
  },
});
</script>
