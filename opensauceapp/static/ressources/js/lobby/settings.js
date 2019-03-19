let score_goal_select = document.getElementById("score_goal_select");

let catergory_difficulty_checkbox = document.getElementByClassName("catergory-difficulty-checkbox");

console.log(catergory_difficulty_checkbox);

score_goal_select.addEventListener("change", function(e) {
    let score_goal_value = e.srcElement.selectedOptions[0].value;
    console.log(score_goal_value);
});
