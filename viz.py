import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from datetime import datetime, time

values = []

logical_clock_1 = []
global_times_1 = []

logical_clock_2 = []
global_times_2 = []

logical_clock_3 = []
global_times_3 = []

with open('port_2056_log.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(' | ')
        logical_clock_1 += [parts[0][15:]]
        datetime_obj = datetime.strptime(parts[2][13:-1], '%H:%M:%S.%f')
        global_times_1 += [datetime_obj]
        values += [parts]

with open('port_3056_log.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(' | ')
        logical_clock_2 += [parts[0][15:]]
        datetime_obj = datetime.strptime(parts[2][13:-1], '%H:%M:%S.%f')
        global_times_2 += [datetime_obj]
        values += [parts]
    
with open('port_4056_log.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(' | ')
        logical_clock_3 += [parts[0][15:]]
        datetime_obj = datetime.strptime(parts[2][13:-1], '%H:%M:%S.%f')
        global_times_3 += [datetime_obj]
        values += [parts]

print(values[-1])
print("len(logical_clock)", len(logical_clock_1))
print("len(global_times)", len(global_times_1))

fig, ax = plt.subplots()
ax.plot(global_times_1, logical_clock_1, label='Clock rate = 0.2')
ax.plot(global_times_2, logical_clock_2, label='Clock rate = 0.3')
ax.plot(global_times_3, logical_clock_3, label='Clock rate = 0.3')

plt.title('System Time vs Logical Clock per Clock Rate (CR)')
plt.xlabel('System time')
plt.ylabel('Logical clock')

ax.legend()

plt.xticks(global_times_1, rotation='vertical')
plt.xticks(global_times_2, rotation='vertical')
plt.xticks(global_times_3, rotation='vertical')

ax.yaxis.set_major_locator(MaxNLocator(10))
ax.xaxis.set_major_locator(MaxNLocator(10))

plt.savefig('Run 1.png')