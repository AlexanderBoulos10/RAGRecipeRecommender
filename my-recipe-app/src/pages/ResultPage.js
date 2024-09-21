import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "../styles/ResultPage.css";

const ResultPage = () => {
	const location = useLocation();
	const navigate = useNavigate();
	const recipe = location.state?.recipe;

	if (!recipe) {
		return <div>No recipe found. Please go back and try again.</div>;
	}

	return (
		<div className="result-page">
			<h1 className="recipe-title">{recipe.title}</h1>

			<h2 className="section-title">Ingredients</h2>
			<ul className="ingredients-list">
				{recipe.ingredients.map((ingredient, index) => (
					<li key={index} className="ingredient-item">
						{ingredient}
					</li>
				))}
			</ul>

			<h2 className="section-title">Instructions</h2>
			<ol className="instructions-list">
				{recipe.instructions.map((instruction, index) => (
					<li key={index} className="instruction-item">
						{instruction}
					</li>
				))}
			</ol>

			<button className="back-button" onClick={() => navigate(-1)}>
				Back to Search
			</button>
		</div>
	);
};

export default ResultPage;
