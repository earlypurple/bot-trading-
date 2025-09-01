"""
⚡ OPTIMISEUR DE LATENCE API ULTRA-AVANCÉ - TRADINGBOT PRO 2025 ULTRA
Système d'optimisation de latence avec cache intelligent et connexions persistantes
"""

import asyncio
import aiohttp
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
import json
import hashlib
from collections import defaultdict
import statistics
import logging
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import weakref

@dataclass
class LatencyMetrics:
    """Métriques de latence pour une API"""
    endpoint: str
    avg_latency: float
    min_latency: float
    max_latency: float
    success_rate: float
    total_requests: int
    failed_requests: int
    last_updated: datetime

class IntelligentCache:
    """Cache intelligent avec TTL adaptatif"""
    
    def __init__(self, default_ttl: int = 300):
        self.cache = {}
        self.access_times = defaultdict(list)
        self.default_ttl = default_ttl
        self.hit_count = 0
        self.miss_count = 0
    
    def _generate_key(self, endpoint: str, params: Dict = None) -> str:
        """Génération de clé de cache"""
        key_data = f"{endpoint}:{json.dumps(params or {}, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, endpoint: str, params: Dict = None) -> Optional[Any]:
        """Récupération depuis le cache"""
        key = self._generate_key(endpoint, params)
        
        if key in self.cache:
            data, expiry, access_count = self.cache[key]
            
            if datetime.now() < expiry:
                # Mettre à jour les statistiques d'accès
                self.cache[key] = (data, expiry, access_count + 1)
                self.access_times[key].append(datetime.now())
                self.hit_count += 1
                return data
            else:
                # Données expirées
                del self.cache[key]
        
        self.miss_count += 1
        return None
    
    def set(self, endpoint: str, data: Any, params: Dict = None, ttl: int = None) -> None:
        """Mise en cache avec TTL adaptatif"""
        key = self._generate_key(endpoint, params)
        
        # TTL adaptatif basé sur la fréquence d'accès
        if key in self.access_times and len(self.access_times[key]) > 1:
            # Calculer la fréquence d'accès
            recent_accesses = [
                t for t in self.access_times[key] 
                if t > datetime.now() - timedelta(hours=1)
            ]
            
            if len(recent_accesses) > 5:  # Fréquemment accédé
                adaptive_ttl = max(60, (ttl or self.default_ttl) // 2)
            else:
                adaptive_ttl = ttl or self.default_ttl
        else:
            adaptive_ttl = ttl or self.default_ttl
        
        expiry = datetime.now() + timedelta(seconds=adaptive_ttl)
        self.cache[key] = (data, expiry, 1)
        
        # Nettoyer les anciennes entrées d'accès
        if key in self.access_times:
            self.access_times[key] = [
                t for t in self.access_times[key] 
                if t > datetime.now() - timedelta(hours=24)
            ]
    
    def get_stats(self) -> Dict:
        """Statistiques du cache"""
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'hit_count': self.hit_count,
            'miss_count': self.miss_count,
            'hit_rate': hit_rate,
            'cache_size': len(self.cache)
        }
    
    def clear_expired(self) -> int:
        """Nettoyage des entrées expirées"""
        now = datetime.now()
        expired_keys = [
            key for key, (_, expiry, _) in self.cache.items()
            if now >= expiry
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        return len(expired_keys)

class ConnectionPool:
    """Pool de connexions persistantes avec load balancing"""
    
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.sessions = {}
        self.session_stats = defaultdict(lambda: {'requests': 0, 'errors': 0})
        self.last_cleanup = datetime.now()
    
    async def get_session(self, base_url: str) -> aiohttp.ClientSession:
        """Obtention d'une session persistante"""
        if base_url not in self.sessions:
            # Créer une nouvelle session avec configuration optimisée
            connector = aiohttp.TCPConnector(
                limit=self.max_connections,
                limit_per_host=5,
                keepalive_timeout=30,
                enable_cleanup_closed=True
            )
            
            timeout = aiohttp.ClientTimeout(
                total=30,
                connect=10,
                sock_read=20
            )
            
            session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={
                    'User-Agent': 'TradingBot-Pro-2025-Ultra/1.0',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive'
                }
            )
            
            self.sessions[base_url] = session
        
        return self.sessions[base_url]
    
    def update_stats(self, base_url: str, success: bool):
        """Mise à jour des statistiques de session"""
        self.session_stats[base_url]['requests'] += 1
        if not success:
            self.session_stats[base_url]['errors'] += 1
    
    async def cleanup_sessions(self):
        """Nettoyage des sessions inutilisées"""
        now = datetime.now()
        
        # Nettoyer toutes les heures
        if now - self.last_cleanup > timedelta(hours=1):
            for base_url, session in list(self.sessions.items()):
                stats = self.session_stats[base_url]
                
                # Fermer les sessions avec trop d'erreurs
                if stats['requests'] > 10 and stats['errors'] / stats['requests'] > 0.5:
                    await session.close()
                    del self.sessions[base_url]
                    del self.session_stats[base_url]
            
            self.last_cleanup = now
    
    async def close_all(self):
        """Fermeture de toutes les sessions"""
        for session in self.sessions.values():
            await session.close()
        self.sessions.clear()
        self.session_stats.clear()

class LatencyOptimizer:
    """Optimiseur de latence ultra-avancé"""
    
    def __init__(self, max_connections: int = 20):
        self.cache = IntelligentCache()
        self.connection_pool = ConnectionPool(max_connections)
        self.metrics = {}
        self.request_queue = asyncio.Queue(maxsize=1000)
        self.worker_count = 5
        self.workers = []
        self.is_running = False
        
        # Configuration de priorités
        self.endpoint_priorities = {
            'prices': 1,      # Haute priorité
            'portfolio': 2,   # Moyenne priorité
            'news': 3,        # Basse priorité
            'analytics': 4    # Très basse priorité
        }
        
        # Retry logic
        self.retry_config = {
            'max_retries': 3,
            'base_delay': 0.1,
            'max_delay': 2.0,
            'exponential_base': 2
        }
        
        # Thread pool pour opérations CPU-intensives
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        
        # Callbacks pour monitoring
        self.latency_callbacks = []
    
    async def start(self):
        """Démarrage de l'optimiseur"""
        if self.is_running:
            return
        
        self.is_running = True
        
        # Démarrer les workers
        for i in range(self.worker_count):
            worker = asyncio.create_task(self._request_worker(f"worker-{i}"))
            self.workers.append(worker)
        
        # Démarrer le monitoring
        asyncio.create_task(self._monitoring_loop())
        
        print("⚡ Optimiseur de latence démarré")
    
    async def stop(self):
        """Arrêt de l'optimiseur"""
        self.is_running = False
        
        # Arrêter les workers
        for worker in self.workers:
            worker.cancel()
        
        # Fermer les connexions
        await self.connection_pool.close_all()
        
        # Fermer le thread pool
        self.thread_pool.shutdown(wait=True)
        
        print("⚡ Optimiseur de latence arrêté")
    
    async def _request_worker(self, worker_id: str):
        """Worker pour traiter les requêtes"""
        while self.is_running:
            try:
                # Récupérer une requête de la queue
                request_data = await asyncio.wait_for(
                    self.request_queue.get(), 
                    timeout=1.0
                )
                
                # Traiter la requête
                await self._process_request(request_data)
                
                # Marquer la requête comme terminée
                self.request_queue.task_done()
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"❌ Erreur worker {worker_id}: {e}")
    
    async def _process_request(self, request_data: Dict):
        """Traitement d'une requête optimisée"""
        try:
            endpoint = request_data['endpoint']
            params = request_data.get('params', {})
            priority = request_data.get('priority', 5)
            future = request_data['future']
            
            start_time = time.time()
            
            # Vérifier le cache d'abord
            cached_result = self.cache.get(endpoint, params)
            if cached_result is not None:
                latency = time.time() - start_time
                self._update_metrics(endpoint, latency, True)
                future.set_result(cached_result)
                return
            
            # Faire la requête HTTP avec optimisations
            result = await self._make_optimized_request(endpoint, params)
            
            if result is not None:
                # Mettre en cache selon la priorité
                cache_ttl = self._get_cache_ttl(priority)
                self.cache.set(endpoint, result, params, cache_ttl)
                
                latency = time.time() - start_time
                self._update_metrics(endpoint, latency, True)
                future.set_result(result)
            else:
                latency = time.time() - start_time
                self._update_metrics(endpoint, latency, False)
                future.set_exception(Exception("Request failed"))
                
        except Exception as e:
            future.set_exception(e)
    
    async def _make_optimized_request(self, endpoint: str, params: Dict) -> Optional[Any]:
        """Requête HTTP optimisée avec retry logic"""
        base_url = self._extract_base_url(endpoint)
        session = await self.connection_pool.get_session(base_url)
        
        for attempt in range(self.retry_config['max_retries'] + 1):
            try:
                async with session.get(endpoint, params=params) as response:
                    if response.status == 200:
                        self.connection_pool.update_stats(base_url, True)
                        return await response.json()
                    elif response.status == 429:  # Rate limited
                        retry_after = int(response.headers.get('Retry-After', 1))
                        await asyncio.sleep(retry_after)
                        continue
                    else:
                        self.connection_pool.update_stats(base_url, False)
                        return None
                        
            except asyncio.TimeoutError:
                if attempt < self.retry_config['max_retries']:
                    delay = min(
                        self.retry_config['base_delay'] * (
                            self.retry_config['exponential_base'] ** attempt
                        ),
                        self.retry_config['max_delay']
                    )
                    await asyncio.sleep(delay)
                else:
                    self.connection_pool.update_stats(base_url, False)
                    return None
            except Exception as e:
                self.connection_pool.update_stats(base_url, False)
                if attempt == self.retry_config['max_retries']:
                    return None
                
                delay = min(
                    self.retry_config['base_delay'] * (
                        self.retry_config['exponential_base'] ** attempt
                    ),
                    self.retry_config['max_delay']
                )
                await asyncio.sleep(delay)
        
        return None
    
    def _extract_base_url(self, endpoint: str) -> str:
        """Extraction de l'URL de base"""
        from urllib.parse import urlparse
        parsed = urlparse(endpoint)
        return f"{parsed.scheme}://{parsed.netloc}"
    
    def _get_cache_ttl(self, priority: int) -> int:
        """TTL du cache basé sur la priorité"""
        ttl_map = {
            1: 30,    # Haute priorité - 30 secondes
            2: 120,   # Moyenne priorité - 2 minutes
            3: 300,   # Basse priorité - 5 minutes
            4: 600,   # Très basse priorité - 10 minutes
            5: 900    # Défaut - 15 minutes
        }
        return ttl_map.get(priority, 300)
    
    def _update_metrics(self, endpoint: str, latency: float, success: bool):
        """Mise à jour des métriques de latence"""
        if endpoint not in self.metrics:
            self.metrics[endpoint] = LatencyMetrics(
                endpoint=endpoint,
                avg_latency=0.0,
                min_latency=float('inf'),
                max_latency=0.0,
                success_rate=0.0,
                total_requests=0,
                failed_requests=0,
                last_updated=datetime.now()
            )
        
        metric = self.metrics[endpoint]
        metric.total_requests += 1
        
        if success:
            # Mettre à jour les latences
            metric.min_latency = min(metric.min_latency, latency)
            metric.max_latency = max(metric.max_latency, latency)
            
            # Moyenne mobile pour la latence moyenne
            alpha = 0.1  # Facteur de lissage
            metric.avg_latency = (alpha * latency + 
                                (1 - alpha) * metric.avg_latency)
        else:
            metric.failed_requests += 1
        
        # Calculer le taux de succès
        metric.success_rate = (
            (metric.total_requests - metric.failed_requests) / 
            metric.total_requests * 100
        )
        
        metric.last_updated = datetime.now()
        
        # Déclencher les callbacks
        self._trigger_latency_callbacks(endpoint, metric)
    
    def _trigger_latency_callbacks(self, endpoint: str, metric: LatencyMetrics):
        """Déclenchement des callbacks de latence"""
        for callback in self.latency_callbacks:
            try:
                callback(endpoint, metric)
            except Exception as e:
                print(f"❌ Erreur callback latence: {e}")
    
    async def _monitoring_loop(self):
        """Boucle de monitoring et optimisation"""
        while self.is_running:
            try:
                # Nettoyer le cache
                expired_count = self.cache.clear_expired()
                if expired_count > 0:
                    print(f"🧹 Nettoyé {expired_count} entrées de cache expirées")
                
                # Nettoyer les connexions
                await self.connection_pool.cleanup_sessions()
                
                # Analyser les métriques
                await self._analyze_performance()
                
                await asyncio.sleep(60)  # Monitoring toutes les minutes
                
            except Exception as e:
                print(f"❌ Erreur monitoring: {e}")
                await asyncio.sleep(60)
    
    async def _analyze_performance(self):
        """Analyse des performances et optimisations"""
        try:
            # Identifier les endpoints lents
            slow_endpoints = [
                metric for metric in self.metrics.values()
                if metric.avg_latency > 2.0  # Plus de 2 secondes
            ]
            
            for metric in slow_endpoints:
                print(f"⚠️ Endpoint lent détecté: {metric.endpoint} "
                      f"({metric.avg_latency:.2f}s)")
                
                # Ajuster la stratégie de cache
                if metric.success_rate > 80:
                    # Augmenter le TTL pour réduire les requêtes
                    print(f"📈 Augmentation du TTL pour {metric.endpoint}")
            
            # Identifier les endpoints avec taux d'échec élevé
            failing_endpoints = [
                metric for metric in self.metrics.values()
                if metric.success_rate < 90 and metric.total_requests > 10
            ]
            
            for metric in failing_endpoints:
                print(f"❌ Endpoint instable: {metric.endpoint} "
                      f"({metric.success_rate:.1f}% succès)")
                
        except Exception as e:
            print(f"❌ Erreur analyse performance: {e}")
    
    async def make_request(self, endpoint: str, params: Dict = None, 
                          priority: int = 5) -> Any:
        """Interface publique pour faire une requête optimisée"""
        if not self.is_running:
            await self.start()
        
        # Créer un Future pour la réponse
        future = asyncio.Future()
        
        # Ajouter à la queue avec priorité
        request_data = {
            'endpoint': endpoint,
            'params': params or {},
            'priority': priority,
            'future': future
        }
        
        try:
            await self.request_queue.put(request_data)
            return await future
        except asyncio.QueueFull:
            raise Exception("Queue de requêtes pleine")
    
    def add_latency_callback(self, callback: Callable[[str, LatencyMetrics], None]):
        """Ajout d'un callback pour monitoring de latence"""
        self.latency_callbacks.append(callback)
    
    def get_metrics(self) -> Dict:
        """Obtention des métriques de performance"""
        cache_stats = self.cache.get_stats()
        
        return {
            'cache_stats': cache_stats,
            'endpoint_metrics': {
                endpoint: {
                    'avg_latency': metric.avg_latency,
                    'min_latency': metric.min_latency,
                    'max_latency': metric.max_latency,
                    'success_rate': metric.success_rate,
                    'total_requests': metric.total_requests,
                    'failed_requests': metric.failed_requests
                }
                for endpoint, metric in self.metrics.items()
            },
            'queue_size': self.request_queue.qsize(),
            'active_workers': len([w for w in self.workers if not w.done()])
        }
    
    def get_performance_summary(self) -> Dict:
        """Résumé des performances"""
        if not self.metrics:
            return {
                'avg_latency': 0.0,
                'total_requests': 0,
                'success_rate': 0.0,
                'cache_hit_rate': 0.0
            }
        
        latencies = [m.avg_latency for m in self.metrics.values()]
        total_requests = sum(m.total_requests for m in self.metrics.values())
        total_failed = sum(m.failed_requests for m in self.metrics.values())
        
        overall_success_rate = (
            (total_requests - total_failed) / total_requests * 100
            if total_requests > 0 else 0
        )
        
        return {
            'avg_latency': statistics.mean(latencies) if latencies else 0.0,
            'median_latency': statistics.median(latencies) if latencies else 0.0,
            'total_requests': total_requests,
            'success_rate': overall_success_rate,
            'cache_hit_rate': self.cache.get_stats()['hit_rate']
        }

# Instance globale
latency_optimizer = LatencyOptimizer()

# Fonctions utilitaires
async def start_latency_optimizer():
    """Démarrage de l'optimiseur de latence"""
    await latency_optimizer.start()

async def stop_latency_optimizer():
    """Arrêt de l'optimiseur de latence"""
    await latency_optimizer.stop()

async def optimized_request(endpoint: str, params: Dict = None, priority: int = 5):
    """Requête optimisée"""
    return await latency_optimizer.make_request(endpoint, params, priority)

def get_latency_metrics():
    """Métriques de latence"""
    return latency_optimizer.get_metrics()

def get_performance_summary():
    """Résumé des performances"""
    return latency_optimizer.get_performance_summary()

if __name__ == "__main__":
    async def test_latency_optimizer():
        print("⚡ Test de l'optimiseur de latence")
        
        # Démarrer l'optimiseur
        await start_latency_optimizer()
        
        # Simuler quelques requêtes
        test_endpoints = [
            "https://api.coingecko.com/api/v3/simple/price",
            "https://api.binance.com/api/v3/ticker/price",
            "https://api.coinbase.com/v2/exchange-rates"
        ]
        
        # Faire des requêtes parallèles
        tasks = []
        for i in range(10):
            for endpoint in test_endpoints:
                task = optimized_request(
                    endpoint, 
                    {'ids': 'bitcoin', 'vs_currencies': 'usd'},
                    priority=1
                )
                tasks.append(task)
        
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            print(f"✅ {len([r for r in results if not isinstance(r, Exception)])} requêtes réussies")
        except Exception as e:
            print(f"❌ Erreur test: {e}")
        
        # Afficher les métriques
        metrics = get_performance_summary()
        print(f"📊 Latence moyenne: {metrics['avg_latency']:.3f}s")
        print(f"📊 Taux de succès: {metrics['success_rate']:.1f}%")
        print(f"📊 Cache hit rate: {metrics['cache_hit_rate']:.1f}%")
        
        # Arrêter l'optimiseur
        await stop_latency_optimizer()
    
    # Exécuter le test
    asyncio.run(test_latency_optimizer())
