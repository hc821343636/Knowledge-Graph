import numpy as np
import matplotlib.pyplot as plt


def generate_source_signal(frequency, duration=1.0, sample_rate=1000, t=None):
    if t is None:
        t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
    source_signal = np.sin(2 * np.pi * frequency * t)
    return source_signal


def simulate_received_signals(source_signal, mic_distance, sound_speed=343.0, sample_rate=1000, angle=0):
    time_delay = (mic_distance * np.sin(np.radians(angle))) / sound_speed
    delay_samples = int(time_delay * sample_rate)

    # Simulate received signals with time delay
    received_signal1 = np.roll(source_signal, -delay_samples)
    received_signal1[-delay_samples:] = 0
    received_signal2 = source_signal

    return received_signal1, received_signal2


def calculate_correlation(received_signal1, received_signal2):
    correlation_coefficient = np.corrcoef(received_signal1, received_signal2)[0, 1]
    return correlation_coefficient

def find_first_peak_index(vector):
    for i in range(len(vector) - 1):
        if vector[i] > vector[i + 1]:
            return i
    return -1  # 如果没有找到满足条件的下标

# Parameters
frequency = 90.0  # Hz
mic_distance = 2.0  # meters
sound_speed = 343.0  # meters/second
sample_rate = 5000  # Hz
duration = 1.0  # seconds
angle = 70  # 入射角度，单位为度

# Generate source signal
t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
source_signal = generate_source_signal(frequency, duration=duration, sample_rate=sample_rate, t=t)

# Calculate correlations for different delays
max_delay_samples = int(sample_rate * duration)
delays = np.arange(0, max_delay_samples + 1)
correlation_values = []

for delay_samples in delays:
    received_signal1, received_signal2 = simulate_received_signals(source_signal, mic_distance, sound_speed,
                                                                   sample_rate, angle)
    received_signal1 = np.roll(received_signal1, delay_samples)

    correlation_coefficient = calculate_correlation(received_signal1, received_signal2)
    correlation_values.append(correlation_coefficient)

# Find the delay corresponding to the maximum correlation coefficient

estimated_delay_samples = find_first_peak_index(correlation_values)

estimated_delay_ms = estimated_delay_samples / sample_rate * 1000

# Calculate the estimated angle using the inverse formula
estimated_angle = np.degrees(np.arcsin((estimated_delay_ms * sound_speed) / (mic_distance * 1000)))

# Plot results
delay_times_ms = delays / sample_rate * 1000  # 转换为毫秒
plt.plot(delay_times_ms, correlation_values)
plt.title('Correlation Coefficient vs. Time Delay')
plt.xlabel('Time Delay (ms)')
plt.ylabel('Correlation Coefficient')

# Mark the estimated delay on the plot
plt.axvline(x=estimated_delay_ms, color='r', linestyle='--', label='Estimated Delay')
plt.legend()

plt.show()

# Print the estimated results
print(f"True Angle: {angle} degrees")
print(f"Estimated Delay: {estimated_delay_ms} ms")
print(f"Estimated Angle: {estimated_angle} degrees")
