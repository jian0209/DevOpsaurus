<template>
  <q-layout view="lHh Lpr lFf" class="main-background global-css">
    <q-header elevated>
      <q-toolbar class="main-background">
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />
        <q-toolbar-title class="toolbar-title">
          {{ username }}
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      class="main-background sidebar"
    >
      <q-list>
        <q-item-label header class="sidebar-logo">
          <q-img src="src/assets/logo.png" height="100px" width="100px" />
          <p class="logo-text">DevOpsaurus</p>
        </q-item-label>

        <SidebarLink
          v-for="link in linksList"
          :key="link.title"
          v-bind="link"
          @update:activeLink="changeActiveLink($event)"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from "vue";
import SidebarLink from "components/SidebarLink.vue";
import { getInfo, logout } from "src/api/auth";
import { useUserStore } from "src/stores/user";

export default defineComponent({
  name: "UserLayout",
  components: {
    SidebarLink,
  },
  data() {
    return {
      linksList: [
        {
          title: "Dashboard",
          name: "Dashboard",
          icon: "space_dashboard",
          routeTo: "/dashboard",
          activeLink: false,
        },
        {
          title: "Redis",
          name: "Redis",
          icon: "storage",
          routeTo: "/redis",
          activeLink: false,
        },
        {
          title: "UPS",
          name: "UPS",
          icon: "battery_5_bar",
          routeTo: "/ups-monitor",
          activeLink: false,
        },
        {
          title: "Nodes",
          name: "Nodes",
          icon: "timeline",
          isExpended: true,
          childLink: [
            {
              title: "Monitor",
              name: "NodesMonitor",
              icon: "monitor_heart",
              routeTo: "/nodes/monitor",
              activeLink: false,
            },
            {
              title: "Edit Nginx",
              name: "NodesNginx",
              icon: "change_circle",
              routeTo: "/nodes/edit",
              activeLink: false,
            },
          ],
        },
        {
          title: "Database (MySQL)",
          name: "Database",
          icon: "schema",
          isExpended: true,
          childLink: [
            {
              title: "View Data",
              name: "DatabaseView",
              icon: "table_chart",
              routeTo: "/database/view",
              activeLink: false,
            },
            {
              title: "Edit Data",
              name: "DatabaseEdit",
              icon: "edit_note",
              routeTo: "/database/edit",
              activeLink: false,
            },
            {
              title: "Database Schedule",
              name: "DatabaseSchedule",
              icon: "update",
              routeTo: "/database/schedule",
              activeLink: false,
            },
          ],
        },
        {
          title: "Command",
          name: "Command",
          icon: "keyboard_command_key",
          routeTo: "/command",
          activeLink: false,
        },
        {
          title: "Logs",
          name: "Logs",
          icon: "assignment",
          routeTo: "/command",
          isExpended: true,
          childLink: [
            {
              title: "User Login",
              name: "userLoginLog",
              icon: "badge",
              routeTo: "/log/user",
              activeLink: false,
            },
            {
              title: "System",
              name: "systemLog",
              icon: "wysiwyg",
              routeTo: "/log/system",
              activeLink: false,
            },
          ],
        },
        {
          title: "Settings",
          name: "Settings",
          icon: "settings",
          isExpended: true,
          childLink: [
            {
              title: "Users",
              name: "SettingsUser",
              icon: "people_alt",
              routeTo: "/settings/user",
              activeLink: false,
            },
            {
              title: "Redis",
              name: "SettingsRedis",
              icon: "storage",
              routeTo: "/settings/redis",
              activeLink: false,
            },
            // {
            //   title: "UPS",
            //   name: "SettingsUPS",
            //   icon: "battery_5_bar",
            //   routeTo: "/settings/ups",
            //   activeLink: false,
            // },
            {
              title: "Nodes",
              name: "SettingsNodes",
              icon: "timeline",
              routeTo: "/settings/nodes",
              activeLink: false,
            },
            {
              title: "Database",
              name: "SettingsDatabase",
              icon: "schema",
              routeTo: "/settings/database",
              activeLink: false,
            },
            {
              title: "Command",
              name: "SettingsCommand",
              icon: "keyboard_command_key",
              routeTo: "/settings/command",
              activeLink: false,
            },
            {
              title: "Integration",
              name: "SettingsIntegration",
              icon: "settings_suggest",
              routeTo: "/settings/integration",
              activeLink: false,
            },
            {
              title: "Mail (SMTP)",
              name: "SettingsMail",
              icon: "mail_outline",
              routeTo: "/settings/mail",
              activeLink: false,
            },
            {
              title: "Telegram",
              name: "SettingsTelegram",
              icon: "send",
              routeTo: "/settings/telegram",
              activeLink: false,
            },
            {
              title: "Slack",
              name: "SettingsSlack",
              icon: "send",
              routeTo: "/settings/slack",
              activeLink: false,
            },
          ],
        },
        {
          title: "Logout",
          name: "Logout",
          icon: "door_sliding",
          routeTo: "/login",
          activeLink: false,
        },
      ],
      leftDrawerOpen: ref(false),
      activeLink: ref(""),
      getInfoInterval: null,
      userStore: useUserStore(),
      username: ref(""),
    };
  },
  methods: {
    initActiveLink() {
      this.compareLink("", true);
    },
    toggleLeftDrawer() {
      this.leftDrawerOpen = !this.leftDrawerOpen;
    },
    changeActiveLink(link) {
      this.compareLink(link);
    },
    compareLink(link, init = false) {
      this.linksList.forEach((parentLink, index) => {
        if (parentLink.childLink && parentLink.childLink.length > 0) {
          parentLink.childLink.forEach((childLink, j) => {
            if (init) {
              if (childLink.routeTo === this.$route.path) {
                this.linksList[index].childLink[j].activeLink = true;
                this.linksList[index].needExpend = true;
              }
            } else {
              this.linksList[index].childLink[j].activeLink =
                childLink.name === link;
              this.linksList[index].needExpend =
                this.linksList[index].childLink[j].activeLink;
            }
          });
        } else {
          if (init) {
            this.linksList[index].activeLink =
              parentLink.routeTo === this.$route.path;
          } else {
            this.linksList[index].activeLink = parentLink.name === link;
          }
        }
      });
    },
    getUserInfo() {
      getInfo().then((res) => {
        if (res.code !== 0) {
          logout();
          this.userStore.logout();
          this.$router.push({ path: "/login" });
          this.$q.notify({
            message: this.$t("dialog.sessionExpired"),
            type: "negative",
          });
          return;
        }

        this.userStore.setUserInfo(res.data);
        this.username = res.data.username;
      });
    },
    checkUser() {
      this.getInfoInterval = setInterval(() => {
        this.getUserInfo();
      }, 15000);
    },
    clearUserCheck() {
      if (this.getInfoInterval) {
        clearInterval(this.getInfoInterval);
        this.getInfoInterval = null;
      }
    },
  },
  created() {
    this.initActiveLink();
    this.getUserInfo();
    this.checkUser();
  },
  unmounted() {
    this.clearUserCheck();
  },
});
</script>
