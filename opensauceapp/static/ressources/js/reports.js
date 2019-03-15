let ignore_buttons = document.getElementsByClassName("ignore_button");
let delete_buttons = document.getElementsByClassName("delete_button");

[].forEach.call(ignore_buttons, function (button) { button.addEventListener("click", execute_ignore); });
[].forEach.call(delete_buttons, function (button) { button.addEventListener("click", execute_delete); });

function execute_delete(event)
{
  let source = event.target || event.srcElement;
  let card = document.getElementById("report_card_" + source.value);
  let data = {id : source.value}

  fetch('/report_delete/', {
      method: "DELETE",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
          "Content-Type": "application/json",
      },
      redirect: "follow",
      referrer: "no-referrer",
      body: JSON.stringify(data),
  });

  card.style.visibility = 'hidden';
}

function execute_ignore(event)
{
  let source = event.target || event.srcElement;
  let card = document.getElementById("report_card_" + source.value);
  let data = {id : source.value}

  fetch('/report_ignore/', {
      method: "DELETE",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
          "Content-Type": "application/json",
      },
      redirect: "follow",
      referrer: "no-referrer",
      body: JSON.stringify(data),
  });

  card.style.visibility = 'hidden';
}
