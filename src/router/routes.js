const routes = [
  {
    path: "/login",
    component: () => import("layouts/LoginLayout.vue"),
    children: [{ path: "", component: () => import("pages/LoginPage.vue") }],
  },
  {
    path: "/dashboard",
    component: () => import("layouts/UserLayout.vue"),
    children: [
      { path: "", component: () => import("pages/DashboardPage.vue") },
    ],
  },
  {
    path: "/redis",
    component: () => import("layouts/UserLayout.vue"),
    children: [{ path: "", component: () => import("pages/RedisPage.vue") }],
  },
  {
    path: "/ups-monitor",
    component: () => import("layouts/UserLayout.vue"),
    children: [{ path: "", component: () => import("pages/UpsPage.vue") }],
  },
  {
    path: "/nodes",
    component: () => import("layouts/UserLayout.vue"),
    children: [
      {
        path: "/monitor",
        component: () => import("pages/nodes/MonitorPage.vue"),
      },
      {
        path: "/edit",
        component: () => import("pages/nodes/EditNginxPage.vue"),
      },
    ],
  },
  {
    path: "/database",
    component: () => import("layouts/UserLayout.vue"),
    children: [
      {
        path: "/view",
        component: () => import("pages/database/ViewPage.vue"),
      },
      {
        path: "/edit",
        component: () => import("pages/database/EditPage.vue"),
      },
      {
        path: "/schedule",
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
        component: () => import("pages/CommandPage.vue"),
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
