#!/usr/bin/ruby
require 'kropotkin'

while true
  fact = get_oldest_fact_and_stamp('whooshingby', 'completed-task',
                                   {}, 'rewarder_ruby')
  if !fact
    next
  end

  reward_percentages = get_newest_fact('whooshingby',
                                       'reward_percentages',
                                       {})['percentages']

  r = (fact['name'].hash * 47 + fact['time'].hash * 61) % 100
  n = 0
  for p in reward_percentages
    name = p[0]
    percentage = p[1]
    if !((n...n+percentage).include?(r))
      n = n + percentage
      next
    end

    content = {'name' => name, 'task_id' => fact['kropotkin_id'], \
               'source' => 'ruby'}
    if !(store_opinion('whooshingby', 'reward', content))
      print "Could not store reward opinion"
    end
    break
  end
end
