"""
🔐 ANALYSE DE SÉCURITÉ - TRADINGBOT PRO 2025 ULTRA
Scanner de vulnérabilités et audit de sécurité complet
"""

import subprocess
import json
import requests
import re
import os
from datetime import datetime
from typing import Dict, List, Any
import pkg_resources
import importlib.metadata

class SecurityAnalyzer:
    """Analyseur de sécurité ultra-complet"""
    
    def __init__(self):
        self.vulnerabilities = []
        self.security_score = 100
        self.recommendations = []
    
    def analyze_dependencies(self) -> List[Dict[str, Any]]:
        """Analyse des dépendances pour vulnérabilités"""
        return self.check_dependencies_vulnerabilities()
    
    def analyze_source_code(self) -> List[Dict[str, Any]]:
        """Analyse du code source pour problèmes de sécurité"""
        return self.check_source_code_security()
    
    def calculate_security_score(self) -> int:
        """Calcule le score de sécurité global"""
        return self.get_security_score()
        
    def check_dependencies_vulnerabilities(self) -> Dict[str, Any]:
        """Scanner les vulnérabilités des dépendances"""
        print("🔍 Analyse des vulnérabilités des dépendances...")
        
        try:
            # Utiliser safety pour scanner les vulnérabilités
            result = subprocess.run(['safety', 'check', '--json'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                vulnerabilities = json.loads(result.stdout) if result.stdout else []
            else:
                # Si safety n'est pas installé, utiliser une vérification manuelle
                vulnerabilities = self.manual_vulnerability_check()
            
            return {
                'total_vulnerabilities': len(vulnerabilities),
                'critical': len([v for v in vulnerabilities if v.get('severity', '').lower() == 'critical']),
                'high': len([v for v in vulnerabilities if v.get('severity', '').lower() == 'high']),
                'medium': len([v for v in vulnerabilities if v.get('severity', '').lower() == 'medium']),
                'low': len([v for v in vulnerabilities if v.get('severity', '').lower() == 'low']),
                'details': vulnerabilities
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Impossible de scanner les vulnérabilités automatiquement'
            }
    
    def check_source_code_security(self) -> List[Dict[str, Any]]:
        """Vérification de sécurité du code source"""
        print("🔍 Analyse de sécurité du code source...")
        
        security_issues = []
        
        # Patterns de sécurité à vérifier
        security_patterns = {
            'hardcoded_secrets': [
                r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
                r'secret[_-]?key\s*=\s*["\'][^"\']+["\']',
                r'password\s*=\s*["\'][^"\']+["\']',
                r'token\s*=\s*["\'][^"\']+["\']'
            ],
            'sql_injection': [
                r'query\s*=\s*["\'].*\+.*["\']',
                r'execute\s*\(["\'].*%.*["\']',
                r'cursor\.execute\s*\(["\'].*\+.*["\']'
            ],
            'unsafe_imports': [
                r'from\s+pickle\s+import',
                r'import\s+pickle',
                r'eval\s*\(',
                r'exec\s*\('
            ]
        }
        
        # Scanner tous les fichiers Python
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                            for category, patterns in security_patterns.items():
                                for pattern in patterns:
                                    matches = re.finditer(pattern, content, re.IGNORECASE)
                                    for match in matches:
                                        security_issues.append({
                                            'file': file_path,
                                            'category': category,
                                            'pattern': pattern,
                                            'line': content[:match.start()].count('\n') + 1,
                                            'severity': 'high' if category == 'hardcoded_secrets' else 'medium'
                                        })
                    except Exception:
                        continue
        
        return security_issues
    
    def calculate_security_score(self) -> int:
        """Calcule le score de sécurité global - méthode corrigée"""
        # Analyse des dépendances
        vuln_results = self.analyze_dependencies()
        
        # Analyse du code source
        code_results = self.analyze_source_code()
        
        # Analyse de l'environnement (simulation)
        env_results = self.analyze_environment()
        
        return self.get_security_score(vuln_results, code_results, env_results)
    
    def analyze_environment(self) -> Dict[str, Any]:
        """Analyse de l'environnement de sécurité"""
        print("🔍 Analyse de sécurité de l'environnement...")
        
        env_issues = []
        
        # Vérifier les variables d'environnement sensibles
        sensitive_vars = ['API_KEY', 'SECRET_KEY', 'PASSWORD', 'TOKEN']
        for var in sensitive_vars:
            if os.getenv(var):
                env_issues.append({
                    'type': 'exposed_env_var',
                    'variable': var,
                    'severity': 'medium',
                    'recommendation': f'Chiffrer la variable {var}'
                })
        
        # Vérifier les permissions de fichiers
        sensitive_files = ['config.py', '.env', 'credentials.json']
        for file_name in sensitive_files:
            if os.path.exists(file_name):
                stat_info = os.stat(file_name)
                permissions = oct(stat_info.st_mode)[-3:]
                if permissions != '600':  # Pas assez restrictif
                    env_issues.append({
                        'type': 'file_permissions',
                        'file': file_name,
                        'current_permissions': permissions,
                        'severity': 'high',
                        'recommendation': f'chmod 600 {file_name}'
                    })
        
        return {
            'total_issues': len(env_issues),
            'issues': env_issues
        }
    
    def get_security_score(self, vuln_results: Any, code_results: List, env_results: Dict) -> int:
        """Calcule le score de sécurité global avec tous les résultats"""
        base_score = 100
        
        # Analyse des dépendances
        if isinstance(vuln_results, dict) and 'total_vulnerabilities' in vuln_results:
            critical = vuln_results.get('critical', 0)
            high = vuln_results.get('high', 0) 
            medium = vuln_results.get('medium', 0)
            low = vuln_results.get('low', 0)
            
            base_score -= (critical * 20 + high * 10 + medium * 5 + low * 2)
        
        # Analyse du code source
        critical_code = len([i for i in code_results if i.get('severity') == 'high'])
        medium_code = len([i for i in code_results if i.get('severity') == 'medium'])
        base_score -= (critical_code * 15 + medium_code * 5)
        
        # Analyse de l'environnement
        env_issues = env_results.get('total_issues', 0)
        base_score -= (env_issues * 3)
        
        return max(0, min(100, base_score))
    
    def manual_vulnerability_check(self) -> List[Dict[str, Any]]:
        """Vérification manuelle des packages à risque"""
        risky_patterns = [
            {'package': 'requests', 'min_version': '2.28.0', 'reason': 'Vulnérabilités SSL anciennes'},
            {'package': 'urllib3', 'min_version': '1.26.12', 'reason': 'Vulnérabilités de sécurité'},
            {'package': 'flask', 'min_version': '2.2.0', 'reason': 'Vulnérabilités XSS et CSRF'},
            {'package': 'numpy', 'min_version': '1.22.0', 'reason': 'Buffer overflow possibles'},
            {'package': 'pandas', 'min_version': '1.4.0', 'reason': 'Vulnérabilités dans les anciennes versions'},
            {'package': 'tensorflow', 'min_version': '2.8.0', 'reason': 'Vulnérabilités de sécurité critiques'}
        ]
        
        vulnerabilities = []
        
        try:
            installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
            
            for risk in risky_patterns:
                package_name = risk['package']
                if package_name in installed_packages:
                    installed_version = installed_packages[package_name]
                    min_version = risk['min_version']
                    
                    if self.version_compare(installed_version, min_version) < 0:
                        vulnerabilities.append({
                            'package': package_name,
                            'installed_version': installed_version,
                            'min_safe_version': min_version,
                            'severity': 'medium',
                            'description': risk['reason']
                        })
        
        except Exception as e:
            print(f"Erreur lors de la vérification manuelle: {e}")
        
        return vulnerabilities
    
    def version_compare(self, v1: str, v2: str) -> int:
        """Compare deux versions (retourne -1 si v1 < v2, 0 si égales, 1 si v1 > v2)"""
        try:
            from packaging import version
            if version.parse(v1) < version.parse(v2):
                return -1
            elif version.parse(v1) > version.parse(v2):
                return 1
            else:
                return 0
        except:
            # Comparaison simple si packaging n'est pas disponible
            v1_parts = [int(x) for x in v1.split('.')]
            v2_parts = [int(x) for x in v2.split('.')]
            
            for i in range(max(len(v1_parts), len(v2_parts))):
                v1_part = v1_parts[i] if i < len(v1_parts) else 0
                v2_part = v2_parts[i] if i < len(v2_parts) else 0
                
                if v1_part < v2_part:
                    return -1
                elif v1_part > v2_part:
                    return 1
            return 0
    
    def check_code_security(self) -> Dict[str, Any]:
        """Analyser la sécurité du code source"""
        print("🔍 Analyse de sécurité du code source...")
        
        security_issues = []
        files_scanned = 0
        
        # Patterns de sécurité à vérifier
        security_patterns = [
            {
                'pattern': r'password\s*=\s*["\'][^"\']+["\']',
                'severity': 'high',
                'description': 'Mot de passe en dur détecté'
            },
            {
                'pattern': r'api_key\s*=\s*["\'][^"\']+["\']',
                'severity': 'high',
                'description': 'Clé API en dur détectée'
            },
            {
                'pattern': r'secret\s*=\s*["\'][^"\']+["\']',
                'severity': 'high',
                'description': 'Secret en dur détecté'
            },
            {
                'pattern': r'eval\s*\(',
                'severity': 'critical',
                'description': 'Utilisation dangereuse de eval()'
            },
            {
                'pattern': r'exec\s*\(',
                'severity': 'critical',
                'description': 'Utilisation dangereuse de exec()'
            },
            {
                'pattern': r'shell=True',
                'severity': 'medium',
                'description': 'Utilisation de shell=True dans subprocess'
            },
            {
                'pattern': r'pickle\.loads?\(',
                'severity': 'high',
                'description': 'Désérialisation pickle non sécurisée'
            },
            {
                'pattern': r'input\s*\(',
                'severity': 'low',
                'description': 'Utilisation de input() potentiellement dangereuse'
            }
        ]
        
        # Scanner les fichiers Python
        for root, dirs, files in os.walk('src'):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    files_scanned += 1
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                            for pattern_data in security_patterns:
                                matches = re.finditer(pattern_data['pattern'], content, re.IGNORECASE)
                                for match in matches:
                                    line_num = content[:match.start()].count('\n') + 1
                                    security_issues.append({
                                        'file': file_path,
                                        'line': line_num,
                                        'severity': pattern_data['severity'],
                                        'description': pattern_data['description'],
                                        'code_snippet': match.group()[:100]
                                    })
                    
                    except Exception as e:
                        print(f"Erreur lors de l'analyse de {file_path}: {e}")
        
        return {
            'files_scanned': files_scanned,
            'total_issues': len(security_issues),
            'critical': len([i for i in security_issues if i['severity'] == 'critical']),
            'high': len([i for i in security_issues if i['severity'] == 'high']),
            'medium': len([i for i in security_issues if i['severity'] == 'medium']),
            'low': len([i for i in security_issues if i['severity'] == 'low']),
            'issues': security_issues
        }
    
    def check_environment_security(self) -> Dict[str, Any]:
        """Vérifier la sécurité de l'environnement"""
        print("🔍 Analyse de sécurité de l'environnement...")
        
        env_issues = []
        
        # Vérifier les variables d'environnement sensibles
        sensitive_env_vars = [
            'API_KEY', 'SECRET_KEY', 'PASSWORD', 'TOKEN',
            'COINBASE_API_KEY', 'COINBASE_SECRET_KEY'
        ]
        
        for var in sensitive_env_vars:
            if var in os.environ:
                value = os.environ[var]
                if len(value) < 20:
                    env_issues.append({
                        'variable': var,
                        'issue': 'Clé trop courte (potentiellement faible)',
                        'severity': 'medium'
                    })
                
                # Vérifier si la clé semble être un exemple/test
                if value.lower() in ['test', 'example', 'demo', '12345']:
                    env_issues.append({
                        'variable': var,
                        'issue': 'Clé de test/exemple détectée',
                        'severity': 'low'
                    })
        
        # Vérifier les permissions de fichiers
        file_permissions = []
        sensitive_files = ['src/config.py', '.env', 'requirements.txt']
        
        for file_path in sensitive_files:
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                permissions = oct(stat.st_mode)[-3:]
                
                if permissions[2] != '0':  # Autres utilisateurs ont des permissions
                    env_issues.append({
                        'file': file_path,
                        'issue': f'Permissions trop ouvertes: {permissions}',
                        'severity': 'medium'
                    })
                
                file_permissions.append({
                    'file': file_path,
                    'permissions': permissions
                })
        
        return {
            'environment_variables_checked': len(sensitive_env_vars),
            'files_checked': len(sensitive_files),
            'total_issues': len(env_issues),
            'issues': env_issues,
            'file_permissions': file_permissions
        }
    
    def generate_security_recommendations(self, vuln_results: Dict, code_results: Dict, env_results: Dict) -> List[str]:
        """Générer des recommandations de sécurité"""
        recommendations = []
        
        # Recommandations basées sur les vulnérabilités
        if vuln_results.get('total_vulnerabilities', 0) > 0:
            recommendations.append("Mettre à jour les dépendances vulnérables immédiatement")
            recommendations.append("Configurer des alertes automatiques pour les nouvelles vulnérabilités")
        
        # Recommandations basées sur le code
        if code_results.get('critical', 0) > 0:
            recommendations.append("Corriger immédiatement les problèmes critiques de sécurité dans le code")
        
        if code_results.get('high', 0) > 0:
            recommendations.append("Remplacer les secrets en dur par des variables d'environnement")
            recommendations.append("Réviser l'utilisation de eval() et exec()")
        
        # Recommandations basées sur l'environnement
        if env_results.get('total_issues', 0) > 0:
            recommendations.append("Renforcer les clés API et mots de passe")
            recommendations.append("Corriger les permissions de fichiers sensibles")
        
        # Recommandations générales
        recommendations.extend([
            "Implémenter un système de logging de sécurité",
            "Configurer HTTPS pour toutes les communications",
            "Ajouter une authentification à deux facteurs (2FA)",
            "Mettre en place une surveillance des accès",
            "Effectuer des audits de sécurité réguliers",
            "Chiffrer les données sensibles au repos",
            "Implémenter une politique de mots de passe forts",
            "Configurer des sauvegardes sécurisées"
        ])
        
        return recommendations
    
    def calculate_security_score(self, vuln_results: Dict, code_results: Dict, env_results: Dict) -> int:
        """Calculer un score de sécurité global"""
        score = 100
        
        # Pénalités pour vulnérabilités
        score -= vuln_results.get('critical', 0) * 20
        score -= vuln_results.get('high', 0) * 10
        score -= vuln_results.get('medium', 0) * 5
        score -= vuln_results.get('low', 0) * 2
        
        # Pénalités pour problèmes de code
        score -= code_results.get('critical', 0) * 15
        score -= code_results.get('high', 0) * 8
        score -= code_results.get('medium', 0) * 4
        score -= code_results.get('low', 0) * 1
        
        # Pénalités pour problèmes d'environnement
        score -= env_results.get('total_issues', 0) * 3
        
        return max(0, score)  # Score minimum de 0
    
    def run_complete_security_audit(self) -> Dict[str, Any]:
        """Lancer un audit de sécurité complet"""
        print("🔐 DÉBUT DE L'AUDIT DE SÉCURITÉ COMPLET")
        print("=" * 50)
        
        start_time = datetime.now()
        
        # 1. Analyser les vulnérabilités des dépendances
        vuln_results = self.check_dependencies_vulnerabilities()
        
        # 2. Analyser la sécurité du code
        code_results = self.check_code_security()
        
        # 3. Analyser l'environnement
        env_results = self.check_environment_security()
        
        # 4. Générer recommandations
        recommendations = self.generate_security_recommendations(vuln_results, code_results, env_results)
        
        # 5. Calculer le score de sécurité
        security_score = self.calculate_security_score(vuln_results, code_results, env_results)
        
        end_time = datetime.now()
        
        # Rapport final
        report = {
            'audit_info': {
                'timestamp': start_time.isoformat(),
                'duration_seconds': (end_time - start_time).total_seconds(),
                'security_score': security_score,
                'grade': self.get_security_grade(security_score)
            },
            'vulnerability_analysis': vuln_results,
            'code_security_analysis': code_results,
            'environment_security_analysis': env_results,
            'recommendations': recommendations,
            'summary': {
                'total_issues': (
                    vuln_results.get('total_vulnerabilities', 0) +
                    code_results.get('total_issues', 0) +
                    env_results.get('total_issues', 0)
                ),
                'critical_issues': (
                    vuln_results.get('critical', 0) +
                    code_results.get('critical', 0)
                ),
                'high_issues': (
                    vuln_results.get('high', 0) +
                    code_results.get('high', 0)
                )
            }
        }
        
        # Sauvegarder le rapport
        with open('security_audit_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.print_security_report(report)
        return report
    
    def get_security_grade(self, score: int) -> str:
        """Obtenir une note de sécurité"""
        if score >= 90:
            return 'A+'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        elif score >= 50:
            return 'D'
        else:
            return 'F'
    
    def print_security_report(self, report: Dict[str, Any]):
        """Afficher le rapport de sécurité"""
        print("\n" + "="*60)
        print("🛡️ RAPPORT D'AUDIT DE SÉCURITÉ")
        print("="*60)
        
        audit_info = report['audit_info']
        print(f"🎯 Score de sécurité: {audit_info['security_score']}/100 ({audit_info['grade']})")
        
        summary = report['summary']
        print(f"⚠️ Total des problèmes: {summary['total_issues']}")
        print(f"🔴 Critiques: {summary['critical_issues']}")
        print(f"🟡 Élevés: {summary['high_issues']}")
        
        if summary['critical_issues'] > 0:
            print("\n🚨 ATTENTION: Problèmes critiques détectés !")
        elif summary['high_issues'] > 0:
            print("\n⚠️ Des problèmes de sécurité importants nécessitent votre attention")
        elif summary['total_issues'] == 0:
            print("\n✅ Aucun problème de sécurité détecté !")
        
        print(f"\n📋 Recommandations principales:")
        for i, rec in enumerate(report['recommendations'][:5], 1):
            print(f"  {i}. {rec}")
        
        print(f"\n📄 Rapport complet sauvegardé: security_audit_report.json")
        print("="*60)

# Fonction principale pour tests
def main():
    analyzer = SecurityAnalyzer()
    analyzer.run_complete_security_audit()

if __name__ == "__main__":
    main()
