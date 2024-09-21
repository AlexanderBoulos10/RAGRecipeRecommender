import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/QueryPage.css";

const QueryPage = () => {
	const [query, setQuery] = useState("");
	const navigate = useNavigate();

	const handleSubmit = async (e) => {
		e.preventDefault();
		// Send query to backend
		const response = await fetch("http://localhost:8000/query", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ query_text: query }),
		});
		const data = await response.json();

		// Navigate to ResultPage with the recipe data
		navigate("/result", { state: { recipe: data } });
	};

	return (
		<div className="query-page">
			<h1 className="title">Recipe Recommendation System</h1>
			<h2 className="subtitle">What recipe are you looking for?</h2>
			<form onSubmit={handleSubmit} className="query-form">
				<input
					className="query-input"
					type="text"
					placeholder="Enter your culinary craving..."
					value={query}
					onChange={(e) => setQuery(e.target.value)}
					required
				/>
				<button className="submit-button" type="submit">
					Get Recipe
				</button>
			</form>
		</div>
	);
};

export default QueryPage;
