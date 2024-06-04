import React from "react";
import ReactDOM from "react-dom/client";
import App from "./app/App.tsx";

import "@styles/index.module.css";

// biome-ignore lint/style/noNonNullAssertion: Root will always be present.
ReactDOM.createRoot(document.getElementById("root")!).render(
	<React.StrictMode>
		<App />
	</React.StrictMode>,
);
