from lib.base import CheckBase, whitelist


class CheckReplicaCount(CheckBase):
    enable_parameter = "replica-count"
    description = 'check that minimum number of replicas is configured'
    default_enabled = True
    MIN_REPLICAS = 3

    def _do_check_(self, m, replica_cnt):
        template = "{} must have at least {} replicas"

        name = m['metadata']['name']
        err_msg = template.format(name, self.MIN_REPLICAS)

        assert replica_cnt >= self.MIN_REPLICAS, err_msg

    @whitelist('StatefulSet', 'Deployment', 'ReplicaSet', 'Scale',
               'ReplicationController')
    def check_replica_count(self, m):
        replicas = int(m['spec']['replicas'])
        self._do_check_(m, replicas)

    @whitelist('HorizontalPodAutoscaler')
    def check_min_replica_count(self, m):
        replicas = int(m['spec']['minReplicas'])
        self._do_check_(m, replicas)
