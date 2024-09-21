import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

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
		<div>
			<h1>Recipe Recommendation System</h1>
			<form onSubmit={handleSubmit}>
				<label>
					Enter what kind of recipe you want to make:
					<input
						type="text"
						value={query}
						onChange={(e) => setQuery(e.target.value)}
						required
					/>
				</label>
				<button type="submit">Submit</button>
			</form>
		</div>
	);
};

export default QueryPage;
