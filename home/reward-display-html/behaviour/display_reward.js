function display_reward()
{
}

function compare_rewards(r, s) {
    if      (r['time'] != s['time']) { return r['time'] - s['time']; }

    if      (r['name'] < s['name'])  { return -1; }
    else if (r['name'] > s['name'])  { return 1;  }
    else                             { return 0; }
}

rewards = [];
function check_reward() {
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
      if (xmlhttp.readyState == 4) {
        server_rewards = JSON.parse(xmlhttp.responseText);
        server_rewards.sort(compare_rewards);
          if (server_rewards.length > rewards.length) {
            alert(JSON.stringify(server_rewards.slice(-1)[0]));
          }
        rewards = server_rewards;
      }
    }
    xmlhttp.open("GET", FACT_URL + '/reward', true);
    xmlhttp.send();
}

setInterval(check_reward, 10000);