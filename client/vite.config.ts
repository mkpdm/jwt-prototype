import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

import { resolve } from "node:path";

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [react()],
	resolve: {
		alias: {
			"@layout": resolve(__dirname, "./src/app/layout"),
			"@components": resolve(__dirname, "./src/app/components"),
			"@data": resolve(__dirname, "./src/data"),
			"@hooks": resolve(__dirname, "./src/hooks"),
			"@assets": resolve(__dirname, "./src/assets"),
			"@styles": resolve(__dirname, "./src/assets/styles"),
			"@icons": resolve(__dirname, "./src/assets/icons"),
		},
	},
});
