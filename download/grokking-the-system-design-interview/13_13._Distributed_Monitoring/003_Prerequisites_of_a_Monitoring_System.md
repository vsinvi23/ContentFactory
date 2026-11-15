# Prerequisites_of_a_Monitoring_System

Source: https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Prerequisites of a Monitoring System

Explore the core components of effective distributed monitoring systems metrics and alerting. Define how to measure system health and the necessity of setting clear thresholds. Analyze the design decision between push and pull strategies for metric collection and data persistence.

We'll cover the following...

- [Monitoring: Metrics and alerting](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Monitoring-Metrics-and-alerting)
- [Metrics](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Metrics)
  - [Populate the metrics](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Populate-the-metrics)
  - [Persist the data](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Persist-the-data)
  - [Application metrics](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Application-metrics)
- [Alerting](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Alerting)

## Monitoring: Metrics and alerting[#](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Monitoring-Metrics-and-alerting)

A robust monitoring system defines specific **measurements** (metrics) and threshold values. When values exceed acceptable ranges, the system triggers **notifications** (alerts). This visibility enables support teams to respond quickly to health and performance issues, improving service stability. Rather than relying on intuition, engineers use telemetry data and automated alerts to monitor infrastructure health.

To understand how monitoring works, we will examine the significance of metrics, alerts, and the specific data required for effective tracking.

1.

What are the conventional approaches to handle failures in IT infrastructure?

Show Answer

Did you find this helpful?

## Metrics[#](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Metrics)

**Metrics** are objective measurements of a system’s activity. They provide real-time insight into component performance and health. Common examples include:

- **High-level data:** A web server’s request capacity or the number of active servers in a pool.
- **Network performance:** Throughput (megabits per second) and latency (round-trip time).

Collecting these metrics should incur minimal performance penalties, such as user-perceived latency or computational overhead.

Operating system resource usage is a standard starting point for monitoring. With a monitoring system in place, we can automatically track:

- Processor load and CPU statistics (e.g., cache hits/misses).
- RAM usage by the OS and processes.
- Disk space, read/write latencies, and swap space usage.

Metrics from web servers, databases, and other software help determine if the infrastructure is running smoothly.

> **Note:** Use the terminal below to view CPU utilization details for active processes on the virtual machine.

Terminal 1

Terminal

Click to Connect...

W

We use the `top` command to view Linux processes. This opens an interactive summary of the system and a list of active threads. The default view displays:

- **System summary:** Uptime, active users, and average load over the past few minutes.
- **Task state:** The status of tasks (`running`, `sleeping`, or `stopped`).
- **CPU consumption:** Percentage of CPU used by various processes.
- **Memory overview:** Physical memory statistics, including free, used, and buffered memory.

Follow these steps to observe a change in CPU usage:

1. Press `q` to quit the current terminal view.
2. Run `nohup ./script.sh &>/dev/null &`. This executes a script containing an infinite loop in the background.
3. Run the `top` command again to observe the increase in CPU usage.

### Populate the metrics[#](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Populate-the-metrics)

Metrics must be centralized for global monitoring. A fundamental design challenge is choosing how to move data from servers to the monitoring system: Push or Pull.

We define these strategies from the monitoring system’s perspective:

- **Pull strategy:** The monitoring system requests (pulls) metrics from an exposed endpoint on the server. In a pull-based model, the server stores metrics in memory and exposes them on request. This prevents the server from overwhelming the monitoring system, as the monitoring service controls the polling frequency.
- **Push strategy:** The server or a local agent sends (pushes) metrics to the monitoring system periodically. This is beneficial when firewalls prevent the monitoring system from accessing the server directly.

> **Key difference:** In the Pull model, data flows only when requested by the monitoring system. In the Push model, distributed collectors proactively send data to the monitoring system.

1.

Logging is the process of recording events in a software system. How does it help in monitoring?

Show Answer

Did you find this helpful?

> **Note:** The term “metrics” often refers to both the definition (what is measured) and the specific values recorded, depending on context.

### Persist the data[#](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Persist-the-data)

While a centralized in-memory repository works for small setups, large data centers generate enormous amounts of data. To handle this, we use [**time series databases (TSDB)**](https://www.educative.io/answers/what-is-a-time-series-database).

TSDBs store samples chronologically, ensuring durability and enabling historical analysis. This allows engineers to visualize a metric’s entire timeline, identify trends, and correlate events over time.

### Application metrics[#](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Application-metrics)

To track internal application logic, we use **code instrumentation**. This involves embedding code or APIs within the application to capture custom metrics that the OS cannot see.

Combined with system measurements, these metrics create a comprehensive view of the environment. Monitoring systems use this data to:

- Analyze historical trends and error rates.
- Automate responses (e.g., commissioning new EC2 instances when traffic spikes).
- Alert human operators when critical thresholds are breached.

## Alerting[#](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Alerting)

**Alerting** is the component that triggers action when metric values change. An alert definition consists of two parts:

1. **Condition:** A threshold or rule based on metric values (e.g., CPU > 90%).
2. **Action:** The response executed when the condition is met (e.g., send an email or page an engineer).

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27609%27%20height=%27150.69000000000005%27/%3e)![Metrics are collected continuously; an alert fires when a condition is met and triggers an action](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Metrics are collected continuously; an alert fires when a condition is met and triggers an action")

Metrics are collected continuously; an alert fires when a condition is met and triggers an action

Let’s test your understanding with the help of an AI assessment.

AI Powered

Saved

1 attempt left

Reset

Proactive monitoring

How would you design a monitoring system that can detect failures before users notice them?

This is your last attempt.

Introduction to Distributed Monitoring

Design of a Monitoring System

Ask

[Monitoring: Metrics and alerting](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Monitoring-Metrics-and-alerting)

[Metrics](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Metrics)

[Populate the metrics](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Populate-the-metrics)

[Persist the data](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Persist-the-data)

[Application metrics](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Application-metrics)

[Alerting](https://www.educative.io/courses/grokking-the-system-design-interview/prerequisites-of-a-monitoring-system#Alerting)