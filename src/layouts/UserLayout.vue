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
          icon: "space_dashboard",
          routeTo: "/dashboard",
        },
        {
          title: "Redis",
          icon: "storage",
          routeTo: "/redis",
        },
        {
          title: "UPS",
          icon: "battery_5_bar",
          routeTo: "/ups-monitor",
        },
        {
          title: "Nodes",
          icon: "timeline",
          isExpended: true,
          childLink: [
            {
              title: "Monitor",
              icon: "monitor_heart",
              routeTo: "/nodes/monitor",
            },
            {
              title: "Edit Nginx",
              icon: "change_circle",
              routeTo: "/nodes/edit",
            },
          ],
        },
        {
          title: "Database (MySQL)",
          icon: "schema",
          isExpended: true,
          childLink: [
            {
              title: "View Data",
              icon: "table_chart",
              routeTo: "/database/view",
            },
            {
              title: "Edit Data",
              icon: "edit_note",
              routeTo: "/database/edit",
            },
            {
              title: "Database Schedule",
              icon: "update",
              routeTo: "/database/schedule",
            },
          ],
        },
        {
          title: "Command",
          icon: "keyboard_command_key",
          routeTo: "/command",
        },
        {
          title: "Logout",
          icon: "door_sliding",
          routeTo: "/login",
        },
      ],
      leftDrawerOpen: false,
    };
  },
  methods: {
    toggleLeftDrawer() {
      this.leftDrawerOpen = !this.leftDrawerOpen;
    },
  },
});
</script>
