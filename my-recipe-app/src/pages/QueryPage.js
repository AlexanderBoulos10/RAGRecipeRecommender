import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/QueryPage.css";

const QueryPage = () => {
	const [recipe, setRecipe] = useState("");
	const [ingredients, setIngredients] = useState(""); // For ingredient input
	const [isRecipeMode, setIsRecipeMode] = useState(true); // Toggle between query and ingredient modes
	const [isLoading, setIsLoading] = useState(false);
	const navigate = useNavigate();

	const handleSubmit = async (e) => {
		e.preventDefault();
		setIsLoading(true); // Set loading to true when the user clicks submit
		const endpoint = isRecipeMode ? "recipeQuery" : "ingredientQuery";
		try {
			const response = await fetch(`http://localhost:8000/${endpoint}`, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					query_text: isRecipeMode ? recipe : ingredients,
				}),
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
			<h2 className="subtitle">Choose your input method</h2>

			<div className="toggle">
				<label>
					<input
						type="radio"
						name="inputMode"
						value="query"
						checked={isRecipeMode}
						onChange={() => setIsRecipeMode(true)}
					/>
					Search by Recipe Name
				</label>
				<label>
					<input
						type="radio"
						name="inputMode"
						value="ingredients"
						checked={!isRecipeMode}
						onChange={() => setIsRecipeMode(false)}
					/>
					Search by Ingredients
				</label>
			</div>

			{/* Render the appropriate form based on the input mode */}
			<form onSubmit={handleSubmit} className="query-form">
				{isRecipeMode ? (
					<>
						<input
							className="query-input"
							type="text"
							placeholder="Enter your culinary craving..."
							value={recipe}
							onChange={(e) => setRecipe(e.target.value)}
							required
						/>
					</>
				) : (
					<>
						<textarea
							className="ingredients-input"
							placeholder="Enter ingredients separated by commas..."
							value={ingredients}
							onChange={(e) => setIngredients(e.target.value)}
							required
						/>
					</>
				)}
				<button
					className="submit-button"
					type="submit"
					disabled={isLoading}>
					{isLoading ? "Loading..." : "Get Recipe"}
				</button>
			</form>

			{isLoading && <div className="loader"></div>}
		</div>
	);
};

export default QueryPage;
