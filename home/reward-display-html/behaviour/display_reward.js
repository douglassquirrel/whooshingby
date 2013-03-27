rewards = [];

function check_reward() {
  xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4) {
      server_rewards = JSON.parse(xmlhttp.responseText);
      server_rewards.sort(compare_rewards);
        if (server_rewards.length > rewards.length) {
          latest_reward = server_rewards.slice(-1)[0]
          display_reward(latest_reward['name']);
        }
      rewards = server_rewards;
    }
  }
  xmlhttp.open("GET", FACT_URL + '/reward', true);
  xmlhttp.send();
}

function compare_rewards(r, s) {
  if      (r['time'] != s['time']) { return r['time'] - s['time']; }
  else if (r['name'] < s['name'])  { return -1; }
  else if (r['name'] > s['name'])  { return 1;  }
  else                             { return 0; }
}

function display_reward(name)
{
  reward_elts = document.querySelectorAll('*[data-reward]');
  for (i=0; i<reward_elts.length; i++) {
    reward_elts[i].style.display = 'none';
  }
  chosen_element = reward_elts[Math.floor(Math.random() * reward_elts.length)];
  chosen_element.style.display = 'block';
  name_elts = chosen_element.querySelectorAll('*[data-reward-name]');
  for (i=0; i<name_elts.length; i++) {
    name_elts[i].innerHTML = name;
  }
}

setInterval(check_reward, 1000);