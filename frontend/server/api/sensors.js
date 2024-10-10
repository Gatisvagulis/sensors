export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  // Make a request to the external API
  const result = await $fetch(`${config.public.apiBase}/api/sensors`);
  return result;
});
