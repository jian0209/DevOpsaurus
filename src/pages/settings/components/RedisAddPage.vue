<template>
  <div>
    <TitleContainer title="Add Redis Connection" />
    <q-form @submit="submitAddUser" class="form-main-cont">
      <div
        class="form-input-cont"
        v-for="(item, index) in formList"
        :key="index"
      >
        <div class="form-input-name">{{ item.label }}</div>
        <q-input
          v-if="
            item.type === 'text' ||
            item.type === 'email' ||
            item.type === 'password'
          "
          v-model="redisDetails[item.model]"
          :type="item.type"
          class="usual-form-input"
          color="secondary"
          dense
          outlined
        />
        <q-select
          v-if="item.type === 'select'"
          class="usual-form-input"
          v-model="redisDetails[item.model]"
          :options="roles"
          color="secondary"
          outlined
          dense
        />
      </div>
      <div class="add-btn-cont">
        <UsualButton label="Add Redis Connection" type="submit" color="info" />
      </div>
    </q-form>
  </div>
</template>

<script>
import { computed, defineComponent } from "vue";
import TitleContainer from "src/components/TitleCont.vue";
import UsualButton from "src/components/Button.vue";
import "src/css/settingsScreen.scss";

export default defineComponent({
  name: "RedisAddPage",
  components: {
    TitleContainer,
    UsualButton,
  },
  data() {
    return {
      formList: [
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
      redisDetails: {
        host: null,
        port: null,
        database: null,
        auth: null,
        get: null,
      },
    };
  },
  methods: {
    submitAddRedis() {
      console.log("Add redis", this.redisDetails);
      this.$router.push("/settings/redis");
    },
  },
});
</script>
