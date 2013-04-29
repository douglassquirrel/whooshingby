function check_reward() {
  reward_xmlhttp = new XMLHttpRequest();
  reward_xmlhttp.onreadystatechange = function() {
    if (reward_xmlhttp.readyState != 4) { return; }

    if (reward_xmlhttp.responseText.length > 0) {
      server_rewards = JSON.parse(reward_xmlhttp.responseText);
      if (server_rewards.length > 0) {
        display_reward(server_rewards[0]['name']);
      }
    }
  }

  /* Need to add a unique id here */
  query_string = 'kropotkin_criteria=stamp-display_reward.3141,result-oldest';
  url = '/factspace/kropotkin/reward?' + query_string;

  reward_xmlhttp.open("GET", url, true);
  reward_xmlhttp.send();
}

function display_reward(name)
{
  reward_elts = document.querySelectorAll('*[data-reward]');
  hidden_elts = []
  for (i=0; i<reward_elts.length; i++) {
      if (reward_elts[i].style.display != 'none') {
        reward_elts[i].style.display = 'none';
      } else {
        hidden_elts.push(reward_elts[i]);
      }
  }
  chosen_element = hidden_elts[Math.floor(Math.random() * hidden_elts.length)];
  chosen_element.style.display = 'block';
  name_elts = chosen_element.querySelectorAll('*[data-reward-name]');
  for (i=0; i<name_elts.length; i++) {
    name_elts[i].innerHTML = name;
  }
}

setInterval(check_reward, 1000);