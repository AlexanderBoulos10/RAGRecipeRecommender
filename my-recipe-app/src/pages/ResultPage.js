import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

const ResultPage = () => {
	const location = useLocation();
	const navigate = useNavigate();
	const recipe = location.state?.recipe;

	if (!recipe) {
		return <div>No recipe found. Please go back and try again.</div>;
	}

	return (
		<div>
			<h1>{recipe.title}</h1>
			<h2>Ingredients</h2>
			<ul>
				{recipe.ingredients.map((ingredient, index) => (
					<li key={index}>{ingredient}</li>
				))}
			</ul>
			<h2>Instructions</h2>
			<ol>
				{recipe.instructions.map((instruction, index) => (
					<li key={index}>{instruction}</li>
				))}
			</ol>
			<button onClick={() => navigate(-1)}>Go Back</button>
		</div>
	);
};

export default ResultPage;
