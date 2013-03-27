function check_reward() {
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = receive_reward;
    xmlhttp.open("GET", FACT_URL + '/reward', true);
    xmlhttp.send();
}

function receive_reward()
{
  if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
    alert(xmlhttp.responseText);
  }
}

function display_reward()
{
}

setInterval(check_reward, 10000);