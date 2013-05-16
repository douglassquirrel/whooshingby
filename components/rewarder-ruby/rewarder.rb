#!/usr/bin/ruby
require 'kropotkin'

STAMP = 'rewarderruby.%d' % Process.pid

while true
  fact = get_oldest_fact_and_stamp('whooshingby', 'completed-task', {}, STAMP)
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
      next
    end
    content = {'name' => reward['name'], 'time' => Time.now.to_i}
    if !(store_opinion('whooshingby', 'reward', content))
      print "Could not store reward opinion"
    end
    n = n + reward['percentage']
  end
end
