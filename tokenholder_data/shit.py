percentages = [
    31.6608, 5.0368, 4.7809, 2.2500, 1.6248, 1.4763, 0.9176, 0.6368,
    0.5603, 0.5492, 0.4800, 0.4786, 0.4733, 0.4674, 0.4632, 0.4618,
    0.4510, 0.4411, 0.4409, 0.4396, 0.4385, 0.4300, 0.4205, 0.4202,
    0.4101, 0.4093, 0.4052, 0.4037, 0.3988, 0.3950, 0.3849, 0.3750,
    0.3741, 0.3695, 0.3635, 0.3539, 0.3508, 0.3500, 0.3429, 0.3422,
    0.3418, 0.3344, 0.3299, 0.3273, 0.3267, 0.3266, 0.3263, 0.3244,
    0.3232, 0.3225
]

additional_percentages = [
    0.3214, 0.3200, 0.3146, 0.3136, 0.3082, 0.3061, 0.3043, 0.3002, 0.2991, 0.2989,
    0.2984, 0.2977, 0.2955, 0.2918, 0.2840, 0.2836, 0.2832, 0.2804, 0.2774, 0.2768,
    0.2757, 0.2748, 0.2736, 0.2705, 0.2704, 0.2679, 0.2653, 0.2652, 0.2608, 0.2608,
    0.2566, 0.2504, 0.2485, 0.2449, 0.2418, 0.2403, 0.2400, 0.2383, 0.2309, 0.2257,
    0.2251, 0.2242, 0.2175, 0.2080, 0.2039, 0.2036, 0.2018, 0.2003
]

# Convert percentages to float values and calculate the sum
total_additional_percentage = sum(additional_percentages)

# Convert percentages to float values and calculate the sum
total_percentage = sum(percentages)
print(total_percentage)
print(total_percentage+total_additional_percentage)