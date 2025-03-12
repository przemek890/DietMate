import { vitePlugin as remix } from "@remix-run/dev";
import { defineConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [
    remix({
      future: {
        v3_fetcherPersist: true,
        v3_relativeSplatPath: true,
        v3_throwAbortReason: true,
        v3_singleFetch: true,
        v3_lazyRouteDiscovery: true,
      },
    }),
    {
      name: "remix-manifest-resolver",
      resolveId(id) {
        if (id === "remix:manifest") {
          return id;
        }
      },
      load(id) {
        if (id === "remix:manifest") {
          return "export default {}";
        }
      },
    },
    tsconfigPaths(),
  ],
  define: {
    'window.VITE_REACT_APP_DOMAIN': JSON.stringify(process.env.REACT_APP_DOMAIN || 'http://localhost')
  },
});
