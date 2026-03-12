# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

# Prometheus query for Docker Swarm container CPU usage as a percentage.
#
# Query breakdown:
#   container_cpu_usage_seconds_total  - cAdvisor metric: cumulative CPU time consumed by containers (in seconds).
#   {APM_QUERY_FILTER, ...}            - Label selectors:
#       APM_QUERY_FILTER                   - Datadog placeholder replaced at runtime with environment-specific filters.
#       name!=''                           - Exclude entries with no container name (e.g. host-level cgroup summaries).
#       image!=''                          - Exclude entries with no image (e.g. pause/infra containers).
#       container_label_com_docker_swarm_service_name!=''
#                                          - Restrict to containers that belong to a Docker Swarm service.
#                                            Docker label "com.docker.swarm.service.name" is exposed by cAdvisor
#                                            as the Prometheus label "container_label_com_docker_swarm_service_name".
#   rate(...[1m])                      - Per-second average CPU consumption rate over the last 1 minute.
#   sum by (name, id, image, instance) - Aggregate across CPU modes, grouped by:
#       name     - Container name.
#       id       - Container ID (or cgroup path).
#       image    - Container image name.
#       instance - Prometheus scrape target (host:port) that provided the metrics.
#   * 100                              - Convert from fractional CPU cores/second to CPU usage percentage.
#   round(..., 0.01)                   - Round the result to two decimal places (precision of 0.01).
SWARM_CONTAINER_CPU_USAGE_PCT_QUERY = (
    "round("
    "sum by (name, id, image, instance) ("
    "rate(container_cpu_usage_seconds_total"
    "{APM_QUERY_FILTER, name!='', image!='', container_label_com_docker_swarm_service_name!=''}[1m])"
    ") * 100, 0.01)"
)
