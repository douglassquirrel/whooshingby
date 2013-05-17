#!/usr/bin/ruby
require 'kropotkin'

while true
  fact = get_oldest_fact_and_stamp('whooshingby', 'completed-task',
                                   {}, 'rewarder_ruby')
  if !fact
    next
  end

  reward_percentages = get_all_facts('whooshingby',
                                     'reward_percentage',
                                     {})

  r = (fact['name'].hash * 47 + fact['time'].hash * 61) % 100
  n = 0
  for reward in reward_percentages
    if !((n...n+reward['percentage']).include?(r))
      n = n + reward['percentage']
      next
    end

    content = {'name' => reward['name'], 'time' => Time.now.to_i}
    if !(store_opinion('whooshingby', 'reward', content))
      print "Could not store reward opinion"
    end
    break
  end
end
