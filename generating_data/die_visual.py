import plotly.express as px

from die import Die

# Create a D6.
die_1 = Die()
die_2 = Die(10)

# Make some rolls, and store results in a list.
results = []
for roll_num in range(50000):
    result = die_1.roll() + die_2.roll()
    results.append(result)
   
# Analyze the results.
frequencies = []
max_result = die_1.num_sides + die_2.num_sides
poss_results =  range(2, max_result+1)
for value in poss_results:
    frequency = results.count(value)
    frequencies.append(frequency)

print(frequencies)
    
# Visualize the results.
title = "Results of rolling D6 and D10 50,000 times."
labels = {'x': 'Result', 'y': 'Frequency of Result'}

hist = px.bar(x=poss_results, y=frequencies, title=title, labels=labels)
hist.update_layout(xaxis_dtick=1)
hist.show()

