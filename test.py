from datetime import datetime

time = "2020/03/27 - 2020/03/31"

starttime, endtime = time.split('-')
start_time = starttime.strip().replace('/', '-') + ' 00:00:00'
starttimes = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

print(start_time)
print(starttimes)
print(type(start_time))
print(type(starttimes))

print('*' * 10)

test = datetime.now()

test_time = test.strftime("%Y-%m-%d %H:%M:%S")
print(test)
print(type(test))
print(test_time)
print(type(test_time))
