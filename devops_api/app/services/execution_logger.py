import logging
logger = logging.getLogger(__name__)

import json
from sqlalchemy.orm import Session
from app import models
from datetime import datetime
from typing import Union


def log_execution_event(
    db: Session,
    execution_id: int,
    user_id: int,
    event: str,
    message: Union[str, dict],
    log_content: Union[str, dict] = ""
):
    """
    Crée une entrée dans execution_logs.
    Convertit automatiquement les dicts en JSON pour éviter les erreurs SQL.
    """

    # Sécuriser : convertir tous les dicts en chaîne pour message
    if isinstance(message, dict):
        try:
            message = json.dumps(message, indent=2, ensure_ascii=False)
        except Exception as e:
            message = f"[ERREUR de serialization JSON message] {str(e)}"

    # log_content uniquement pour affichage console
    if isinstance(log_content, dict):
        try:
            log_content = json.dumps(log_content, indent=2, ensure_ascii=False)
        except Exception as e:
            log_content = f"[ERREUR de serialization JSON log_content] {str(e)}"

    logger.debug("[execution_logger] save event=%s execution_id=%d", event, execution_id)
    logger.debug("[execution_logger] message=%s", message[:120])
    logger.debug("[execution_logger] log_content=%s", log_content[:120])

    log = models.ExecutionLog(
        execution_id=execution_id,
        user_id=user_id,
        event=event,
        message=message,
        created_at=datetime.utcnow()
    )

    db.add(log)
    db.commit()
    logger.debug("[execution_logger] log enregistré execution_id=%d event=%s", execution_id, event)
