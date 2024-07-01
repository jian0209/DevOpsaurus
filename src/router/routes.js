const routes = [
  {
    path: "/login",
    component: () => import("layouts/LoginLayout.vue"),
    children: [
      {
        path: "",
        name: "login",
        component: () => import("pages/LoginPage.vue"),
      },
    ],
  },
  {
    path: "/dashboard",
    component: () => import("layouts/UserLayout.vue"),
    children: [
      {
        path: "",
        name: "dashboard",
        component: () => import("pages/DashboardPage.vue"),
      },
    ],
  },
  {
    path: "/redis",
    component: () => import("layouts/UserLayout.vue"),
    children: [
      {
        path: "",
        name: "redis",
        component: () => import("pages/RedisPage.vue"),
      },
    ],
  },
  {
    path: "/ups-monitor",
    component: () => import("layouts/UserLayout.vue"),
    children: [
      {
        path: "",
        name: "ups-monitor",
        component: () => import("pages/UpsPage.vue"),
      },
    ],
  },
  {
    path: "/nodes",
    component: () => import("layouts/UserLayout.vue"),
    children: [
      {
        path: "monitor",
        name: "nodes-monitor",
        component: () => import("pages/nodes/MonitorPage.vue"),
      },
      {
        path: "edit",
        name: "nodes-edit",
        component: () => import("pages/nodes/EditNginxPage.vue"),
      },
    ],
  },
  {
    path: "/database",
    component: () => import("layouts/UserLayout.vue"),
    children: [
      {
        path: "view",
        name: "database-view",
        component: () => import("pages/database/ViewPage.vue"),
      },
      {
        path: "edit",
        name: "database-edit",
        component: () => import("pages/database/EditPage.vue"),
      },
      {
        path: "schedule",
        name: "database-schedule",
        component: () => import("pages/database/SchedulePage.vue"),
      },
    ],
  },
  {
    path: "/command",
    component: () => import("layouts/UserLayout.vue"),
    children: [
      {
        path: "",
        name: "command",
        component: () => import("pages/CommandPage.vue"),
      },
    ],
  },
  {
    path: "/log",
    component: () => import("layouts/UserLayout.vue"),
    children: [
      {
        path: "user",
        name: "log-user",
        component: () => import("pages/logs/UserLoginLog.vue"),
      },
      {
        path: "system",
        name: "log-system",
        component: () => import("pages/logs/SystemLog.vue"),
      },
    ],
  },
  {
    path: "/settings",
    component: () => import("layouts/UserLayout.vue"),
    children: [
      {
        path: "user",
        name: "settings-user",
        component: () => import("pages/settings/SettingUserPage.vue"),
      },
      {
        path: "user/add",
        name: "settings-user-add",
        component: () => import("pages/settings/components/UserAddPage.vue"),
      },
      {
        path: "redis",
        name: "settings-redis",
        component: () => import("pages/settings/SettingRedisPage.vue"),
      },
      {
        path: "redis/add",
        name: "settings-redis-add",
        component: () => import("pages/settings/components/RedisAddPage.vue"),
      },
      {
        path: "ups",
        name: "settings-ups",
        component: () => import("pages/settings/SettingUpsPage.vue"),
      },
      {
        path: "ups/add",
        name: "settings-ups-add",
        component: () => import("pages/settings/components/UpsAddPage.vue"),
      },
      {
        path: "nodes",
        name: "settings-nodes",
        component: () => import("pages/settings/SettingNodesPage.vue"),
      },
      {
        path: "nodes/add",
        name: "settings-nodes-add",
        component: () => import("pages/settings/components/NodesAddPage.vue"),
      },
      {
        path: "database",
        name: "settings-database",
        component: () => import("pages/settings/SettingDatabasePage.vue"),
      },
      {
        path: "database/add",
        name: "settings-database-add",
        component: () =>
          import("pages/settings/components/DatabaseAddPage.vue"),
      },
      {
        path: "command",
        name: "settings-command",
        component: () => import("pages/settings/SettingCommandPage.vue"),
      },
      {
        path: "command/add",
        name: "settings-command-add",
        component: () => import("pages/settings/components/CommandAddPage.vue"),
      },
      {
        path: "integration",
        name: "settings-integration",
        component: () => import("pages/settings/SettingIntegrationPage.vue"),
      },
      {
        path: "mail",
        name: "settings-mail",
        component: () => import("pages/settings/SettingMailPage.vue"),
      },
      {
        path: "telegram",
        name: "settings-telegram",
        component: () => import("pages/settings/SettingTelegramPage.vue"),
      },
    ],
  },
  {
    path: "/forbidden",
    component: () => import("pages/ErrorForbidden.vue"),
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
