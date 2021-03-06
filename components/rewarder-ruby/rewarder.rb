#!/usr/bin/env ruby
require 'kropotkin'
require 'json'

STDOUT.sync = true
STDERR.sync = true

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

Kropotkin.subscribe('whooshingby', 'fact', 'completed_task')
while true
  fact = Kropotkin.get_next_statement('whooshingby', 'fact', 'completed_task')

  percentages_fact = Kropotkin.get_newest_fact('whooshingby',
                                               'reward_percentages',
                                               {})
  reward_percentages = JSON.parse(percentages_fact['percentages'])

  random_value = (fact['name'].hash * 47 + fact['time'].hash * 61) % 100
  name = choose(random_value, reward_percentages)
  if name
    content = {'name' => name, 'task_id' => fact['task_id'], \
               'source' => 'ruby', 'time' => Time.now.to_i}
    if !(Kropotkin.store_opinion('whooshingby', 'reward', content))
      print "Could not store reward opinion"
    end
  end
end
