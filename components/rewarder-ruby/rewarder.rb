#!/usr/bin/ruby
require 'kropotkin'
require 'json'

def choose(random_value, percentages, default=nil)
  n = 0
  for p in percentages
    name = p[0]
    percentage = p[1]
    if (n...n+percentage).include?(random_value)
      return name
    else
      n = n + percentage
    end
  end
  return default
end

while true
  fact = get_oldest_fact_and_stamp('whooshingby', 'completed_task',
                                   {}, 'rewarder_ruby')
  if !fact
    next
  end

  percentages_fact = get_newest_fact('whooshingby', 'reward_percentages', {})
  reward_percentages = JSON.parse(percentages_fact['percentages'])

  random_value = (fact['name'].hash * 47 + fact['time'].hash * 61) % 100
  name = choose(random_value, reward_percentages)
  if name
    content = {'name' => name, 'task_id' => fact['task_id'], \
               'source' => 'ruby'}
    if !(store_opinion('whooshingby', 'reward', content))
      print "Could not store reward opinion"
    end
  end
end
