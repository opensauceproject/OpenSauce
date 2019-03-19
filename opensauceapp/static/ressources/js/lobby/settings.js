let score_goal_select = document.getElementById("score_goal_select");

let catergory_difficulty_checkbox = document.getElementByClassName("catergory-difficulty-checkbox");

console.log(catergory_difficulty_checkbox);

score_goal_select.addEventListener("change", send_settings);

for(let i = 0; i < catergory_difficulty_checkbox.length; i++)
{
    // Verify this when network
    let checkbox = catergory_difficulty_checkbox[i];
    checkbox.addEventListener("change", send_settings);
}

function update_settings(settings)
{
    // TODO Update settings according to the message
}

function send_settings()
{
    let settings = {};
    settings["score_goal_value"] = parseInt(e.srcElement.selectedOptions[0].value);
    lobby_socket.send(JSON.stringify({
        "type": "settings",
        "settings": settings,
    }));
}