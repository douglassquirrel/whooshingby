function display_reward()
{
}

function check_reward() {
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
      if (xmlhttp.readyState == 4) {
        new_rewards = JSON.parse(xmlhttp.responseText);
          alert(JSON.stringify(new_rewards));
      }
    }
    xmlhttp.open("GET", FACT_URL + '/reward', true);
    xmlhttp.send();
}

setInterval(check_reward, 10000);