# Purpose: Central service for emitting audit events uniformly
"""
GLTive Audit Logger Service
Reusable service pattern for modules to safely write audit trails.
"""
from audit.models.log import AuditLog


class AuditService:
    """
    Standard mechanism to construct and save AuditLog events.
    """

    @classmethod
    def log_event(
        cls,
        action_code: str,
        target_entity_type: str,
        target_entity_id: str,
        actor_user=None,
        company=None,
        before_snapshot: dict = None,
        after_snapshot: dict = None,
        metadata: dict = None,
    ) -> AuditLog:
        """
        Writes a single immutable audit entry safely.
        Swallows nothing — exceptions here mean the transaction failed, 
        ensuring audit enforcement.
        """
        
        log = AuditLog.objects.create(
            actor_user=actor_user,
            company=company,
            action_code=action_code,
            target_entity_type=target_entity_type,
            target_entity_id=str(target_entity_id),
            before_snapshot=before_snapshot or {},
            after_snapshot=after_snapshot or {},
            metadata=metadata or {},
        )
        
        return log
