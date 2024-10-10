// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-04-03",
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      // Use the correct backend URL
      apiBase:
        process.env.NODE_ENV === "development"
          ? "http://127.0.0.1:8000" // Django backend in development
          : "http://django-backend:8000", // Docker backend
    },
  },
});
