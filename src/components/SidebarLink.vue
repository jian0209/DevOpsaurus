<template>
  <q-list>
    <q-item
      v-if="!$props.isExpended"
      clickable
      @click="goTo($props.routeTo, $props.name)"
      :active="$props.activeLink"
      active-class="active-link"
    >
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
      :default-opened="$props.needExpend"
    >
      <q-item
        v-for="(item, index) in $props.childLink"
        :key="index"
        clickable
        @click="goTo(item.routeTo, item.name)"
        class="sidebar-sub-item"
        :active="item.activeLink"
        active-class="active-link"
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

export default defineComponent({
  name: "SidebarLink",
  props: {
    activeLink: {
      type: Boolean,
      default: false,
    },
    name: {
      type: String,
      default: "",
    },
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
    needExpend: {
      type: Boolean,
      default: false,
    },
    childLink: {
      type: Array,
    },
  },
  methods: {
    goTo(route, name) {
      if (route) {
        this.$router.push({ path: route });
        this.$emit("update:activeLink", name);
      }
    },
  },
});
</script>
