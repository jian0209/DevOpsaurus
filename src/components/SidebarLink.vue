<template>
  <q-list>
    <q-item v-if="!$props.isExpended" clickable @click="goTo($props.routeTo)">
      <q-item-section v-if="$props.icon" avatar>
        <q-icon :name="$props.icon" />
      </q-item-section>

      <q-item-section>
        <q-item-label>{{ $props.title }}</q-item-label>
      </q-item-section>
    </q-item>

    <q-expansion-item
      v-else
      group="groupExpanded"
      :icon="$props.icon"
      :label="$props.title"
    >
      <q-item
        v-for="(item, index) in $props.childLink"
        :key="index"
        clickable
        @click="goTo(item.routeTo)"
        class="sidebar-sub-item"
      >
        <q-item-section v-if="item.icon" avatar>
          <q-icon :name="item.icon" />
        </q-item-section>

        <q-item-section>
          <q-item-label>{{ item.title }}</q-item-label>
        </q-item-section>
      </q-item>
    </q-expansion-item>
  </q-list>
</template>

<script>
import { defineComponent } from "vue";
import "src/css/component.scss";
import { useRouteStore } from "src/stores/route.js";

export default defineComponent({
  name: "SidebarLink",
  props: {
    title: {
      type: String,
      required: true,
    },
    caption: {
      type: String,
      default: "",
    },
    routeTo: {
      type: String,
      default: "/",
    },
    icon: {
      type: String,
      default: "",
    },
    isExpended: {
      type: Boolean,
      default: false,
    },
    childLink: {
      type: Array,
    },
  },
  setup() {
    const routerStore = useRouteStore();

    const goTo = (route) => {
      if (route) {
        routerStore.routeTo(route);
      }
    };

    return {
      goTo,
    };
  },
});
</script>
