import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import en from "./locales/en.json";
import az from "./locales/az.json";
import ru from "./locales/ru.json";
import tr from "./locales/tr.json";
import ar from "./locales/ar.json";

const savedLang = typeof window !== "undefined"
  ? localStorage.getItem("gltive-lang") || "en"
  : "en";

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: en },
    az: { translation: az },
    ru: { translation: ru },
    tr: { translation: tr },
    ar: { translation: ar },
  },
  lng: savedLang,
  fallbackLng: "en",
  interpolation: { escapeValue: false },
});

const RTL_LANGUAGES = new Set(["ar"]);

export function changeLanguage(lang: string) {
  i18n.changeLanguage(lang);
  localStorage.setItem("gltive-lang", lang);
  document.documentElement.lang = lang;
  if (RTL_LANGUAGES.has(lang)) {
    document.documentElement.dir = "rtl";
  } else {
    document.documentElement.dir = "ltr";
  }
}

// Set initial direction
if (RTL_LANGUAGES.has(savedLang)) {
  document.documentElement.dir = "rtl";
}
document.documentElement.lang = savedLang;

export const AVAILABLE_LANGUAGES = [
  { code: "en", name: "English" },
  { code: "az", name: "Azərbaycanca" },
  { code: "ru", name: "Русский" },
  { code: "tr", name: "Türkçe" },
  { code: "ar", name: "العربية", rtl: true },
] as const;

export default i18n;
