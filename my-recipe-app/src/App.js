import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import QueryPage from "./pages/QueryPage";
import ResultPage from "./pages/ResultPage";

function App() {
	return (
		<Router>
			<Routes>
				<Route path="/" element={<QueryPage />} />
				<Route path="/result" element={<ResultPage />} />
			</Routes>
		</Router>
	);
}

export default App;
