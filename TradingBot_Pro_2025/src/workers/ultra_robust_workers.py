"""
🔧 SYSTÈME WORKERS ULTRA-ROBUSTE - TRADINGBOT PRO 2025 ULTRA
Workers optimisés avec gestion d'erreurs avancée et monitoring en temps réel
"""

import asyncio
import time
import logging
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
import uuid
from collections import defaultdict, deque
import weakref

class TaskPriority(Enum):
    """Priorités des tâches"""
    CRITICAL = 1    # Trading urgent
    HIGH = 2        # Prédictions
    MEDIUM = 3      # Analytics
    LOW = 4         # Maintenance
    BACKGROUND = 5  # Logs, cleanup

class TaskStatus(Enum):
    """Statuts des tâches"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    """Définition d'une tâche"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    priority: TaskPriority = TaskPriority.MEDIUM
    data: Dict[str, Any] = field(default_factory=dict)
    callback: Optional[Callable] = None
    timeout: float = 30.0
    max_retries: int = 3
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    retries: int = 0
    worker_id: Optional[str] = None

@dataclass
class WorkerStats:
    """Statistiques d'un worker"""
    worker_id: str
    tasks_completed: int = 0
    tasks_failed: int = 0
    total_processing_time: float = 0.0
    last_activity: datetime = field(default_factory=datetime.now)
    current_task: Optional[str] = None
    is_healthy: bool = True
    error_rate: float = 0.0

class UltraRobustWorkerSystem:
    """Système de workers ultra-robuste avec monitoring avancé"""
    
    def __init__(self, max_workers: int = 5, queue_size: int = 1000):
        self.max_workers = max_workers
        self.queue_size = queue_size
        
        # Queues par priorité
        self.priority_queues = {
            TaskPriority.CRITICAL: asyncio.Queue(maxsize=100),
            TaskPriority.HIGH: asyncio.Queue(maxsize=200),
            TaskPriority.MEDIUM: asyncio.Queue(maxsize=300),
            TaskPriority.LOW: asyncio.Queue(maxsize=200),
            TaskPriority.BACKGROUND: asyncio.Queue(maxsize=200)
        }
        
        # État du système
        self.workers = {}
        self.worker_stats = {}
        self.is_running = False
        self.shutdown_event = asyncio.Event()
        
        # Monitoring et métriques
        self.task_history = deque(maxlen=1000)
        self.performance_metrics = {
            'total_tasks': 0,
            'completed_tasks': 0,
            'failed_tasks': 0,
            'avg_processing_time': 0.0,
            'queue_sizes': {},
            'worker_utilization': 0.0
        }
        
        # Configuration
        self.health_check_interval = 30.0
        self.stats_update_interval = 10.0
        self.max_consecutive_failures = 5
        
        # Callbacks
        self.task_callbacks = {
            'on_task_start': [],
            'on_task_complete': [],
            'on_task_failed': [],
            'on_worker_error': []
        }
        
        # Logger
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Configuration du logger"""
        logger = logging.getLogger("UltraRobustWorkers")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    async def start(self) -> bool:
        """Démarrage du système de workers"""
        if self.is_running:
            return True
        
        try:
            self.logger.info(f"🚀 Démarrage système workers ({self.max_workers} workers)")
            
            self.is_running = True
            self.shutdown_event.clear()
            
            # Démarrer les workers
            for i in range(self.max_workers):
                worker_id = f"worker-{i+1}"
                worker_task = asyncio.create_task(self._worker_loop(worker_id))
                self.workers[worker_id] = worker_task
                self.worker_stats[worker_id] = WorkerStats(worker_id=worker_id)
            
            # Démarrer les tâches de monitoring
            asyncio.create_task(self._health_monitor())
            asyncio.create_task(self._stats_updater())
            asyncio.create_task(self._queue_balancer())
            
            self.logger.info("✅ Système workers démarré avec succès")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur démarrage workers: {e}")
            return False
    
    async def stop(self, timeout: float = 30.0) -> bool:
        """Arrêt propre du système"""
        if not self.is_running:
            return True
        
        try:
            self.logger.info("🛑 Arrêt du système workers...")
            
            self.is_running = False
            self.shutdown_event.set()
            
            # Annuler tous les workers
            for worker_id, worker_task in self.workers.items():
                worker_task.cancel()
            
            # Attendre l'arrêt avec timeout
            try:
                await asyncio.wait_for(
                    asyncio.gather(*self.workers.values(), return_exceptions=True),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                self.logger.warning("⚠️ Timeout atteint lors de l'arrêt")
            
            # Nettoyer les queues
            await self._clear_all_queues()
            
            self.logger.info("✅ Système workers arrêté")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur arrêt workers: {e}")
            return False
    
    async def _worker_loop(self, worker_id: str):
        """Boucle principale d'un worker"""
        self.logger.info(f"🔄 Worker {worker_id} démarré")
        stats = self.worker_stats[worker_id]
        consecutive_failures = 0
        
        while self.is_running and not self.shutdown_event.is_set():
            try:
                # Récupérer une tâche avec priorité
                task = await self._get_next_task()
                
                if task is None:
                    await asyncio.sleep(0.1)
                    continue
                
                # Traiter la tâche
                success = await self._process_task(task, worker_id)
                
                if success:
                    consecutive_failures = 0
                    stats.tasks_completed += 1
                else:
                    consecutive_failures += 1
                    stats.tasks_failed += 1
                
                # Vérifier la santé du worker
                if consecutive_failures >= self.max_consecutive_failures:
                    self.logger.warning(f"⚠️ Worker {worker_id} en difficulté")
                    stats.is_healthy = False
                    await asyncio.sleep(5)  # Pause récupération
                    consecutive_failures = 0
                else:
                    stats.is_healthy = True
                
                stats.last_activity = datetime.now()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                consecutive_failures += 1
                stats.tasks_failed += 1
                self.logger.error(f"❌ Erreur worker {worker_id}: {e}")
                await self._trigger_callback('on_worker_error', worker_id, str(e))
                await asyncio.sleep(1)  # Pause avant retry
        
        stats.current_task = None
        self.logger.info(f"🛑 Worker {worker_id} arrêté")
    
    async def _get_next_task(self) -> Optional[Task]:
        """Récupération de la prochaine tâche selon priorité"""
        for priority in TaskPriority:
            queue = self.priority_queues[priority]
            
            try:
                task = queue.get_nowait()
                return task
            except asyncio.QueueEmpty:
                continue
        
        return None
    
    async def _process_task(self, task: Task, worker_id: str) -> bool:
        """Traitement d'une tâche avec gestion complète d'erreurs"""
        stats = self.worker_stats[worker_id]
        start_time = time.time()
        
        try:
            # Mettre à jour l'état
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
            task.worker_id = worker_id
            stats.current_task = task.id
            
            await self._trigger_callback('on_task_start', task)
            
            # Traitement avec timeout
            try:
                result = await asyncio.wait_for(
                    self._execute_task(task),
                    timeout=task.timeout
                )
                
                task.result = result
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now()
                
                await self._trigger_callback('on_task_complete', task)
                
                processing_time = time.time() - start_time
                stats.total_processing_time += processing_time
                
                self.task_history.append(task)
                self.performance_metrics['completed_tasks'] += 1
                
                return True
                
            except asyncio.TimeoutError:
                raise Exception(f"Timeout après {task.timeout}s")
            
        except Exception as e:
            task.error = str(e)
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now()
            
            # Retry logic
            if task.retries < task.max_retries:
                task.retries += 1
                task.status = TaskStatus.PENDING
                
                # Remettre en queue avec priorité réduite
                retry_priority = TaskPriority(min(task.priority.value + 1, 5))
                await self.add_task(task, retry_priority)
                
                self.logger.info(f"🔄 Retry tâche {task.name} ({task.retries}/{task.max_retries})")
            else:
                await self._trigger_callback('on_task_failed', task)
                self.performance_metrics['failed_tasks'] += 1
                self.logger.error(f"❌ Échec définitif tâche {task.name}: {e}")
            
            return False
        
        finally:
            stats.current_task = None
            self.performance_metrics['total_tasks'] += 1
    
    async def _execute_task(self, task: Task) -> Any:
        """Exécution réelle d'une tâche"""
        try:
            if task.callback:
                if asyncio.iscoroutinefunction(task.callback):
                    return await task.callback(task.data)
                else:
                    return task.callback(task.data)
            else:
                # Tâche générique
                await asyncio.sleep(0.1)  # Simulation
                return f"Tâche {task.name} exécutée"
                
        except Exception as e:
            raise Exception(f"Erreur exécution tâche {task.name}: {e}")
    
    async def add_task(self, task: Task, priority: TaskPriority = None) -> bool:
        """Ajout d'une tâche au système"""
        try:
            if priority:
                task.priority = priority
            
            queue = self.priority_queues[task.priority]
            
            try:
                queue.put_nowait(task)
                self.logger.debug(f"➕ Tâche ajoutée: {task.name} (priorité: {task.priority.name})")
                return True
            except asyncio.QueueFull:
                self.logger.warning(f"⚠️ Queue {task.priority.name} pleine")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erreur ajout tâche: {e}")
            return False
    
    async def add_simple_task(self, name: str, callback: Callable, data: Dict = None, 
                            priority: TaskPriority = TaskPriority.MEDIUM) -> str:
        """Ajout d'une tâche simple"""
        task = Task(
            name=name,
            callback=callback,
            data=data or {},
            priority=priority
        )
        
        success = await self.add_task(task)
        return task.id if success else None
    
    async def _health_monitor(self):
        """Monitoring de santé des workers"""
        while self.is_running:
            try:
                current_time = datetime.now()
                
                for worker_id, stats in self.worker_stats.items():
                    # Vérifier l'activité récente
                    time_since_activity = (current_time - stats.last_activity).total_seconds()
                    
                    if time_since_activity > 60:  # Plus d'activité depuis 1 minute
                        stats.is_healthy = False
                        self.logger.warning(f"⚠️ Worker {worker_id} inactif")
                    
                    # Calculer le taux d'erreur
                    total_tasks = stats.tasks_completed + stats.tasks_failed
                    if total_tasks > 0:
                        stats.error_rate = stats.tasks_failed / total_tasks
                    
                await asyncio.sleep(self.health_check_interval)
                
            except Exception as e:
                self.logger.error(f"❌ Erreur health monitor: {e}")
                await asyncio.sleep(self.health_check_interval)
    
    async def _stats_updater(self):
        """Mise à jour des statistiques"""
        while self.is_running:
            try:
                # Mettre à jour les métriques globales
                total_processing_time = sum(
                    stats.total_processing_time for stats in self.worker_stats.values()
                )
                
                if self.performance_metrics['completed_tasks'] > 0:
                    self.performance_metrics['avg_processing_time'] = (
                        total_processing_time / self.performance_metrics['completed_tasks']
                    )
                
                # Tailles des queues
                self.performance_metrics['queue_sizes'] = {
                    priority.name: queue.qsize()
                    for priority, queue in self.priority_queues.items()
                }
                
                # Utilisation des workers
                active_workers = len([
                    stats for stats in self.worker_stats.values()
                    if stats.current_task is not None
                ])
                
                self.performance_metrics['worker_utilization'] = (
                    active_workers / self.max_workers * 100
                )
                
                await asyncio.sleep(self.stats_update_interval)
                
            except Exception as e:
                self.logger.error(f"❌ Erreur stats updater: {e}")
                await asyncio.sleep(self.stats_update_interval)
    
    async def _queue_balancer(self):
        """Équilibrage intelligent des queues"""
        while self.is_running:
            try:
                # Vérifier si les queues critiques sont surchargées
                critical_queue = self.priority_queues[TaskPriority.CRITICAL]
                high_queue = self.priority_queues[TaskPriority.HIGH]
                
                if critical_queue.qsize() > 50:
                    self.logger.warning("⚠️ Queue critique surchargée")
                    # Pourrait implémenter une logique de répartition
                
                if high_queue.qsize() > 100:
                    self.logger.warning("⚠️ Queue haute priorité surchargée")
                
                await asyncio.sleep(30)  # Vérifier toutes les 30 secondes
                
            except Exception as e:
                self.logger.error(f"❌ Erreur queue balancer: {e}")
                await asyncio.sleep(30)
    
    async def _trigger_callback(self, event: str, *args):
        """Déclenchement des callbacks"""
        for callback in self.task_callbacks.get(event, []):
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(*args)
                else:
                    callback(*args)
            except Exception as e:
                self.logger.error(f"❌ Erreur callback {event}: {e}")
    
    async def _clear_all_queues(self):
        """Vidage de toutes les queues"""
        for priority, queue in self.priority_queues.items():
            while not queue.empty():
                try:
                    task = queue.get_nowait()
                    task.status = TaskStatus.CANCELLED
                except asyncio.QueueEmpty:
                    break
    
    def add_callback(self, event: str, callback: Callable):
        """Ajout d'un callback pour un événement"""
        if event in self.task_callbacks:
            self.task_callbacks[event].append(callback)
    
    def get_stats(self) -> Dict:
        """Statistiques du système"""
        return {
            'performance_metrics': self.performance_metrics,
            'worker_stats': {
                worker_id: {
                    'tasks_completed': stats.tasks_completed,
                    'tasks_failed': stats.tasks_failed,
                    'error_rate': stats.error_rate,
                    'is_healthy': stats.is_healthy,
                    'current_task': stats.current_task
                }
                for worker_id, stats in self.worker_stats.items()
            },
            'queue_status': {
                priority.name: {
                    'size': queue.qsize(),
                    'maxsize': queue.maxsize
                }
                for priority, queue in self.priority_queues.items()
            },
            'is_running': self.is_running
        }
    
    def get_health_report(self) -> Dict:
        """Rapport de santé du système"""
        healthy_workers = len([
            stats for stats in self.worker_stats.values()
            if stats.is_healthy
        ])
        
        total_queue_size = sum(queue.qsize() for queue in self.priority_queues.values())
        
        return {
            'system_health': 'HEALTHY' if healthy_workers >= self.max_workers * 0.8 else 'DEGRADED',
            'healthy_workers': healthy_workers,
            'total_workers': self.max_workers,
            'total_queue_size': total_queue_size,
            'avg_processing_time': self.performance_metrics['avg_processing_time'],
            'worker_utilization': self.performance_metrics['worker_utilization'],
            'completed_tasks': self.performance_metrics['completed_tasks'],
            'failed_tasks': self.performance_metrics['failed_tasks']
        }

# Instance globale
ultra_worker_system = UltraRobustWorkerSystem()

# Fonctions utilitaires
async def start_workers():
    """Démarrage du système de workers"""
    return await ultra_worker_system.start()

async def stop_workers():
    """Arrêt du système de workers"""
    return await ultra_worker_system.stop()

async def add_worker_task(name: str, callback: Callable, data: Dict = None, 
                         priority: TaskPriority = TaskPriority.MEDIUM):
    """Ajout d'une tâche worker"""
    return await ultra_worker_system.add_simple_task(name, callback, data, priority)

def get_worker_stats():
    """Statistiques des workers"""
    return ultra_worker_system.get_stats()

def get_worker_health():
    """Santé des workers"""
    return ultra_worker_system.get_health_report()

# Exemple d'utilisation
async def example_task(data: Dict) -> str:
    """Tâche d'exemple"""
    await asyncio.sleep(0.1)
    return f"Traité: {data.get('message', 'aucune donnée')}"

if __name__ == "__main__":
    async def test_worker_system():
        print("🔧 Test du système workers ultra-robuste")
        
        # Démarrer le système
        success = await start_workers()
        
        if success:
            print("✅ Système workers démarré")
            
            # Ajouter quelques tâches de test
            tasks = []
            for i in range(10):
                task_id = await add_worker_task(
                    f"test_task_{i}",
                    example_task,
                    {'message': f'Test {i}'},
                    TaskPriority.HIGH if i % 2 == 0 else TaskPriority.MEDIUM
                )
                tasks.append(task_id)
            
            print(f"➕ {len(tasks)} tâches ajoutées")
            
            # Attendre traitement
            await asyncio.sleep(5)
            
            # Afficher statistiques
            stats = get_worker_stats()
            health = get_worker_health()
            
            print(f"📊 Tâches terminées: {stats['performance_metrics']['completed_tasks']}")
            print(f"📊 Santé système: {health['system_health']}")
            print(f"📊 Utilisation workers: {health['worker_utilization']:.1f}%")
            
            # Arrêter le système
            await stop_workers()
            print("✅ Système workers arrêté")
        else:
            print("❌ Échec démarrage système workers")
    
    # Exécuter le test
    asyncio.run(test_worker_system())
