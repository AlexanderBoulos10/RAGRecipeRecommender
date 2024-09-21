import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/QueryPage.css";

const QueryPage = () => {
	const [query, setQuery] = useState("");
	const [isLoading, setIsLoading] = useState(false);
	const navigate = useNavigate();

	const handleSubmit = async (e) => {
		e.preventDefault();
		setIsLoading(true); // Set loading to true when the user clicks submit
		try {
			const response = await fetch("http://localhost:8000/query", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ query_text: query }),
			});
			const data = await response.json();
			navigate("/result", { state: { recipe: data } });
		} catch (error) {
			console.error("Error fetching recipe:", error);
		} finally {
			setIsLoading(false); // Set loading to false once the request is done
		}
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
				<button
					className="submit-button"
					type="submit"
					disabled={isLoading}>
					{isLoading ? "Loading..." : "Get Recipe"}
				</button>
			</form>
			{isLoading && <div className="loader"></div>}{" "}
			{/* Show loader if isLoading is true */}
		</div>
	);
};

export default QueryPage;
