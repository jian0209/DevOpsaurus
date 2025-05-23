import { boot } from "quasar/wrappers";
import { createI18n } from "vue-i18n";
import messages from "src/i18n";
import { useUserStore } from "src/stores/user";

export default boot(({ app }) => {
  const userStore = useUserStore();
  if (
    !userStore.language ||
    !userStore.language === "zh-CN" ||
    !userStore.language === "zh-TW"
  ) {
    userStore.language = "en-US";
  }

  function missingTranslationHandler(locale, key) {
    return key.split(".").findLast((item) => item);
  }

  const i18n = createI18n({
    locale: userStore.language,
    globalInjection: true,
    messages,
    missing: missingTranslationHandler,
  });

  app.use(i18n);
});
