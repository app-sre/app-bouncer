import yaml
from textwrap import dedent

from checks.replicas import CheckReplicaCount
from lib.result import CheckError, CheckSuccess


def test_replicas_valid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps/v1
    kind: Deployment
    metadata:
        name: test
    spec:
        replicas: 3
        template:
            spec:
                containers: []
    """))

    c = CheckReplicaCount()

    result = c.check_replica_count(manifest)
    assert isinstance(result, CheckSuccess)


def test_replicas_invalid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps/v1beta1
    kind: Deployment
    metadata:
        name: test
    spec:
        replicas: 1
        template:
            spec:
                containers: []
    """))

    c = CheckReplicaCount()

    result = c.check_replica_count(manifest)
    assert isinstance(result, CheckError)


def test_minreplicas_valid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: autoscaling/v1
    kind: HorizontalPodAutoscaler
    metadata:
        name: test
    spec:
        minReplicas: 3
    """))

    c = CheckReplicaCount()

    result = c.check_min_replica_count(manifest)
    assert isinstance(result, CheckSuccess)


def test_minreplicas_invalid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: autoscaling/v1
    kind: HorizontalPodAutoscaler
    metadata:
        name: test
    spec:
        minReplicas: 1
    """))

    c = CheckReplicaCount()

    result = c.check_min_replica_count(manifest)
    assert isinstance(result, CheckError)
